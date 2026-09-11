# 架构定稿：决策者 State / 回环状态机 + 记忆 Schema

> 状态：**已定稿（设计）· 记忆层工程已落地（2026-09-08）**  
> 依据：运行时四层定稿；用户确认 A 按最优方案、B 按跨端历史 + 长记忆读写 + 学情总览（定时/手动刷新）；**无教师端**（竞赛范围：学生端 + 管理端）。  
> 记忆落地：`chat_threads`/`chat_messages` 服务端权威 + 前端 IndexedDB 缓存；`long_term_memories` + `memory_search|upsert|forget`；回合注入 `memory_brief`；学情重建含长期记忆。

---

## 〇、与产品范围对齐

| 角色 | 可见 |
|------|------|
| 学生 | 对话历史（跨端）、学情总览、错题、练习；对话步骤条 |
| 管理端 `admin` | 题库/回流；可选班级聚合学情；**完整 Agent trace** |
| ~~教师端~~ | **已取消** |

隐私红线（保留）：对话**原文**与**摘要**仅学生本人；学情画像可本人看，管理端仅看聚合/运维必要字段（不含对话原文）。

---

# A. 决策者 State 与回环状态机（推荐方案）

## A1. 设计原则

1. **一次用户请求 = 一条 Agent 线程回合**（可 checkpoint）；State 描述「这一次任务走到哪」。  
2. **题库匹配为第 0 段**，不计入自研 3 轮。  
3. **自研一轮**定义：`再规划 → ≥1 次工具调用 → 回判`；`autonomous_round ∈ {1,2,3}`。  
4. 编排只执行；**是否交付、是否回环**只由规划/推理层改 `phase`。  
5. 护栏可把 `phase` 打到 `fused` / `delivered_degraded`，并写 `stop_reason`。

## A2. 阶段（phase）

```text
perceived          感知完成（有 question_text）
planned            已产出 intent + plan.steps
awaiting_tool      编排正在执行某 step / 工具
judging            决策者回判中（题库匹配或自研复检）
bank_accepted      题库匹配通过 → 即将交付权威答案
autonomous         已进入自主路线（round 从 1 起算）
deliverable        回判通过，可渲染交付
delivered          已输出给用户（终态）
delivered_degraded 第 3 轮仍不足或熔断后，输出「当前最佳+说明」（终态）
fused              护栏强制停止且无可交付正文（终态，少见）
```

### 状态转移（主路径）

```text
perceived
  → planned
  → awaiting_tool (search_bank / graph / …)
  → judging (match_judge)
       ├─ 同一道题 → bank_accepted → delivered
       └─ 否/无候选 → autonomous (round=1)
            → planned(再规划) → awaiting_tool → judging
                 ├─ 满足 → deliverable → delivered
                 └─ 不满足且 round<3 → autonomous (round+=1) → …
                 └─ 不满足且 round≥3 → delivered_degraded
```

讲解 / 学习计划 / 寒暄：无题库第 0 段，直接 `planned → awaiting_tool(graph/explain) → judging → deliverable → delivered`（仍可走 validate；失败则 degraded）。

## A3. AgentState 最小字段（建议 TypedDict）

### 感知与输入

| 字段 | 类型 | 说明 |
|------|------|------|
| `thread_id` | str | 会话线程 |
| `user_id` | str | 学生身份 |
| `raw_text` / `image_ref` | str? | 原始输入引用（图可只存对象键，不进 LLM） |
| `question_text` | str | OCR/文本归一结果 |
| `source` | text\|image\|mixed | |
| `volume_hint` | {estimated_items, heavy?} | 感知粗估 |

### 规划与回环

| 字段 | 类型 | 说明 |
|------|------|------|
| `phase` | 见 A2 | 当前阶段 |
| `intent` | solve\|explain\|study_plan\|syllabus\|chat\|mixed | |
| `plan` | {summary, steps[], needs_drawing, allow_bank} | 当前规划 |
| `plan_version` | int | 每再规划 +1 |
| `autonomous_round` | 0..3 | 0=未进自研 |
| `max_autonomous_rounds` | 3 | 常量可配置 |

### 题库与回判

| 字段 | 类型 | 说明 |
|------|------|------|
| `bank_candidate` | obj? | 软召回 top1 |
| `match` | {passed, score, reason}? | 同一性判断 |
| `last_observation` | {tool, ok, preview, artifact_refs?} | 最近工具观察 |
| `critique` | {satisfied, score, issues[], next_hint?} | 自研/绘图终判 |
| `internal_draw_ok` | bool? | 绘图工具内循环是否通过（双保险之一） |

### 交付与护栏

