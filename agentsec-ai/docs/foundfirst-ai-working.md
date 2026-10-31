# FoundFirst AI: Detailed Working Flow

## 1. Startup flow

1. The FastAPI application is created by `create_app`.
2. Environment variables and `.env` values are loaded into typed settings.
3. Trusted-host middleware is installed.
4. Optional JWT middleware protects API routes while leaving health and authentication routes available.
5. The application lifespan initializes the configured database layer.
6. API routes are mounted under both `/api` and `/api/v1`.
7. Docker Compose starts PostgreSQL, Redis, the backend, frontend, specialized workers, and Flower.

## 2. Authentication and authorization flow

1. The frontend displays the operator login screen.
2. Login calls the backend authentication route.
3. The backend verifies the configured credentials or registered user record.
4. A token is returned when authentication succeeds.
5. The frontend stores the token locally and sends it with protected requests.
6. A scan target is submitted for authorization when policy requires approval.
7. The administrator reviews the request and records approval or rejection.
8. Only an approved target should enter an assessment workflow.

## 3. Scan creation flow

1. The operator enters a scan name and authorized target.
2. Optional attack categories are selected.
3. The frontend sends the scan request to the scans API.
4. The backend validates the target, including invalid, private, non-routable, shell-like, or markup-like values.
5. A scan record is created with a stable identifier.
6. The workflow runner marks the scan as running and publishes `scan.started`.
7. The decision engine chooses stages from the scan type and target context.
8. A workflow record is persisted with queued steps and generated task identifiers.
9. The first Celery task is sent to its specialized queue.
10. Remaining tasks are linked as a Celery continuation.

## 4. Stage selection

The default stage plans are:

| Mode | Stages |
|---|---|
| Full | Reconnaissance, enumeration, vulnerability checks, report |
| Recon only | Reconnaissance, report |
| Vulnerability only | Vulnerability checks, report |
| Quick | Reconnaissance, vulnerability checks, report |

The decision engine may replace the default plan using context rules. Explicit attack-category selection filters the relevant stage and can add the Git-secret stage when a repository scan is selected.

## 5. Reconnaissance flow

1. The recon worker checks whether the scan was cancelled.
2. The plugin registry discovers available plugin modules.
3. The worker selects all recon plugins or the requested tool decisions.
4. Each plugin receives a typed `PluginInput` containing scan ID, target, task ID, timeout, and optional parameters.
5. The executor launches the configured command without treating raw user input as a shell command.
6. Output is normalized into parsed records, raw output, command metadata, status, error, and execution time.
7. Subdomains and host values from all successful plugins are merged and deduplicated.
8. The recon processor persists the resulting asset inventory.
9. Tool errors remain attached to the workflow result rather than being silently discarded.

## 6. Enumeration flow

1. Enumeration reads recon output or receives the selected target.
2. HTTPX checks live hosts and can provide technology information.
3. Naabu or another port plugin discovers exposed ports.
4. Katana crawls reachable applications and records URLs.
5. Technology fingerprinting, directory discovery, and JavaScript discovery add context.
6. Processors aggregate counts and detailed records.
7. A context builder produces the input for vulnerability and secret analysis.
8. The stage publishes `enum.completed` and returns live-host, port, endpoint, and timing data.

## 7. Vulnerability flow

1. The vulnerability worker checks cancellation and receives the scan context.
2. Nuclei runs the selected templates.
3. Web-application, API-security, and authorization modules add specialized checks.
4. Raw module findings are combined.
5. The vulnerability validator checks evidence quality and rejects unsupported or placeholder findings.
6. The finding processor assigns scan/task provenance and persists accepted findings.
7. The worker returns findings, counts, and execution time.
8. Finding events update the dashboard and report inputs.

## 8. Secret and Git flow

1. The secrets worker receives JavaScript files, repository URLs, and context.
2. JavaScript extraction, Git scanning, and cloud checks run through their modules.
3. A secret validator checks whether a candidate is real enough to retain.
4. Secret-like values are redacted before persistence.
5. Repository results can be compared with a baseline.
6. The report and API layers expose detector and location metadata without exposing the secret value.

## 9. Continuation and failure flow

1. A successful task allows the linked next task to execute.
2. A retryable exception uses the task's retry configuration.
3. A failed tool is recorded in structured output.
4. The fallback manager can select an alternate tool for supported decisions.
5. If queue dispatch fails, the workflow raises an explicit dispatch error and logs the exception.
6. Cancellation causes workers to return a cancelled status rather than continue scanning.
7. The final report stage summarizes completed, failed, and skipped work.

