# FoundFirst AI: Project Features

## 1. Project overview

FoundFirst AI is an authorized security-assessment platform. It combines a React operator interface, a FastAPI backend, Celery workers, Redis messaging, PostgreSQL configuration, local workflow storage, security tools, and report generation into one controlled workflow.

The platform is designed to answer four operational questions:

1. What assets and services are exposed by an authorized target?
2. Which weaknesses are indicated by the collected evidence?
3. Which findings have enough evidence to be useful to an operator?
4. What report and remediation context should be produced for the assessment?

## 2. User and access features

- Operator login and registration endpoints.
- Optional JWT protection for API routes.
- Refresh and logout flows.
- Configurable administrator credentials through environment variables.
- Target authorization requests before an assessment is approved.
- Administrator review with approval, rejection, reviewer notes, and history.
- Trusted-host protection for the HTTP application.
- Health and readiness endpoints for operations and deployment checks.

## 3. Scan management

- Create scans with a name and target.
- Support for full, quick, reconnaissance-only, and vulnerability-only modes.
- Persist scan status, target, timestamps, progress, and task provenance.
- Cancel an active scan through the cancellation mechanism.
- Select individual attack categories instead of running the default plan.
- Keep scan results isolated by `scan_id` and `task_id`.
- Display queued, running, completed, partial, failed, and cancelled states.
- Apply target validation before persistence or worker dispatch.
- Enforce configurable concurrency, scan timeout, tool timeout, DNS resolver, and rate-limit settings.

## 4. Reconnaissance features

The reconnaissance layer uses registered plugins and can run tools such as:

- Subfinder for subdomain discovery.
- Amass as a recon fallback.
- Assetfinder, Findomain, and related enumeration plugins.
- DNSX and HTTPX-related discovery.
- Cloud enumeration where enabled.

Recon output is normalized, deduplicated, associated with the scan, and stored through processors. When a tool fails or produces unusable output, the decision and fallback components can choose an alternate tool.

## 5. Enumeration features

Enumeration builds a richer target context from recon output:

- Live-host detection.
- Port discovery through Naabu or configured port scanners.
- Nmap and RustScan plugin support where installed.
- Technology fingerprinting through WhatWeb and HTTPX metadata.
- Web crawling through Katana.
- JavaScript and endpoint discovery.
- Directory discovery with configured wordlists.
- Aggregated host, port, technology, URL, and directory statistics.
- Context-building for the vulnerability stage.

## 6. Vulnerability assessment features

The vulnerability layer contains modular checks and validation:

- Nuclei template-based checks.
- Web-application test modules.
- API-security checks.
- Authorization testing.
- CORS, SQLMap, Dalfox, TplMap, and WPScan plugin integration where configured.
- Finding validation before persistence.
- Finding severity, evidence, affected URL, confidence, remediation, CWE, and OWASP-style mapping.
- Scan/task provenance so a finding is not incorrectly attributed to another scan.
- Deduplication and structured finding processing.

## 7. Secret and repository scanning

- JavaScript secret extraction.
- Public Git repository scanning through TruffleHog.
- Cloud-security checks.
- Explicit repository authorization requirements.
- Support for branch, commit range, and baseline options.
- Baseline suppression for previously accepted repository results.
- Redaction of secret-like values before storage, display, and report output.
- No private-repository credential collection in the Git scanning flow.

## 8. Workflow and resilience

- Rule-based decision engine for selecting stages.
- Event bus for scan lifecycle and stage completion events.
- Redis event bridge for live updates.
- Celery queues separated by recon, enumeration, vulnerability, secrets, and report workloads.
- Retry configuration on worker tasks.
- Fallback manager for transient dispatch and tool failures.
- State-machine transitions for scan lifecycle.
- Cancellation checks before and during worker execution.
- Bounded WebSocket event history with expiration.

## 9. Dashboard and operator interface

The React frontend provides:

- Overview dashboard.
- Scan list and scan creation modal.
- Live scan progress and terminal-style tool output.
- Findings dashboard with severity badges.
- Reports dashboard.
- Target authorization page.
- Administrator review page.
- Public Git repository scan page.
- PostgreSQL status page.
- AI-analysis configuration status page.
- Plugin and attack-category selection.
- Activity timeline, severity breakdown, scan statistics, and recent-scan details.
- JSON, CSV, Markdown, and PDF report download paths where supported.

