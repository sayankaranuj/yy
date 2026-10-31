# AgentSec AI — setup_structure.ps1
<#
Idempotent setup script to create the exact Phase 0 folder structure and
placeholder files. This script will NOT overwrite existing files; it only
creates files and directories that are missing.

Run from the repository root:
  .\setup_structure.ps1
#>

Param()

$root = Get-Location

function Ensure-Dir([string]$path) {
    if (-Not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

function Ensure-File([string]$path, [string]$placeholder) {
    if (-Not (Test-Path $path)) {
        New-Item -ItemType File -Path $path -Force | Out-Null
        Set-Content -Path $path -Value $placeholder -Encoding UTF8
    }
}

Write-Host "Creating folders and placeholder files (no overwrites)"

# Backend tree
Ensure-Dir "$root\backend"
Ensure-File "$root\backend\main.py" "# AgentSec AI — main.py"

Ensure-Dir "$root\backend\config"
Ensure-File "$root\backend\config\__init__.py" "# AgentSec AI — config/__init__.py"
Ensure-File "$root\backend\config\settings.py" "# AgentSec AI — config/settings.py"
Ensure-File "$root\backend\config\database.py" "# AgentSec AI — config/database.py"

Ensure-Dir "$root\backend\models"
@(
    'base.py','organization.py','domain.py','subdomain.py','host.py','port.py',
    'service.py','technology.py','endpoint.py','finding.py','task.py','plugin.py',
    'result.py','scan.py','user.py'
) | ForEach-Object {
    Ensure-File "$root\backend\models\$_" "# AgentSec AI — models/$_"
}
Ensure-File "$root\backend\models\__init__.py" "# AgentSec AI — models/__init__.py"

Ensure-Dir "$root\backend\api"
@('router.py','auth.py','scans.py','assets.py','findings.py','reports.py','websocket.py') | ForEach-Object {
    Ensure-File "$root\backend\api\$_" "# AgentSec AI — api/$_"
}
Ensure-File "$root\backend\api\__init__.py" "# AgentSec AI — api/__init__.py"

Ensure-Dir "$root\backend\orchestrator"
@('orchestrator.py','decision_engine.py','event_bus.py','fallback_manager.py','state_machine.py') | ForEach-Object {
    Ensure-File "$root\backend\orchestrator\$_" "# AgentSec AI — orchestrator/$_"
}
Ensure-File "$root\backend\orchestrator\__init__.py" "# AgentSec AI — orchestrator/__init__.py"

Ensure-Dir "$root\backend\workers"
@('celery_app.py','recon_agent.py','enum_agent.py','vuln_agent.py','secret_agent.py','exploit_agent.py','report_agent.py') | ForEach-Object {
    Ensure-File "$root\backend\workers\$_" "# AgentSec AI — workers/$_"
}
Ensure-File "$root\backend\workers\__init__.py" "# AgentSec AI — workers/__init__.py"

Ensure-Dir "$root\backend\plugins"
@(
    'base_plugin.py','subfinder.py','amass.py','assetfinder.py','findomain.py','dnsx.py','httpx_plugin.py',
    'naabu.py','rustscan.py','nmap_plugin.py','whatweb.py','katana.py','waybackurls.py','gau.py',
    'nuclei_plugin.py','sqlmap_plugin.py','dalfox.py','jwt_tool.py','corsy.py','tplmap.py','subjack.py',
    'trufflehog.py','gitleaks.py','secretfinder.py','linkfinder.py','s3scanner.py','cloud_enum.py','wpscan_plugin.py','ffuf_plugin.py','scrapegraph_plugin.py'
) | ForEach-Object {
    Ensure-File "$root\backend\plugins\$_" "# AgentSec AI — plugins/$_"
}
Ensure-File "$root\backend\plugins\__init__.py" "# AgentSec AI — plugins/__init__.py"

Ensure-Dir "$root\backend\reports"
@('pdf_generator.py','report_builder.py','owasp_mapper.py') | ForEach-Object {
    Ensure-File "$root\backend\reports\$_" "# AgentSec AI — reports/$_"
}
Ensure-File "$root\backend\reports\__init__.py" "# AgentSec AI — reports/__init__.py"

Ensure-Dir "$root\backend\utils"
@('logger.py','validators.py','helpers.py') | ForEach-Object {
    Ensure-File "$root\backend\utils\$_" "# AgentSec AI — utils/$_"
}
Ensure-File "$root\backend\utils\__init__.py" "# AgentSec AI — utils/__init__.py"

# Frontend and tools
Ensure-Dir "$root\frontend"
Ensure-File "$root\frontend\.gitkeep" ""

Ensure-Dir "$root\tools"
Ensure-File "$root\tools\.gitkeep" ""

# Docker
Ensure-Dir "$root\docker"
Ensure-File "$root\docker\Dockerfile.backend" "# AgentSec AI — Dockerfile.backend"
Ensure-File "$root\docker\Dockerfile.worker" "# AgentSec AI — Dockerfile.worker"
Ensure-File "$root\docker\nginx.conf" "# AgentSec AI — nginx.conf"

# Top level files
Ensure-File "$root\.env" "# AgentSec AI — .env"
Ensure-File "$root\.env.example" "# AgentSec AI — .env.example"
Ensure-File "$root\.gitignore" "# AgentSec AI — .gitignore"
Ensure-File "$root\docker-compose.yml" "# AgentSec AI — docker-compose.yml"
Ensure-File "$root\requirements.txt" "# AgentSec AI — requirements.txt"

Write-Host "Setup complete. Created missing files and folders." 
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

$directories = @(
    "backend",
    "backend/config",
    "backend/models",
    "backend/api",
    "backend/orchestrator",
    "backend/workers",
    "backend/plugins",
    "backend/reports",
    "backend/utils",
    "frontend",
    "tools",
    "docker"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $root $dir
    New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
}

$files = @(
    "backend/main.py",
    "backend/config/__init__.py",
    "backend/config/settings.py",
    "backend/config/database.py",
    "backend/models/__init__.py",
    "backend/models/base.py",
    "backend/models/organization.py",
    "backend/models/domain.py",
    "backend/models/subdomain.py",
    "backend/models/host.py",
    "backend/models/port.py",
    "backend/models/service.py",
    "backend/models/technology.py",
    "backend/models/endpoint.py",
    "backend/models/finding.py",
    "backend/models/task.py",
    "backend/models/result.py",
    "backend/models/plugin.py",
    "backend/models/scan.py",
    "backend/models/user.py",
    "backend/api/__init__.py",
    "backend/api/router.py",
    "backend/api/auth.py",
    "backend/api/scans.py",
    "backend/api/assets.py",
    "backend/api/findings.py",
    "backend/api/reports.py",
    "backend/api/websocket.py",
    "backend/orchestrator/__init__.py",
    "backend/orchestrator/orchestrator.py",
    "backend/orchestrator/decision_engine.py",
    "backend/orchestrator/event_bus.py",
    "backend/orchestrator/fallback_manager.py",
    "backend/orchestrator/state_machine.py",
    "backend/workers/__init__.py",
    "backend/workers/celery_app.py",
    "backend/workers/recon_agent.py",
    "backend/workers/enum_agent.py",
    "backend/workers/vuln_agent.py",
    "backend/workers/secret_agent.py",
    "backend/workers/exploit_agent.py",
    "backend/workers/report_agent.py",
    "backend/plugins/__init__.py",
    "backend/plugins/base_plugin.py",
    "backend/plugins/subfinder.py",
    "backend/plugins/amass.py",
    "backend/plugins/assetfinder.py",
    "backend/plugins/findomain.py",
    "backend/plugins/dnsx.py",
    "backend/plugins/httpx_plugin.py",
    "backend/plugins/naabu.py",
    "backend/plugins/rustscan.py",
    "backend/plugins/nmap_plugin.py",
    "backend/plugins/whatweb.py",
    "backend/plugins/katana.py",
    "backend/plugins/waybackurls.py",
    "backend/plugins/gau.py",
    "backend/plugins/nuclei_plugin.py",
    "backend/plugins/sqlmap_plugin.py",
    "backend/plugins/dalfox.py",
    "backend/plugins/jwt_tool.py",
    "backend/plugins/corsy.py",
    "backend/plugins/tplmap.py",
    "backend/plugins/subjack.py",
    "backend/plugins/trufflehog.py",
    "backend/plugins/gitleaks.py",
    "backend/plugins/secretfinder.py",
    "backend/plugins/linkfinder.py",
    "backend/plugins/s3scanner.py",
    "backend/plugins/cloud_enum.py",
    "backend/plugins/wpscan_plugin.py",
    "backend/plugins/ffuf_plugin.py",
    "backend/plugins/scrapegraph_plugin.py",
    "backend/reports/__init__.py",
    "backend/reports/pdf_generator.py",
    "backend/reports/report_builder.py",
    "backend/reports/owasp_mapper.py",
    "backend/utils/__init__.py",
    "backend/utils/logger.py",
    "backend/utils/validators.py",
    "backend/utils/helpers.py",
    "frontend/.gitkeep",
    "tools/.gitkeep",
    "docker/Dockerfile.backend",
    "docker/Dockerfile.worker",
    "docker/nginx.conf",
    "docker-compose.yml",
    ".env",
    ".env.example",
    ".gitignore",
    "requirements.txt"
)

foreach ($file in $files) {
    $fullPath = Join-Path $root $file
    New-Item -ItemType File -Path $fullPath -Force | Out-Null
}

foreach ($file in $files | Where-Object { $_ -like "*.py" }) {
    $fullPath = Join-Path $root $file
    Set-Content -Path $fullPath -Value "# AgentSec AI — $file" -NoNewline
}

Write-Host "AgentSec AI structure created successfully."
