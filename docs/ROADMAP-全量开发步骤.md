---
type: project-doc
project: 单学科教育智能体
title: 全量开发步骤路线图（P1 至最终形态）
created: 2026-08-28
status: active
version: 1.0
---

# 单学科教育智能体 · 全量开发步骤路线图

> 本文件是对 `CONFIG-CURSOR.md` 的**完整版展开**：从 P1 一直到产品最终形态的所有开发步骤、数据模型、API、前端演进、验收标准与风险。
> 最高准则仍是 `宪法文档-单学科教育智能体.md`（尤其附录 B 的 ADR）。任何冲突以宪法为准。
> 节奏：**先把产品搓出来**，每阶段都要"可运行、可演示、可反馈"。

---

# Part 0 · 覆盖全生命周期的一张表

| 阶段 | 主题 | 核心能力 | 里程碑验收 | 可演示产出 |
|------|------|----------|-----------|-----------|
| **P1** | 学生解题闭环 | 发消息/拍照→搜题→解题→回流 | 学生能拿到搜题/解题答案，回流问答表有数据 | 对话窗口 + 搜题/解题一条龙 |
| **P2** | 错题本 + 学情画像 | 错题增删改查/导入/导出Word + 画像写入 | 学生能维护错题本，画像自动记录 | 错题本页面 + 画像可视化 |
| **P3** | 教师端考务 | 组卷→发布→判卷→改判→洞察 + 题库维护 | 教师能完整走一遍发卷/判卷/看数据 | 教考务悬浮球 + 试卷/成绩/报告页 |
| **P4** | 自主学 + 回流审核 | 讲课答疑/路径推荐/个性化 + 回流审核界面 | 学生有完整自学体验；教师能审回流 | 学习路径页 + 回流审核页 |
| **P5** | 部署容器化 | Docker Compose 编排生产形态 | 一键可部署到服务器 | 部署文档 + compose 配置 |

---

# Part 1 · P1 学生解题闭环（MVP 第一步）

## 1.1 目标
学生能：发文字或拍照，拿到"命中题库的权威答案"或"AI 解题（标注仅供参考）"，未命中且校验通过的可回流到回流问答表。

## 1.2 后端关键实现
1. 初始化 FastAPI 项目骨架（`backend/`）。
2. LangGraph 建 **解题图（solve_graph）**：
   - 节点：输入归一 → OCR/文本识别 → 题库检索 → 命中判断 → (命中)权威答案 / (未命中)AI解题 → 权威校验 → 回流写入
   - 条件边：命中?；校验达标?
3. 数据模型（PostgreSQL，P1）：
   - `question_bank`（正式题库）：id, content, answer,解析, knowledge_tags, source, status
   - `reflow_queue`（回流问答表）：id, question, ai_answer, validate_status, source, created_at
4. 模型接入：
   - MiMo 封装（LLM 生成、OCR 识图）——占位 + 可切换
   - 本地 BGE-M3 Embedding + bge-reranker-v2-m3 Rerank 服务
   - ChromaDB 向量库（离线入库由 data/ 脚本完成）
5. API：
   - `POST /api/student/solve`（文字/图片）
   - `GET /api/student/search`（搜题）

## 1.3 前端关键实现
- Vue3 项目初始化（frontend/）。
- **助学对话窗口**：输入框（文字+图片上传）、消息列表、Markdown+KaTeX 渲染、"AI解答仅供参考"角标。
- 基础登录/用户态（占位）。

## 1.4 P1 验收标准
- [ ] 文字提问能拿到搜题/解题结果
- [ ] 拍照能识别题目并走同一条解题流程
- [ ] 未命中进 AI 解题并标注"仅供参考"
- [ ] 校验达标进回流问答表（手动/自动模式均生效）
- [ ] 全程有日志，可回溯

## 1.5 P1 数据可用真实少量数据
- 手工录入 30-50 道数电题（含选择/填空/简答）到题库，打通链路即可，不追求规模。

---

# Part 2 · P2 错题本 + 学情画像

## 2.1 目标
学生能维护个人错题本；系统能自动记录学情画像（聚合：掌握度/错题/轨迹）。

## 2.2 后端
- 数据模型新增：
  - `mistakes`（错题本）：id, student_id, question_id/snapshot, reason, add_source(手动/考试导入), added_at, deleted_at
  - `student_profiles`（聚合画像）：student_id, 基础信息, 各知识点掌握度(JSON), 练习频率/时长(聚合), updated_at
  - `learning_events`（可选的轻量事件，仅聚合用增量）——按宪法只存聚合，不存流水
- 工具（第6章 6.5）：`mistake_*` 全套 + `read/update_profile`
- 对接：考试结果一键导入错题本

