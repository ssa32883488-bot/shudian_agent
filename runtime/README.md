# 绘图运行时（发布树）

Agent 出图依赖的 Node workbench，已从仓库根 `_archive/` **收进本目录**，便于本机 / Docker / 第三方复现。

| 目录 | 图类 | 入口脚本 |
|------|------|----------|
| `netlist_workbench/` | `logic_dag` | `scripts/render_ir.mjs` |
| `schematex_workbench/` | `timing_wave` / `state_machine` | `scripts/render_wave_ir.mjs` · `render_state_ir.mjs` |

## 首次安装依赖

```bash
cd netlist_workbench && npm ci
cd ../schematex_workbench && npm ci
```

`node_modules` 不进 Git（见本目录 `.gitignore`）。

## 环境变量

| 变量 | 作用 |
|------|------|
| `DRAW_RUNTIME_ROOT` | 覆盖本目录路径（Docker 内一般为 `/app/runtime`） |
| `NODE_BIN` | node 可执行文件，默认 `node` |
| `DIGITAL_JAR` / `JAVA_HOME` | `msi_design`（见 `backend/app/tools/draw/digital_dig/vendor/README.md`） |

查找顺序：`DRAW_RUNTIME_ROOT` → `shudian_agent/runtime/` → 仓库根 `_archive/`（本机兼容）。

自检：

```bash
cd shudian_agent/backend
python -m scripts.check_draw_runtime
```
