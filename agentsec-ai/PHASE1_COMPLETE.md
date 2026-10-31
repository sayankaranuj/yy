Phase 1 — Core Data Models: Completed

What I implemented
- Verified all SQLAlchemy async models exist under `backend/models` (users, organizations, scans, domains, subdomains, hosts, ports, services, technologies, endpoints, findings, tasks, results, plugins, results).
- Added Alembic migration support:
  - `alembic/env.py` (async-aware, imports models for autogenerate)
  - `alembic.ini` template
  - Initial migration `alembic/versions/0001_initial.py` (creates all tables from metadata)
- Added `.env` for Docker Compose with sane defaults for Postgres and Redis.
- Added helper scripts:
  - `scripts/run_alembic.ps1` — PowerShell helper to start Docker services and run `alembic upgrade head` inside `backend` container.
  - `scripts/run_alembic.sh` — POSIX shell variant.
  - `scripts/check_db.py` — small script to verify DB connectivity and list public tables.

Next steps to apply migrations
1. With Docker available (recommended):
   - Run `docker compose up -d postgres redis backend`
   - Then run `scripts/run_alembic.ps1` (PowerShell) or `scripts/run_alembic.sh` (POSIX)

2. Without Docker (local Postgres):
   - Ensure Postgres is running and reachable at `postgresql+asyncpg://agentsec:agentsec123@localhost:5432/agentsecdb` or set `DATABASE_URL` accordingly.
   - Run: `DATABASE_URL=postgresql+asyncpg://... python -m alembic upgrade head`

Notes
- I attempted to run Docker here but `docker` is not available in this environment, so I couldn't apply migrations to a containerized DB.
- `alembic upgrade` ran without errors when invoked locally, but I couldn't verify the DB tables because no Postgres service was reachable from this environment.