## 2.3 前端
- **错题本页面**：列表（筛选）、增删改、一键导入入口、"导出错题 Word"按钮
- **学情/画像可视化**：知识点掌握度雷达图（ECharts）、练习趋势

## 2.4 验收
- [ ] 学生能查/增/删/改错题
- [ ] 考试后可一键把错题导入错题本
- [ ] 能导出错题 Word 文件
- [ ] 画像自动记录并能展示个人掌握度

---

# Part 3 · P3 教师端考务（核心重头）

> 依赖前置：P1 题库、P2 判卷数据承载。P3 是"考"的闭环，涉及状态机与权限。

## 3.1 教师端考务 Agent（悬浮球）
- 右边下角悬浮球，点开一个对话窗口（历史可回看）。
- 内部按需路由：组卷 / 判卷 / 改判 / 洞察。

## 3.2 后端
- 数据模型新增：
  - `papers`（试卷）：id, teacher_id, title, config(题型/难度/范围/规模), status(草稿/已发布/收卷/判卷中/已判完), created_at
  - `paper_questions`：paper_id, question_id, order_no, score, type
  - `exams`（某次考试实例，绑定班级）：paper_id, class_id, status, start/end_time
  - `answers`（学生作答）：exam_id, paper_question_id, student_id, answer_text/image, ai_score, ai_comment, teacher_revised_score, revised
  - `grades`（总成绩/每卷）：exam_student汇总
  - `class_reports`（学情报告缓存）：report_id, scope(paper/class), content/json, generated_at
- **状态机**（宪法 7.5 强制）：
  - 草稿→已发布→收卷→判卷中→已判完（→可洞察/改判）
  - 未收卷不可判卷；未判完不可洞察
- API：
  - 组卷：`POST /api/teacher/paper/generate`（参数确认→组卷）
  - 发布：`POST /api/teacher/paper/{id}/publish`
  - 判卷：`POST /api/teacher/exam/{id}/grade`（异步 Celery）
  - 改判：`PUT /api/teacher/answer/{id}/revise`
  - 洞察：`GET /api/teacher/report/{paper_id or class_id}`
  - 题库维护：`/api/teacher/bank/*`（增删改查/批量导入导出）

## 3.3 前端
- **试卷管理页**：列表、状态标签、新建/编辑/发布/收卷、链接跳转
- **班级成绩页**：按班看成绩分布（ECharts）
- **学情报告页**：共性薄弱点、归因、建议（按次或按课程）
- **题库管理页**：教师 CRUD/批量导入导出；学生只读视图

## 3.4 验收
- [ ] 教师组卷（问答确认参数，规模≤20/简答≤5）→ 试卷入库
- [ ] 发布→学生作答（传图/打字）→收卷
- [ ] 判卷（异步）→ 原始判卷结果
- [ ] 教师抽检改判（客观/主观）
- [ ] 洞察报告（按次 + 按课程）可生成、可导出
- [ ] 状态机约束生效（未收卷不能判、未判完不能洞察）
- [ ] 权限：教师可见学情+判卷，不见学生对话隐私；学生见自己判卷

---

# Part 4 · P4 自主学 + 回流审核

## 4.1 目标
补齐"讲、荐、个性化"自主学习体验；教师能审核回流问答表。

## 4.2 后端
- 讲课答疑（W1）：RAG 多路检索+Rerank→回答
- 学习路径推荐（W4）：知识图谱查询前置依赖
- 个性化推荐（W6）：读画像→定薄弱→推题/提醒
- **回流审核**：
  - `POST /api/teacher/reflow/list`（待审列表）
  - `POST /api/teacher/reflow/{id}/approve`（入正式题库）
  - `POST /api/teacher/reflow/{id}/reject`
- 知识图谱在 P4 正式接查询（P4 前已在 data/ 建好）

## 4.3 前端
- **学习路径页**（前置依赖可视化）
- **回流审核页**（教师审阅候选问答对，勾选入库/驳回）
- 个性化推荐卡片（弱项推题）

## 4.4 验收
- [ ] 讲课答疑有据（引课本+图）
- [ ] 能推荐学习路径（图谱）
- [ ] 能按画像推题/提醒
- [ ] 教师能审回流，选择性入库

---

# Part 5 · P5 部署容器化（生产形态）

## 5.1 目标
将本地 Demo 编排成可部署形态。

## 5.2 实施
- 写通 `Dockerfile`（后端；前端 Nginx 静态）
- 写 `docker-compose.yml`：backend + frontend + postgres + redis + chroma + neo4j + minio
- 数据初始化脚本（建表/迁移 Alembic/离线数据导入）
- 环境变量化（模型 API Key、数据库连接等）
- 部署文档（本机/服务器一键起）

## 5.3 验收
- [ ] `docker-compose up` 一条命令全链路可跑
- [ ] 无硬编码密钥（全部环境变量）
- [ ] 数据可迁移、可备份

