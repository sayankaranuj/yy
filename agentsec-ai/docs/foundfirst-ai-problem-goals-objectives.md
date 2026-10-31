# FoundFirst AI: Problem Definition, Goal, and Objectives

## 1. Problem definition

Security assessment work is often fragmented across command-line tools, separate result formats, manual note-taking, and disconnected reporting steps. Reconnaissance, enumeration, vulnerability checks, secret scanning, validation, and report creation may be performed by different operators or scripts without a consistent scan identity.

This creates practical problems:

- Asset discovery is incomplete or duplicated.
- Tool failures are easy to miss.
- Findings lose their source and evidence context.
- Long-running scans block interactive workflows.
- Operators cannot see progress across tools.
- Reports require repetitive manual assembly.
- Sensitive evidence can be copied into unsafe locations.
- Authorization and scope decisions are not always represented in the workflow.
- It is difficult to compare repeated scans or clean changes.

## 2. Project goal

The goal of FoundFirst AI is to provide a controlled, extensible, and observable platform that coordinates authorized security assessments from scoped target approval through recon, enumeration, vulnerability validation, secret handling, live progress, and report generation.

The project prioritizes traceability and safe orchestration over claiming that automation replaces a security professional.

## 3. General objectives

1. Provide one operator interface for assessment lifecycle management.
2. Validate and authorize targets before work is dispatched.
3. Combine multiple specialized tools behind a normalized plugin contract.
4. Run long tasks asynchronously without blocking the API.
5. Preserve scan, task, tool, finding, and report relationships.
6. Detect and record tool failures instead of silently ignoring them.
7. Use fallback and retry behavior for recoverable failures.
8. Stream bounded live progress to the operator.
9. Validate findings before presenting them as actionable.
10. Redact secret-like evidence before storage and export.
11. Produce repeatable Markdown, JSON, and optional PDF reports.
12. Provide tests and measurable evaluation fixtures for future improvement.

## 4. Specific objectives by lifecycle

### Before scanning

- Authenticate the operator.
- Capture target and scan metadata.
- Validate target syntax and safety constraints.
- Record authorization and administrative review.
- Allow a deliberate scan mode and attack-category selection.

### During discovery

- Run recon plugins.
- Merge duplicate assets.
- Identify live hosts, ports, technologies, URLs, and directories.
- Build a reusable context for later checks.

### During assessment

- Run template, web, API, authorization, and secret checks.
- Preserve raw and parsed evidence.
- Apply cancellation, timeout, retry, and fallback controls.
- Keep output attributable to the correct scan and task.

### After assessment

- Validate and process findings.
- Map findings to severity and OWASP/CWE context.
- Update dashboards and activity timelines.
- Generate scan-scoped reports.
- Preserve a clear record of failed and skipped work.

## 5. Quality objectives

- Correctness: use typed inputs, structured outputs, and explicit errors.
- Safety: support authorized testing only and avoid exposing secrets.
- Reliability: retry transient failures and record permanent failures.
- Observability: expose health, readiness, task, event, and report state.
- Extensibility: add plugins without rewriting the orchestration core.
- Maintainability: keep API, worker, processor, and reporting responsibilities separated.
- Testability: use deterministic fixtures and focused unit/API/frontend tests.

## 6. Success criteria

The project is successful when an authorized operator can:

1. Sign in and request a scoped assessment.
2. Obtain target approval.
3. Start a selected scan mode.
4. Observe stage and tool progress.
5. Review scan-scoped findings with evidence.
6. See failures, skipped checks, and retry outcomes.
7. Generate a redacted report.
8. Repeat the process against a controlled fixture and compare measurable results.

## 7. Non-goals

FoundFirst AI is not intended to:

- Grant permission to test third-party systems.
- Guarantee complete vulnerability discovery.
- Replace manual security review.
- Automatically exploit production systems.
- Store unprotected credentials.
- Claim that an AI provider is active when it is only configured.
- Serve as a public unauthenticated scanning service.

## 8. Expected contribution

The platform creates a single evidence trail from scope decision to report. Its value is the consistent coordination of discovery, assessment, validation, resilience, and reporting, while leaving final risk acceptance and remediation decisions with the responsible security team.

## 9. Technical problem statement

The project problem can be stated as:

> Given an explicitly authorized target and a selected assessment scope, provide a repeatable way to dispatch heterogeneous security tools, normalize their outputs, preserve evidence and provenance, recover from expected failures, stream progress, validate findings, and generate a redacted report without blocking the operator interface.

This statement contains both functional and non-functional requirements. The functional requirement is to perform the assessment stages. The non-functional requirements are safety, traceability, reliability, observability, scalability, and maintainability.

## 10. Inputs, processing, and outputs

### Inputs

- Operator identity.
- Target and authorization information.
- Scan mode.
- Optional attack categories.
- Tool configuration, templates, wordlists, and timeouts.
- Optional approved public repository and scan options.

### Processing

- Validate scope and target.
- Select workflow stages.
- Queue specialized tasks.
- Execute plugins.
- Normalize and deduplicate data.
- Build context.
- Validate candidate findings.
- Redact sensitive evidence.
- Persist and aggregate results.

### Outputs

- Asset inventory.
- Live hosts, ports, technologies, endpoints, and directories.
- Validated findings.
- Tool errors and skipped checks.
- Live events and workflow state.
- Dashboard metrics.
- Markdown, JSON, and optional PDF reports.

## 11. Objective traceability

| Objective | Design response | Evidence of completion |
|---|---|---|
| Avoid fragmented tools | Plugin registry and executor | Normalized tool results |
| Keep UI responsive | Celery and Redis | Queued task workflow |
| Preserve evidence | Finding/result processors | Scan/task provenance |
| Reduce duplicates | Recon merge and finding processing | Deduplication tests |
| Handle failures | Retry, fallback, partial status | Evaluation tests |
| Protect secrets | Redaction utility and report filtering | Redaction tests |
| Explain progress | Event bus and WebSocket | Live event tests |
| Produce reports | Report builder | Markdown/JSON report tests |
| Control scope | Authorization workflow and validators | Authorization tests |

## 12. Functional requirements

1. The system shall accept an authorized target request.
2. The system shall reject invalid or unsafe target values.
3. The system shall create a uniquely identifiable scan.
4. The system shall select a known workflow plan.
5. The system shall dispatch work to the correct queue.
6. The system shall preserve task and scan provenance.
7. The system shall record tool success, failure, timeout, and availability.
8. The system shall validate findings before persistence.
9. The system shall redact secret-like evidence.
10. The system shall expose scan status and results.
11. The system shall generate report artifacts.

## 13. Non-functional requirements

- Security: no secret hardcoding and no uncontrolled target expansion.
- Reliability: retry transient failures and retain partial results.
- Performance: return scan creation without waiting for network work.
- Observability: provide health, readiness, logs, task IDs, and events.
- Portability: support Docker-based local deployment and configured Windows/Linux paths.
- Extensibility: permit new tools through plugin metadata and executor contracts.
- Auditability: retain authorization, task, finding, and report relationships.

## 14. Project boundaries

The project owns orchestration, validation, evidence handling, and presentation. It does not own the behavior or accuracy of third-party tools, the legal authorization of a target, or the final remediation decision. Those boundaries should be stated in every academic, technical, or operational presentation of the system.
