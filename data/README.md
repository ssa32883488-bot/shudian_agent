# 离线数据准备

## 1. 教材图片 → MinIO

先启动 MinIO（在 `docker/`）：

```bash
cd docker
docker compose up -d minio minio-init
```

控制台：http://127.0.0.1:9001 （`minioadmin` / `minioadmin`）  
API：http://127.0.0.1:9000  
Bucket：`shudian-textbook`（匿名可读，便于前端插图）

上传正文 + 学习辅导图片：

```bash
# 在 shudian_agent 根目录；可先 dry-run
python data/upload_textbook_images.py --dry-run
python data/upload_textbook_images.py
```

对象键：`chapters/<hash>.jpg`、`guide/<hash>.jpg`  
公网 URL：`{MEDIA_BASE_URL}/{object_key}`  
（默认 `http://127.0.0.1:9000/shudian-textbook/...`，上线改 `MEDIA_BASE_URL` 为域名即可）

## 2. Canonical chunks → ChromaDB（RAG）

```bash
# 确认 backend/.env 中 MEDIA_BASE_URL 与 MinIO 一致
python data/ingest_canonical.py --dry-run
python data/ingest_canonical.py --reset
# 或只灌部分章：python data/ingest_canonical.py --chapters 3 4
```

写入 `backend/data/chroma` 集合 `textbook_chunks`，`media_urls` 已换成可访问 URL。  
供 `POST /api/student/lecture` 检索。

旧样例入口仍可用：

```bash
python data/ingest_textbook.py
```

## 3. 知识图谱

```bash
python data/ingest_graph.py
```

写入 `backend/data/knowledge_graph.json`，供 `GET /api/student/path` 前置依赖查询。

## 4. 题库样例

```bash
cd backend
python -m scripts.seed_questions
python -m scripts.seed_teacher
```

## 4.1 课本题库灌入（章末习题 + 课文例题 → question_bank）

把 canonical 中的章末习题（`exercise_merged`，约 227）与课文例题（`example`，约 82）写入正式题库，知识点来自 `knowledge_graph_v0.2.json` 的 TESTS 边，并同步 Chroma 集合 `question_bank`。

前置：`backend/.env` 中 `DATABASE_URL`、`MEDIA_BASE_URL`、`CHROMA_PERSIST_DIR` 已配置；教材图可走 MinIO 或后端 `/media` 回退（本机 `MEDIA_BASE_URL=http://127.0.0.1:8000/media` 时需先启动 backend，浏览器才能打开配图）。

```bash
# 在 shudian_agent 根目录
# 1) 可选：上传图片到 MinIO
python data/upload_textbook_images.py --dry-run
python data/upload_textbook_images.py

# 2) dry-run 校验（不写库）
python data/ingest_textbook_question_bank.py --dry-run --report reports/qb_dryrun.json

# 3) 全量灌入（章末习题+例题；仅清除 source 以「课本·」开头的旧题）
python data/ingest_textbook_question_bank.py --reset-qb --report reports/qb_ingest.json

# 只灌例题 / 只灌章末题：
# python data/ingest_textbook_question_bank.py --kinds example --report reports/qb_examples_ingest.json
# python data/ingest_textbook_question_bank.py --kinds exercise --dry-run

# 分章：python data/ingest_textbook_question_bank.py --chapters 3 4 --dry-run
```

`source` 格式：`课本·第X章·题x.y` 或 `课本·第X章·例x.y.z`；`knowledge_tags.kind` 为 `chapter_exercise` / `example`。

验收包（固定种子 `seed=20260903`）：

- `reports/qb_acceptance_sample10.md`
- `reports/qb_acceptance_sample10.json`
- `reports/qb_acceptance_sample10.html`（浏览器打开对照填表；**KaTeX 渲染公式，配图 base64 内嵌**）

仅重渲 HTML（改样式/公式渲染、不写库）：

```bash
python data/ingest_textbook_question_bank.py --render-acceptance-html
```

幂等键：`source=课本·第X章·题x.y` / `knowledge_tags.exercise_id`。重复执行会更新而非复制。

说明：若环境未安装 `sentence_transformers` / FlagEmbedding，Chroma 会用 mock 向量写入（检索演示仍可用）；安装真模型后请重跑本脚本或 `backend/scripts/reindex_chroma_real_bge.py`。

## 5. 知识图谱

```bash
# 实体
python data/extract_kg_entities.py
# TESTS（题↔知识点）
python data/build_kg_tests.py
# 前置链 PRE_REQUISITE_OF
python data/build_kg_prereqs.py
# 写入运行时
python data/ingest_graph.py
```

产物：`data/kg/knowledge_graph_v0.2.json`、`path_graph.json`；运行时 `backend/data/knowledge_graph.json`。


| 配置 | 本机 | 服务器 |
|------|------|--------|
| `MINIO_ENDPOINT` | `127.0.0.1:9000` | 内网 `minio:9000` 或对象存储地址 |
| `MEDIA_BASE_URL` | `http://127.0.0.1:9000/shudian-textbook` | `https://你的域名/...`（浏览器能打开） |
| 图片文件 | 上传一次即可 | 同 bucket；换域名只改 `MEDIA_BASE_URL` 后重新 `ingest_canonical` |