| 字段 | 类型 | 说明 |
|------|------|------|
| `answer_draft` | str | 待交付正文 |
| `trust_level` | authoritative\|ai_reference | |
| `trust_label` | str | 展示角标 |
| `images` | str[] | |
| `stop_reason` | str? | timeout / repeat_action / quota / max_rounds… |
| `trace` | TraceEvent[] | 完整轨迹（管理端） |
| `status_log` | str[] | 学生步骤条文案 |

### 记忆句柄（不把大段历史塞进每步 prompt）

| 字段 | 类型 | 说明 |
|------|------|------|
| `memory_brief` | str? | 本回合注入的短期摘要+长期摘录（截断） |
| `profile_snapshot` | obj? | 可选：调用长期/学情工具后的只读快照 |

## A4. TraceEvent（管理端可观测）

```text
{ ts, phase, event: think|act|observe|judge|guard|deliver,
  summary, tool?, args_digest?, observation_digest?,
  scores?: {retrieval?, match?, critique?, validate?},
  autonomous_round? }
```

学生端只消费 `status_log` / SSE `status`；管理端查 `trace` 全量。

## A5. 护栏与 phase 的关系

| 护栏 | 效果 |
|------|------|
| `autonomous_round > 3` | 禁止再进入 `awaiting_tool`，→ `delivered_degraded` |
| 墙钟/空闲超时、重复动作、工具配额 | `stop_reason` + 有草稿则 degraded，无草稿则 `fused` |
| 输出循环坍缩 | 截断 `answer_draft`，不改 phase 逻辑 |

---

# B. 记忆 Schema（定稿）

## B1. 三板块总览

| 板块 | 存储 | 用途 | 谁触发 |
|------|------|------|--------|
| **短期** | **浏览器 + 服务器** 双写 | 换端可见历史；线程可恢复 | 每条消息 |
| **长期** | 服务器 Store + **Tool 读写** | 偏好、事实、易错点、笔记 | 决策者按需调工具 |
| **学情画像** | `student_profiles` 等 | 学情总览 UI | 每天 **03:00** 批跑；用户在总览点「更新」 |

无教师端；管理端不做「读学生对话」，仅可选班级聚合。

## B2. 短期记忆（跨端历史）

### 目标

换手机/换浏览器登录同一学生账号，仍能看到会话列表与消息。

### 双写策略

| 位置 | 存什么 | 说明 |
|------|--------|------|
| **服务器**（源真相） | 会话元数据 + 消息正文（或加密正文）+ Checkpointer 指针 | 跨端以服务端为准 |
| **浏览器**（缓存） | 同结构本地缓存，加速首屏 | 登录后与服务器同步；冲突以服务器 `updated_at` 为准 |

> 相对旧 ADR「原文仅 IndexedDB」：**改为服务端权威 + 本地缓存**，以满足「换端也能看历史」。摘要表仍可保留作压缩与画像原料。

### 表 / 集合建议

**`chat_threads`**

| 字段 | 说明 |
|------|------|
| `id` | thread_id |
| `user_id` | |
| `agent` | student |
| `title` | 可自动生成 |
| `created_at` / `updated_at` | |
| `archived` | bool |

**`chat_messages`**

| 字段 | 说明 |
|------|------|
| `id` | |
| `thread_id` | |
| `role` | user\|assistant\|system |
| `content` | 展示用正文 |
| `content_format` | md |
| `attachments` | [{type, url/key}] |
| `trust_label` | 助手消息可选 |
| `client_message_id` | 幂等 |
| `created_at` | |

**`agent_checkpoints`**（LangGraph Checkpointer）

- 键：`thread_id`（+ checkpoint_id）  
- 值：序列化 State（含 A3 字段）  
- 用于：同一线程多轮续跑、故障恢复；**不等于**聊天 UI 历史（UI 读 `chat_messages`）

**`memory_summaries`**（保留，隐私）

- 每 N 轮压缩；`user_id` 隔离；**仅本人 API**；供长期/学情蒸馏，管理端不可读原文。

### 同步 API（示意）

- `GET /api/student/threads`  
- `GET /api/student/threads/{id}/messages`  
- `POST` 发消息仍走 solve/stream；落库由服务端写入后，前端更新缓存  
- `POST /api/student/threads/sync` 可选：推本地未确认缓存

## B3. 长期记忆（Tool + Store）

### Tool（决策者按需）

| 工具名 | 作用 |
|--------|------|
| `memory_search` | 按 query 检索该用户长期条目 |
| `memory_upsert` | 写入/更新一条（类型见下） |
| `memory_forget` | 软删或作废（用户要求「忘掉」） |

### 条目类型（均可写）

