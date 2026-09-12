# 精简栈一键启动（Windows PowerShell）
# 用法：
#   cd shudian_agent\docker
#   copy .env.example .env   # 首次，并填写 DEEPSEEK_KEY
#   .\bootstrap_slim.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== 数电教育智能体 · slim 一键部署 =="

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "未找到 docker。请先安装 Docker Desktop。"
}
docker compose version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "需要 docker compose（Docker Compose V2）。"
}

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "已生成 .env（来自 .env.example）。"
    } else {
        Write-Error "缺少 .env.example"
    }
}

$line = Get-Content ".env" | Where-Object { $_ -match '^\s*DEEPSEEK_KEY=' } | Select-Object -Last 1
if (-not $line) {
    $line = Get-Content ".env" | Where-Object { $_ -match '^\s*MIMO_API_KEY=' } | Select-Object -Last 1
}
$key = ""
if ($line) {
    $key = ($line -split "=", 2)[1].Trim()
}
if ([string]::IsNullOrWhiteSpace($key) -or $key -in @("sk-xxx", "CHANGE_ME")) {
    Write-Host ""
    Write-Host "请先在 docker\.env 中填写自备的 DeepSeek API Key："
    Write-Host "  DEEPSEEK_KEY=sk-xxxxxxxx"
    Write-Host "申请：https://platform.deepseek.com/"
    Write-Host "填好后重新执行本脚本。"
    exit 1
}

Write-Host "== docker compose build & up =="
docker compose -f docker-compose.slim.yml --env-file .env up -d --build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$port = if ($env:HTTP_PORT) { $env:HTTP_PORT } else { "80" }
Write-Host ""
Write-Host "== 等待健康检查 =="
$ok = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:$port/health" -UseBasicParsing -TimeoutSec 3
        if ($r.StatusCode -eq 200) { $ok = $true; break }
    } catch { }
    Start-Sleep -Seconds 2
}

if ($ok) {
    Write-Host "OK  http://127.0.0.1:$port/  （/health 已通）"
} else {
    Write-Host "WARN: /health 暂未就绪，请查看：docker compose -f docker-compose.slim.yml logs -f"
}

Write-Host ""
Write-Host "演示账号（seed 后）：管理员 13900000001 / 123456"
Write-Host "设计电路 MSI：仓库已含 Digital.jar（vendor/）；自检 python -m scripts.check_draw_runtime"