## 10. Reporting and evidence

The report builder produces:

- Markdown reports for human review.
- JSON report bundles for integration.
- PDF artifacts when the PDF dependency is available.
- Finding summaries and severity counts.
- OWASP-style mapping.
- Redacted evidence.
- Stage timeline, failed checks, skipped checks, reproduction guidance, and remediation fields in detailed reports.

## 11. Deployment and quality features

- Docker Compose stack for backend, frontend, PostgreSQL, Redis, workers, and Flower.
- Separate queues and worker containers.
- Environment-driven settings through `.env`.
- Alembic database migration support.
- Backend pytest suite.
- Frontend Vitest tests and production build.
- CI, dependency scanning, npm scanning, and secret scanning workflows.
- Coverage configuration and test compose configuration.

## 12. Important implementation distinction

The project exposes AI-provider configuration and an AI-analysis status page, but the current scan workflow is primarily deterministic and tool-driven. Adding an AI key alone does not activate an LLM in the scan pipeline. This distinction prevents the interface from claiming AI analysis that is not actually wired into execution.

## 13. Feature-to-component mapping

| Feature | Backend implementation area | Frontend surface | Output |
|---|---|---|---|
| Login | `backend/api/auth.py` and JWT settings | Login page | Access token/session state |
| Scan creation | `backend/api/scans.py` and storage | Scans page | Scan record and workflow |
| Target approval | `backend/api/targets.py` | Authorization/Admin pages | Approval decision and audit data |
| Recon | `backend/workers/recon_agent.py` and plugins | Live scan page | Assets and subdomains |
| Enumeration | `backend/workers/enum_agent.py` | Scan details/dashboard | Hosts, ports, URLs, technologies |
| Vulnerability checks | `backend/workers/vuln_agent.py` and modules | Findings page | Validated findings |
| Secret checks | `backend/workers/secret_agent.py` | Findings/reports | Redacted secret evidence |
| Live events | event bus and WebSocket API | Live progress panel | Task/tool events |
| Reports | `backend/reports/report_builder.py` | Reports page | Markdown, JSON, optional PDF |
| Dashboard | dashboard API modules | Overview page | Counts, timeline, breakdowns |

## 14. API surface

The router is exposed under both `/api` and `/api/v1`. The exact schemas are defined in `backend/api/schemas.py`; the main functional groups are:

- Authentication: login, registration, refresh, logout.
- Scans: create, list, read, cancel, and workflow control.
- Findings: list, filter, detail, and scan-scoped evidence.
- Reports: list, generate, and download artifacts.
- Results/tasks: inspect worker status and structured output.
- Assets/plugins: inspect discovered assets and registered tool metadata.
- Dashboard: overview, details, severity, and timeline.
- Targets: authorization requests, approvals, rejection, and review history.
- WebSocket: subscribe to a scan's live event stream.

## 15. Data contract for a tool result

Every plugin execution should be converted to a common result shape. Important fields include:

```text
tool_name
success
status
exit_code
timed_out
unavailable
parsed
raw_output
command_executed
error_message
execution_time
scan_id
task_id
```

This contract allows the UI, fallback manager, finding processor, and report builder to operate without knowing every command-line tool's native output format.

## 16. Safety and evidence features

- Target validators reject private or non-routable destinations in normal operation.
- Tool execution uses structured argument lists rather than concatenated shell commands.
- Command display is escaped and credential-like values are redacted.
- Findings retain evidence and provenance but secret values are masked.
- Report filenames are sanitized for Windows and Unix reserved names.
- The workflow records unavailable tools and failed checks instead of presenting a false success.

## 17. Operational controls

The configuration model includes:

- `APP_ENV`, `APP_DEBUG`, `ALLOWED_HOSTS`, and `STORAGE_BACKEND`.
- Database URL and PostgreSQL connection values.
- Redis and Celery broker/result URLs.
- JWT secret, algorithm, expiry, and authentication enablement.
- AI provider keys, which are status-only unless wired into a workflow.
- Maximum concurrent scans and scan/tool timeouts.
- DNS resolvers and tool executable paths.
- Wordlist and Nuclei template paths.

Values belong in `.env` or deployment secret management, never in Markdown reports or source code.