| `kind` | 示例 |
|--------|------|
| `preference` | 回复详细度、公式偏好 |
| `fact` | 「已学完第 3 章组合逻辑」 |
| `weakness` | 「卡诺图圈法易漏」 |
| `note` | 学生自定义笔记 |
| `episodic` | 「上周错题偏好触发器时序」 |

### 表 `long_term_memories`

| 字段 | 说明 |
|------|------|
| `id` | |
| `user_id` | 隔离 |
| `kind` | 上表 |
| `text` | 自然语言内容 |
| `embedding` | 可选，向量检索 |
| `importance` | 0~1 |
| `source` | tool\|summary_distill\|manual |
| `created_at` / `updated_at` | |
| `expires_at` | 可选 |
| `active` | 软删 |

写入策略：工具调用时写；摘要任务也可**建议**条目，但默认仍由决策者 Tool 或夜间任务确认合并，避免脏写。

## B4. 学情画像（后台 + 学情总览）

### 与界面

学生端 **学情总览** 只读展示本 Schema；提供 **「更新学情」** 按钮 → 触发与夜间任务同一套 `rebuild_student_profile(user_id)`。

### 定时

- Cron：**每天 03:00**（服务器本地时区可配，默认 `Asia/Shanghai`）跑全量或增量活跃用户。  
- 手动：总览按钮 → `POST /api/student/profile/rebuild`（限流，如 1 次/10 分钟）。

### `student_profiles` 字段（在现有基础上补齐）

| 字段 | 说明 |
|------|------|
| `basics` | 年级、目标、偏好（可与长期 preference 对齐摘要） |
| `mastery` | `{concept: 0~1}` |
| `weak_points` | `[{concept, score, evidence}]` |
| `chapter_progress` | `{chapter_id: {pct, status}}` |
| `practice_stats` | 练习次数、正确率、近 7 日活跃 |
| `mistake_stats` | 错题量、Top 错因标签 |
| `knowledge_radar` | 雷达图用维度数组（总览可视化） |
| `recent_topics` | 近 14 日对话摘要主题（非原文） |
| `recommendations` | `[{type:practice\|review, label, payload}]` 总览「建议」 |
| `last_rebuild_at` | 上次画像重建 |
| `last_summary_at` | 上次对话摘要 |
| `rebuild_status` | idle\|running\|failed |
| `updated_at` | |

### 重建输入（夜间/手动共用）

1. 近期 `memory_summaries`  
2. 错题本 `mistakes`  
3. 练习记录  
4. 长期记忆中 `weakness` / `fact`  
5. （可选）知识点图覆盖率  

输出：写回 `student_profiles`，**不写对话原文**。

### 班级聚合（仅管理端可选）

- `class_rollups`：无个人对话；仅弱项分布等。  
- **无教师端 UI**；管理端运维用。

## B5. 决策者如何用记忆（编排约定）

1. 回合开始：Checkpointer 恢复 State；注入截断后的 `memory_brief`（最近摘要 + 可选 profile 一行弱项）。  
2. 规划若含长期记忆步 → 调 `memory_search` / `memory_upsert`。  
3. **不**在实时链路做完整画像重建；重建只走 03:00 / 总览按钮。

---

## C. 与四层映射（备忘）

| 层 | A/B 落点 |
|----|----------|
| 感知 | 写 `question_text` / `volume_hint` |
| 规划/推理 | 改 `phase` / `plan` / `match` / `critique` / `autonomous_round` |
| 编排 | 执行 steps；双写短期消息；调五类工具 |
| 护栏·可观测 | 限制 round；写 `trace` + 学生 `status_log` |

---

## D. 实现优先级（供后续开发，非本轮编码）

| 优先级 | 项 | 状态 |
|--------|-----|------|
| P0 | AgentState + phase 状态机接入 solve 流；题库第 0 段 + 自研 ≤3 | **另线**：现行以题库分支 + ReAct `recursion_limit` + `validate` 近似；`SolveState` 无完整 `phase`/`autonomous_round` |
| P0 | 聊天线程/消息服务端权威 + 前端缓存同步（换端历史） | **已落地** |
| P1 | 长期记忆三 Tool + 表 | **已落地** |
| P1 | 学情重建任务 03:00 + 总览「更新」按钮对接现有学情页 | **已落地**（重建已含 LTM） |
| P2 | 管理端 trace 查看器 | **半落地**：`/api/admin/traces` + 管理端 observe 列表/抽屉（节点与工具链）；非 SSE 级完整事件时间线 |

---

## E. 修订说明

- 短期记忆：**纠正**「仅浏览器 IndexedDB」为「**服务器权威 + 浏览器缓存**」。  
- 教师端：不进入本设计。  
- 学情：明确绑定**学生学情总览**，定时 + 手动双触发。  
