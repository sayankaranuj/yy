# FoundFirst AI: Project Limitations

## 1. Scope and authorization

FoundFirst AI is an assessment aid, not a legal authorization system. A user can technically submit a target, but that does not create permission to test it. Operators must obtain written authorization, define scope, respect rate limits, and stop when the engagement ends.

## 2. Detection limitations

- No scanner detects every vulnerability.
- Tool output can contain false positives, false negatives, duplicates, or incomplete evidence.
- Detection quality depends on target reachability, authentication context, tool versions, templates, wordlists, network filtering, and scan timeouts.
- A validated finding is not automatically a confirmed exploitable vulnerability.
- Absence of a finding is not proof of absence.
- Technology fingerprinting can be wrong when applications conceal headers or proxy traffic.
- Dynamic, authenticated, stateful, and business-logic vulnerabilities need tailored tests.
- Authorization tests require correctly configured test roles and credentials.

## 3. Tool availability

The platform is an orchestrator around external tools. A worker can report an unavailable binary, timeout, malformed output, or permission problem. Fallbacks improve resilience but do not guarantee equivalent coverage. Some configured tools are not present in every image, and missing tools reduce the real scan surface.

## 4. Workflow limitations

- Some workflow paths are lightweight or test-oriented rather than complete production pipelines.
- Celery and Redis require correct broker availability and queue configuration.
- A broker outage prevents dispatch even though the API process may remain healthy.
- Retry behavior does not recover every permanent failure.
- The current stage chain is ordered; it is not a full dependency-aware scheduler for every module.
- Cancellation occurs at worker checks and cannot necessarily interrupt a subprocess immediately.
- Live event history is intentionally bounded and expires, so it is not an archival audit log.

## 5. Persistence limitations

PostgreSQL is configured, migrated, and health-checked, but the current scan and workflow repositories still use JSON-backed storage in important paths. This creates limitations for:

- Multi-instance coordination.
- Transactional consistency.
- High-volume concurrent scans.
- Database-level querying and indexing.
- Backup, retention, and recovery guarantees.

The PostgreSQL page is read-only and does not mean every scan record is already PostgreSQL-backed.

## 6. AI limitations

The interface exposes AI-provider configuration status, but the current scan workflow does not automatically invoke an LLM for every finding. A configured provider key does not prove that AI analysis is active. Results should not be described as AI-generated unless the provider integration is explicitly enabled and verified.

## 7. Authentication limitations

- JWT protection is optional and disabled by default in development settings.
- Development defaults are not suitable for production.
- Local storage of browser tokens has the usual browser theft risks.
- A secure deployment needs strong secrets, HTTPS, cookie policy, rotation, revocation, and an operational identity provider.
- Authorization behavior must be tested with real role matrices before production claims are made.

## 8. Reporting limitations

- Reports summarize collected evidence; they do not independently reproduce every issue.
- Markdown and JSON outputs may contain tool-specific fields with inconsistent quality.
- PDF generation depends on the optional rendering stack.
- Reports are not a substitute for a human-reviewed penetration-test report.
- Report retention, access control, signing, and long-term archival require deployment policy.

## 9. Performance limitations

- Resource use depends on the number of targets, open ports, URLs, templates, and workers.
- High concurrency can overload the target, Redis, PostgreSQL, or worker hosts.
- The measured sub-second decision tests do not represent a full network scan.
- A configured maximum concurrency is not a complete capacity-planning model.
- No universal scan-duration guarantee can be made.

## 10. Environment limitations

- Docker Desktop, Python, Node.js, npm, PostgreSQL, Redis, and external binaries must be installed correctly.
- Windows and Linux tool paths differ.
- Network DNS, firewall, proxy, and container permissions affect results.
- Public cloud, authenticated applications, private repositories, and rate-limited services need environment-specific configuration.

## 11. Security limitations

- The platform reduces command-injection risk through validation and structured execution, but every new plugin must be reviewed.
- Redaction patterns cannot recognize every secret format.
- Evidence can still contain sensitive business information even when obvious token values are masked.
- The UI should not be exposed directly to the internet without a hardened reverse proxy and access controls.
- The application must be kept updated with security patches for its Python, JavaScript, container, database, and scanning-tool dependencies.

## 12. Project maturity limitations

The project has meaningful test coverage and operational scaffolding, but some production-readiness work remains: completing PostgreSQL-backed repositories, expanding integration fixtures, validating real worker recovery, enforcing the full role matrix, and measuring accuracy on a maintained authorized benchmark.

## 13. Technical limitations by layer

### Frontend

- The browser is a presentation client and cannot guarantee that a backend operation completed.
- Local token storage is exposed to browser compromise.
- A disconnected WebSocket can cause the operator to miss live events until the page refreshes.
- UI progress is derived from backend events and may lag persisted state.

### API

- Optional authentication means a development deployment can be accidentally exposed without protection.
- Health endpoints indicate process/database availability, not tool availability.
- API availability does not guarantee Redis, Celery, or scanner health.
- Rate-limit settings need runtime enforcement and load validation, not only configuration.

### Orchestrator

- Celery chains are not a complete distributed transaction.
- A task may finish externally before its result is persisted.
- Duplicate delivery or retry can require idempotent processors.
- A rule-based decision is only as correct as its context and rules.

### Plugins

- Native tool output changes can break parsers.
- Plugin imports and subprocesses expand the trust boundary.
- A fallback may have different coverage and severity behavior than the primary tool.
- Tool versions and template versions materially affect results.

### Storage

- JSON storage can lose consistency under concurrent writers.
- File-based reports need retention and access control.
- PostgreSQL schema existence does not mean all repositories use it.
- There is no universal immutable evidence archive in the current prototype.

## 14. Security operations limitations

FoundFirst AI does not provide a complete engagement-management system. It does not automatically enforce a contract, legal scope, emergency contact, maintenance window, or production change-control process. Those controls remain organizational responsibilities.

It also does not guarantee safe behavior from a newly added plugin. Every plugin must be reviewed for argument injection, data exposure, network scope, dependency risk, output redaction, and authorization assumptions.

## 15. Improvements required before production

1. Make PostgreSQL the authoritative store for scans, workflows, findings, and approvals.
2. Add transactional/idempotent result updates.
3. Enforce authentication and role authorization by default.
4. Add durable audit logging and evidence retention policy.
5. Add distributed rate limiting and concurrency controls.
6. Add worker heartbeat, dead-letter, and recovery monitoring.
7. Pin and continuously update tool/template/container versions.
8. Expand authorized vulnerable fixtures and accuracy benchmarks.
9. Add automated cross-scan isolation and privilege-matrix tests.
10. Put the frontend behind HTTPS and a hardened reverse proxy.
