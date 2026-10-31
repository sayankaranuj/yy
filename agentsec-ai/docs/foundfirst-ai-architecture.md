# FoundFirst AI: Architecture

## 1. Architectural style

FoundFirst AI uses a layered, asynchronous service architecture. The frontend handles presentation, the FastAPI service owns API and lifecycle concerns, Celery workers execute long-running stages, Redis coordinates work and events, and storage/reporting components preserve results for later inspection.

```text
Operator
   |
   v
React frontend
   | HTTP / WebSocket
   v
FastAPI API + auth + validation
   |                 \
   |                  \ live events
   v                   v
Workflow orchestrator -> Redis event bridge -> WebSocket client
   |
   v
Redis broker/result backend
   |
   +--> recon worker
   +--> enum worker
   +--> vulnerability worker
   +--> secrets worker
   +--> report worker
             |
             v
      Plugin executor and external tools
             |
             v
     Findings, workflow, asset stores, and reports
```

## 2. Frontend layer

The frontend is a React application built with Vite. It contains:

- Login and token handling.
- Dashboard and navigation.
- Scan creation and attack-category selection.
- Live progress and event rendering.
- Findings, reports, assets, authorization, database, and AI-status pages.
- API download helpers for JSON, CSV, Markdown, and PDF paths.

The frontend does not directly run security tools. It sends scoped requests to the backend and renders backend-provided state.

## 3. API layer

FastAPI mounts versioned and unversioned API routers. The API layer is responsible for:

- Request validation and response schemas.
- Authentication exceptions and JWT verification.
- Target authorization endpoints.
- Scan lifecycle requests.
- Findings, results, task, report, and dashboard queries.
- WebSocket connection handling.
- Health and readiness signals.

The API layer delegates long-running work instead of blocking an HTTP request on a complete scan.

## 4. Orchestration layer

The orchestration layer contains:

- State machine for lifecycle transitions.
- Decision engine for stage selection.
- Event bus for in-process events.
- Redis event bridge for live clients.
- Fallback manager for dispatch retries.
- Workflow store for queued and completed steps.

The orchestrator assigns one task ID to each queued step and preserves the relationship between a scan, task, tool, result, and finding.

## 5. Worker layer

Workers are separated by queue to isolate workload classes:

| Queue | Responsibility |
|---|---|
| `recon_queue` | Subdomain and asset discovery |
| `enum_queue` | Live hosts, ports, technologies, crawling, directories |
| `vuln_queue` | Template and application/API vulnerability checks |
| `secrets_queue` | JavaScript, Git, and cloud secret checks |
| `report_queue` | Report assembly and export |

Workers use async helpers where tool and storage operations allow it, while Celery entry points provide synchronous task adapters for the broker.

## 6. Plugin architecture

The plugin registry discovers modules under the plugin package. A plugin exposes metadata and an executable class or handler. The executor receives a typed input and returns normalized output:

- Tool name.
- Success/status.
- Exit code.
- Parsed records.
- Raw output.
- Command metadata.
- Error message.
- Timeout/unavailable state.
- Execution duration.

This contract lets the orchestrator treat different command-line tools consistently.

## 7. Data and storage

The project has two storage paths:

1. PostgreSQL configuration, SQLAlchemy engine, and Alembic migrations for the database-backed deployment foundation.
2. JSON-backed stores used by current scan, finding, and workflow paths.

This split is intentional in the current prototype but must be resolved before claims of fully transactional production persistence are made.

Reports are written under the generated-report area with sanitized target-derived names. Secret-like evidence is redacted before serialization.

## 8. Security boundaries

- Target input is validated before dispatch.
- Protected API routes require a Bearer token when JWT mode is enabled.
- Trusted hosts restrict accepted HTTP host headers.
- Authorization review separates requested targets from approved targets.
- External commands are executed through plugin abstractions rather than concatenated shell strings.
- Tool output and report evidence are redacted.
- Worker queues separate operational responsibilities.

These boundaries reduce risk but still require deployment hardening and plugin review.

## 9. Deployment topology

The Compose topology places services on a private bridge network. PostgreSQL and Redis use named volumes. The frontend is exposed on port 5173, the backend on port 8000, and Flower is bound to localhost on port 5555 in the documented local setup.

Production deployment should add TLS termination, strong secrets, restricted network exposure, image pinning, logging, backups, and centralized identity controls.

## 10. Architectural trade-offs

- Asynchronous workers keep the API responsive but add broker and queue failure modes.
- Multiple queues improve isolation but require operational monitoring.
- Plugin discovery improves extensibility but requires safe import and metadata handling.
- JSON persistence simplifies local development but limits transactional scale.
- Optional AI configuration keeps the core workflow deterministic but means AI analysis is not automatically part of every scan.

## 11. Class and module responsibilities

| Layer | Responsibility | Must not own |
|---|---|---|
| API routers | Validate requests and expose resources | Long-running subprocess orchestration |
| Settings | Parse typed configuration | Business decisions about findings |
| Orchestrator | Select stages, queue work, publish lifecycle | Tool-specific parsing |
| Workers | Coordinate stage execution | Frontend rendering |
| Plugins | Build/execute/parse one tool | Global scan lifecycle |
| Processors | Normalize and persist stage records | Authentication |
| Stores | Read/write scan and finding state | Choosing attack tools |
| Report builder | Render persisted evidence | Re-running tools |
| Frontend | Display state and collect operator input | Direct tool execution |

This separation makes it possible to replace a tool or UI without rewriting the entire system.

## 12. Sequence diagram

```text
Operator -> Frontend: enter target and scan options
Frontend -> API: create scan
API -> Validator: validate target and scope
API -> ScanStore: persist scan
API -> Orchestrator: start workflow
Orchestrator -> WorkflowStore: persist task plan
Orchestrator -> Redis: enqueue first Celery task
Redis -> ReconWorker: deliver task
ReconWorker -> PluginExecutor: run recon tools
PluginExecutor -> ReconWorker: normalized output
ReconWorker -> Processor: persist assets
ReconWorker -> EventBus: stage event
EventBus -> WebSocket: live update
ReconWorker -> Redis: continue chain
Redis -> Enum/Vuln/ReportWorkers: execute next stages
ReportWorker -> ReportBuilder: render artifacts
Frontend -> API: retrieve findings and reports
API -> Frontend: scan-scoped result
```

## 13. Reliability boundaries

There are separate failure domains:

- Browser failure affects presentation but not necessarily the task.
- API failure can prevent new work but does not necessarily stop an existing worker.
- Redis failure affects dispatch, result delivery, and live events.
- Worker failure affects one stage or queue.
- Tool failure affects one plugin execution.
- Store failure affects persistence and later reporting.

The workflow should expose which boundary failed. A generic "scan failed" message is not enough for diagnosis.

## 14. Security boundaries

The most important trust transitions are:

1. Browser input to API validation.
2. API target to subprocess argument construction.
3. External tool output to parser.
4. Parsed evidence to persistent storage.
5. Persistent evidence to report/export.
6. User identity to target approval and scan permission.

Validation, structured subprocess arguments, redaction, scan-scoped queries, and role checks must be applied at these boundaries.

## 15. Scaling model

For a larger deployment:

- Run multiple stateless API instances behind a reverse proxy.
- Use a shared PostgreSQL database as the source of truth.
- Use Redis with production persistence and monitoring.
- Scale queues independently based on stage demand.
- Store reports in controlled object storage rather than local container files.
- Add task idempotency and distributed locks.
- Centralize logs and metrics.

The current Compose file is a local or small-team topology, not a complete high-availability architecture.
