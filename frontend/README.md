# 数电助学 · 前端（P1）

Vue 3 + Vite + Element Plus + Pinia + Vue Router + Axios + KaTeX。

## 启动

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173/ ，先填学生 ID 进入 `/chat`。

开发代理：`/api` → `http://127.0.0.1:8000`（见 `.env.development` / `vite.config.ts`）。

## 联调

后端需实现 `POST /api/student/solve`。前端适配层同时兼容：

- 任务约定：`source: answer_bank|ai_solve`，请求字段 `image`
- 当前后端 Schema：`trust_level: authoritative|ai_reference`，请求字段 `image_base64`

详见 `src/api/adapters/solve.ts`。
