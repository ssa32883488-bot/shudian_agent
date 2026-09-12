# Digital.jar（msi_design 运行时）

本目录捆绑 [Digital](https://github.com/hneemann/Digital)（GPL-3.0）的 `Digital.jar`，供 **msi_design / 设计电路** 一键可用。

## 许可证

- 上游项目：https://github.com/hneemann/Digital  
- 许可证：**GNU GPL v3**（见上游 `LICENSE`；源码以 GitHub 仓库为准）  
- 本仓库仅再分发官方构建产物；修改/再分发须遵守 GPL-3.0。

## 查找顺序

1. 环境变量 `DIGITAL_JAR`（`.jar` 文件）或 `DIGITAL_HOME`（目录内含 `Digital.jar`）
2. **本目录** `vendor/Digital.jar`（默认已随仓库提供）
3. 邻近本机研发目录 `digital-circuit-poc/digital/Digital.jar`（可选兼容）

## Docker / 一键部署

镜像构建时 `COPY backend/app` 会带上本 jar；`DIGITAL_JAR` 默认指向：

`/app/app/tools/draw/digital_dig/vendor/Digital.jar`

无需再手动挂载。若要用自己的版本：

```bash
-e DIGITAL_JAR=/run/secrets/Digital.jar -v /host/Digital.jar:/run/secrets/Digital.jar:ro
```

Java：安装 **17+**，保证 `java` 在 `PATH`。

自检：`python -m scripts.check_draw_runtime`
