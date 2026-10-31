# AgentSec AI Completion Guide

Use these steps from PowerShell in `C:\FoundFirst\agentsec-ai`.

## 1. Prepare the environment

1. Install Docker Desktop, Python 3.11+, Node.js, and npm.
2. Confirm they are available:

```powershell
docker --version
python --version
node --version
npm --version


PS C:\Users\parth> docker --version
Docker version 29.8.1, build 4a63305
PS C:\Users\parth> python --version
Python 3.13.9
PS C:\Users\parth> node --version
v22.21.0
PS C:\Users\parth> npm --version
10.9.4
PS C:\Users\parth>


```

Docker Desktop must be running with the Linux engine enabled. Verify it before
starting the stack:

```powershell
docker info
```

3. Keep only one copy of each setting in `.env`. For Docker Compose, use these values:

```dotenv
POSTGRES_HOST=postgres
DATABASE_URL=postgresql+asyncpg://agentsec:agentsec123@postgres:5432/agentsecdb
REDIS_HOST=redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

4. Replace development secrets before production use. Keep `.env` private and do not commit it.

## 2. Start PostgreSQL, Redis, backend, and workers

```powershell
docker compose up --build -d
docker compose ps
```

All services should become `running` or `healthy`. Check logs if needed:

```powershell
docker compose logs -f backend
docker compose logs -f worker_recon
```

## 3. Create or update the database schema

Run the Alembic migration inside the backend container:

```powershell
docker compose exec backend alembic upgrade head
```

Check PostgreSQL connectivity:

```powershell
docker compose exec postgres pg_isready -U agentsec -d agentsecdb
```

Verify the backend can reach PostgreSQL through the application:

```powershell
Invoke-RestMethod http://localhost:8000/health/ready
```

This endpoint returns HTTP 503 when PostgreSQL is unavailable or the configured
credentials are invalid. `/health` is only a process liveness check.

Note: the current scan API still uses JSON stores for scan and workflow records. PostgreSQL is configured and migrated, but it must be connected to the scan repositories before it becomes the production source of truth.

## 4. Start the frontend

The frontend is not a Compose service, so run it separately:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

The frontend proxy sends `/api` requests to the backend at `http://localhost:8000`.

## 5. Verify the scan operation

1. Open the frontend.
2. Go to the Scans view.
3. Create a scan using an authorized public target, for example `example.com`.
4. Confirm that the scan appears with a queued/completed status.
5. Confirm that workflow steps, findings, reports, and dashboard counts update.
6. Check worker activity in the terminal or Flower at `http://localhost:5555`.

API checks:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/api/scans
Invoke-RestMethod -Method Post http://localhost:8000/api/scans `
  -ContentType 'application/json' `
  -Body '{"name":"Manual verification","target":"example.com"}'
```

Only scan systems for which you have explicit authorization.

## 6. Configure real scanning tools

Before treating results as real security findings, verify that the worker image contains and can execute the configured tools:

```powershell
docker compose exec worker_recon sh -lc "command -v subfinder; command -v amass; command -v httpx"
docker compose exec worker_vuln sh -lc "command -v nuclei; command -v nmap; command -v naabu"
```

Set valid AI keys only if AI or Strix analysis is enabled. Keep `STRIX_AGENT_ENABLED=false` until scope, budget, and tool permissions are confirmed.

The current Phase 0 workflow completes quickly for UI and API verification. Replace that behavior with the real queued worker lifecycle before production use, including progress updates, failure handling, cancellation, and persisted results.

## 7. Run the final checks

From the project root:

```powershell
python -m pytest -q
Set-Location frontend
npm test -- --run
npm run build
```

Stop the stack when finished:

```powershell
Set-Location ..
docker compose down
```

Use `docker compose down -v` only when you intentionally want to delete PostgreSQL and Redis data volumes.

## Completion checklist

- [ ] `.env` has no duplicate or conflicting values.
- [ ] Docker services are healthy.
- [ ] `http://localhost:8000/health/ready` reports `{"status":"ready","database":"ok"}`.
- [ ] Alembic migrations complete successfully.
- [ ] Frontend loads and can create a scan.
- [ ] Backend, workers, and Redis process the scan.
- [ ] PostgreSQL-backed repositories replace JSON storage for production.
- [ ] Real scanning tools are installed and tested on authorized targets.
- [ ] Backend tests, frontend tests, and frontend build pass.