## 10. Live progress flow

1. Orchestration publishes lifecycle events to the in-process event bus.
2. A Redis-backed event bridge publishes events for WebSocket consumers.
3. The frontend opens the scan event stream.
4. Tool name, command arguments, stdout, stderr, exit status, task ID, and error status are rendered.
5. Credential-like command values are redacted.
6. Event history is bounded and expires to avoid unbounded memory growth.

## 11. Reporting flow

1. The report API gathers scan-scoped workflow records and findings.
2. The report builder redacts finding mappings.
3. Markdown content is assembled for human reading.
4. JSON content is assembled with normalized status, severity, and OWASP mapping.
5. Optional PDF generation renders a detailed HTML-based report.
6. The report path and format are returned to the frontend for download.

## 12. Completion flow

1. The report worker completes or records an error.
2. The workflow store updates the final stage and scan state.
3. Dashboard counters and timeline endpoints read the persisted records.
4. The frontend refreshes scan, finding, report, and activity views.
5. Operators can inspect evidence, export a report, or start a new authorized scan.

## 13. Detailed request-to-worker sequence

The complete request path is:

```text
Browser form
  -> frontend api client
  -> POST /api/scans
  -> Pydantic request validation
  -> target safety validation
  -> scan repository record
  -> run_scan_workflow(scan_id, target, scan_type)
  -> decision engine
  -> workflow store
  -> Celery signature and queue
  -> Redis broker
  -> specialized worker
  -> plugin executor
  -> processor/store
  -> event bus and result backend
  -> report builder
  -> dashboard/report API
  -> browser
```

The HTTP request should return a scan/workflow response without waiting for all network tools to finish. This is the main reason the project uses Celery.

## 14. State and status behavior

At scan level, the normal lifecycle is:

```text
pending -> running -> completed
                    \-> failed
                    \-> cancelled
```

At step level, a task may be queued, running, completed, partially completed, failed, cancelled, or skipped. A partial stage means at least one selected tool returned useful output while another tool failed. The UI must not convert partial into completed without preserving the underlying failure details.

## 15. How stage selection works technically

`STAGE_MAP` provides the default stage list. The decision engine receives a context dictionary containing at least `scan_id`, `target`, and `scan_type`. Rules can replace the standard list, for example when a target contains a configured quick or recon-only marker. Attack-category filtering then removes stages whose category was not selected. Queue mapping assigns:

```text
workers.recon.run -> recon_queue
workers.enum.run  -> enum_queue
workers.vuln.run  -> vuln_queue
workers.git.run   -> secrets_queue
workers.report.run -> report_queue
```

Each signature receives a UUID task ID. The first signature is sent to Celery and the remaining signatures are attached as a continuation chain.

## 16. How a plugin execution works

1. The worker constructs `PluginInput`.
2. The input carries target, scan ID, task ID, timeout, and safe extra parameters.
3. The registry resolves a plugin name.
4. The executor checks availability and builds the command argument list.
5. A subprocess runs with timeout handling.
6. stdout and stderr are captured.
7. The plugin parser converts output into records.
8. The result is returned to the worker.
9. The worker persists normalized records and emits a summary.

An unavailable binary, timeout, non-zero exit status, or parser error must remain visible in `tool_errors` or equivalent structured fields.

## 17. Failure and retry sequence

Retryable Celery exceptions use task retry configuration. A retry is different from a tool fallback:

- Retry repeats the same task after a transient worker or infrastructure exception.
- Fallback selects a different tool when the decision engine says an alternate tool can provide coverage.
- Partial completion preserves successful output even if another tool failed.
- Dispatch failure raises an explicit runtime error and logs the original exception.

This distinction is important for an operator deciding whether to rerun a scan or review an incomplete result.

## 18. Persistence sequence

The current implementation persists workflow and finding data through JSON-backed stores in important paths. PostgreSQL is initialized and available as a deployment foundation, but it is not yet the source of truth for every scan repository. A workflow read therefore obtains:

1. Scan metadata.
2. Workflow steps and task IDs.
3. Structured worker results.
4. Finding records filtered by scan/task provenance.
5. Report artifact metadata.

## 19. Shutdown and recovery

On normal shutdown, containers stop independently and named volumes preserve PostgreSQL/Redis data. If a worker disappears, Celery may retry a configured task, but the system does not guarantee recovery from every process termination. Operators should inspect Flower, worker logs, task state, and workflow records before declaring the scan complete.