---

# Part 6 · 数据模型演进总表（PostgreSQL 全表规划）

| 表 | 阶段 | 说明 |
|----|------|------|
| users | P1 | 学生/教师角色 |
| question_bank | P1 | 正式题库 |
| reflow_queue | P1 | 回流问答表（待审）|
| student_profiles | P2 | 聚合画像 |
| mistakes | P2 | 错题本 |
| papers | P3 | 试卷 |
| paper_questions | P3 | 试卷-题目 |
| exams | P3 | 某次考试实例 |
| answers | P3 | 学生作答+判卷+改判 |
| grades | P3 | 成绩汇总 |
| class_reports | P3 | 学情报告 |
| chat_history | P3/4 | 对话记录（短期/召回）|

> 学情只存**聚合**（宪法 ADR-8），不存原始作答流水。

# Part 7 · API 清单演进总表

| 域 | 阶段 | 端点 |
|----|------|------|
| 学生·解题 | P1 | POST /api/student/solve, GET /api/student/search |
| 学生·错题 | P2 | /api/student/mistakes/*(CRUD/import/export-word) |
| 学生·画像 | P2 | GET /api/student/profile |
| 学生·路径/荐 | P4 | /api/student/path, /api/student/recommend |
| 教师·组卷 | P3 | POST /api/teacher/paper/generate |
| 教师·发布/考务 | P3 | /api/teacher/paper/*, /api/teacher/exam/*, grade, revise |
| 教师·洞察 | P3 | /api/teacher/report/* |
| 教师·题库 | P3 | /api/teacher/bank/* |
| 教师·回流 | P4 | /api/teacher/reflow/* |
| 教师·对话 | P3 | 考务悬浮球会话 |

# Part 8 · 前端页面清单演进

| 页面 | 阶段 | 说明 |
|------|------|------|
| 助学对话窗 | P1 | 学生主交互 |
| 登录/用户态 | P1 | 占位 |
| 错题本 | P2 | 学生 |
| 画像可视 | P2 | 学生（雷达图/趋势）|
| 试卷管理 | P3 | 教师 |
| 班级成绩 | P3 | 教师（分布）|
| 学情报告 | P3 | 教师（薄弱/归因）|
| 题库管理 | P3 | 教师（CRUD/导入导出）|
| 学习路径 | P4 | 学生（图谱）|
| 回流审核 | P4 | 教师 |
| 个性化推荐 | P4 | 学生 |

# Part 9 · 模型接入清单

| 能力 | 模型 | 阶段接入 | 是否本地 |
|------|------|----------|----------|
| 通用 LLM | MiMo 云端 | P1 | 否 |
| OCR 识图 | MiMo 云端 | P1 | 否 |
| Embedding | BGE-M3 本地 | P1 | 是 |
| Rerank | bge-reranker-v2-m3 本地 | P1 | 是 |

# Part 10 · 测试与上线节奏
- **P1/P2 阶段**：手动冒烟测试为主，每个闭环跑通即可。
- **P3 阶段**：由于涉及判卷/成绩，引入**最小验收测试**（状态机、改判、权限）。
- **P4 阶段**：补自动化回归（宪法第8章暂缓，但 P4 后需提上日程）。
- **P5 阶段**：正式部署，再谈监控（第10章）。

# Part 11 · 风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| MiMo 工具调用不稳定 | P1 解题/组卷异常 | MiMo 封装设超时/重试；关键步骤降级为"简单提示词+固定流程" |
| 判卷准确率不足 | 教师不信任 | AI 先判 + 教师可改判；P3 判卷多做"不确定标注" |
| 回流自动灌入垃圾题 | 题库质量下降 | 默认手动入库（回流表审核）；自动入库仅限教师开启 |
| 学情只存聚合丢失细节 | 个性化精度受限 | 聚合采用"细分知识点+多档掌握度"尽量保留信息 |
| 本地 BGE 资源占用 | 拖慢 Demo | P1 可先用小模型/降维；正式化再上 BGE-M3 全量 |
| 状态机被绕过 | 判卷/洞察乱序 | 后端强校验，前端 UI 不展示未授权入口 |

---

# Part 12 · 阶段验收 checklist（总）

- [ ] **P1**：搜题/解题一条龙 + 回流表有数据
- [ ] **P2**：错题本全套 + 画像记录
- [ ] **P3**：组卷→发布→判卷→改判→洞察 全链路 + 题库维护 + 权限/状态机
- [ ] **P4**：讲课/路径/个性化 + 回流审核
- [ ] **P5**：Docker 一键部署

---
# 结束语
按本路线图滚动推进，每阶段结束回到 `CONFIG-CURSOR.md` 与宪法确认没有漂移，再进入下一阶段。重大分歧先问人类。