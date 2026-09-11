# Digital.jar（msi_design 运行时）

本目录用于**合法放置** [Digital](https://github.com/hneemann/Digital) 的 `Digital.jar`。

仓库**不**捆绑该 jar（体积与许可证分发策略由部署方决定）。查找顺序：

1. 环境变量 `DIGITAL_JAR`（指向 `.jar` 文件）或 `DIGITAL_HOME`（目录内含 `Digital.jar`）
2. 本文件旁：`vendor/Digital.jar`（把 jar 拷到这里即可）
3. 邻近本机研发目录 `digital-circuit-poc/digital/Digital.jar`（可选兼容）

Docker 示例：

```bash
# 构建前放入
cp /path/to/Digital.jar shudian_agent/backend/app/tools/draw/digital_dig/vendor/

# 或运行时挂载
-e DIGITAL_JAR=/run/secrets/Digital.jar -v /host/Digital.jar:/run/secrets/Digital.jar:ro
```

Java：安装 **17+**，设 `JAVA_HOME` 或保证 `java` 在 `PATH`。

自检：`python -m scripts.check_draw_runtime`
