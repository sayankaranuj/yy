# FoundFirst AI: Detailed Testing and Controlled Vulnerable Target

## 1. Testing policy

Testing must be limited to systems owned by the project team or explicitly authorized in writing. This document uses a self-owned local fixture and deterministic test data. It does not recommend attacking a public target.

The controlled target is named `vulnerable-fixture.test` and is intended to run only inside an isolated Docker test network. It is not a real public domain.

## 2. Vulnerable fixture design

The fixture contains deliberately seeded, non-destructive conditions:

| Fixture condition | Expected observation | Expected severity |
|---|---|---|
| Missing common security headers | Header audit reports absent hardening headers | Low |
| Reflected marker in a search response | The marker is reflected without server-side persistence | Medium |
| Debug endpoint exposes configuration metadata | A known test-only endpoint returns non-secret metadata | Medium |
| Authorization fixture returns another test user's record | Access-control test detects an object-scope failure | High |
| Test repository contains a fake credential marker | Secret scanner detects and redacts the marker | High |
| Open test port on the fixture service | Enumeration records the port | Informational |

The fixture uses fake values only. It must not contain live credentials, production data, real API keys, or destructive payload handlers.

## 3. Test setup

1. Build the project test images.
2. Start the isolated test compose file.
3. Add `vulnerable-fixture.test` to the test network resolver or container hosts file.
4. Confirm the fixture health endpoint responds.
5. Submit an authorization request for the fixture.
6. Approve it using the test administrator account stored in local environment variables.
7. Run a Full scan with all outputs directed to the test data directory.
8. Stop and remove only the test containers and test volumes after the run.

No credential should be written into a Markdown report or committed file.

## 4. Test layers

### 4.1 Unit tests

Unit tests cover:

- Target validation.
- JWT rejection for expired and `alg:none` tokens.
- Severity and OWASP mapping.
- Secret redaction.
- Decision-engine stage selection.
- Fallback decisions and result merging.
- State transitions and cancellation.
- Report filename sanitization.
- Plugin registration metadata.

### 4.2 API tests

API tests cover:

- Health and readiness responses.
- Authentication routes.
- Scan creation and target validation.
- Findings, reports, tasks, results, and dashboard endpoints.
- Authorization requests and administrator decisions.
- WebSocket route behavior.
- Scan-scoped result filtering.

### 4.3 Worker tests

Worker tests cover:

- Celery task registration.
- Retry configuration.
- Recon plugin execution and deduplication.
- Enumeration summaries.
- Vulnerability validation and processing.
- Secret scanning and redaction.
- Report task output.

### 4.4 Frontend tests

Frontend tests cover:

- Login and error display.
- Scan creation.
- Severity and scan-mode rendering.
- Dashboard data handling.
- Report and result controls.

## 5. Controlled end-to-end test cases

| ID | Action | Expected result |
|---|---|---|
| E2E-01 | Submit fixture before approval | Request is pending and scan is not dispatched |
| E2E-02 | Approve fixture | Approval is persisted with reviewer metadata |
| E2E-03 | Start Full scan | Workflow contains ordered stages and task IDs |
| E2E-04 | Run recon | Fixture host is discovered and duplicate records are merged |
| E2E-05 | Run enumeration | Live host, port, technology, and endpoint counts are returned |
| E2E-06 | Run vulnerability checks | Seeded header, reflection, debug, and authorization findings are validated |
| E2E-07 | Run secret scan | Fake credential is detected, then redacted |
| E2E-08 | Disconnect one optional tool | Failure is visible and supported fallback/retry behavior is recorded |
| E2E-09 | Open live scan view | WebSocket events show task and tool progress |
| E2E-10 | Generate report | Markdown, JSON, and optional PDF outputs are scan-scoped |
| E2E-11 | Cancel during a stage | Worker stops at its cancellation check and returns cancelled |
| E2E-12 | Repeat a clean diff scan | No change notification is created |

## 6. Measured repository evaluation

The existing deterministic evaluation suite reported:

- 14 evaluation tests passed.
- Fixture detection: 1 true positive, 0 false positives, 0 false negatives, recall 1.00.
- Fallback decisions verified for recon, vulnerability, and low-quality output paths.
- Worker retry contracts verified.
- Five sequential and five parallel decision evaluations completed under one second each.
- A planted `port:8080` change was detected by diff logic.
- A clean diff produced no changes.
- Expired and unsigned JWT forms were rejected.
- Secret evidence was redacted before report rendering.
- SQL injection mapped to CWE-89 and the SQL Injection category.
- Report completeness paths were covered by report tests.
- Evaluation-only coverage was 25% of backend statements; this is not project-wide coverage.

The broader repository log also records 79 backend tests passing, 6 frontend tests passing, and a successful frontend build at the time of that verification. These values are historical measurements and should be refreshed when the implementation changes.

## 7. Accuracy metrics

For a real fixture run, calculate:

- True positives: seeded issues correctly reported.
- False positives: findings reported for conditions not present.
- False negatives: seeded issues not reported.
- Precision = true positives / (true positives + false positives).
- Recall = true positives / (true positives + false negatives).
- Duplicate reduction = 1 - (deduplicated records / raw records).

Record the scanner version, template version, fixture commit, target configuration, start time, and test result artifacts with every measurement.

## 8. Negative and safety tests

- Private, loopback, link-local, and cloud-metadata targets are rejected unless a test-only override is explicitly enabled.
- Shell metacharacters and markup-like target values are rejected.
- JWT algorithms are allow-listed.
- Expired tokens are rejected.
- Viewer-level users cannot start scans.
- Scan and finding IDs cannot be used to read another scan's results.
- Rate-limit configuration remains bounded.
- Exploit and autonomous modes remain disabled unless explicitly configured.
- Secret values are absent from stored evidence and generated reports.

## 9. Test limitations

The current repository tests do not by themselves prove detection accuracy against every real technology, complete runtime recovery after killing a worker, live HTTP rate-limit rejection thresholds, or a production RBAC matrix. Those claims require a running controlled environment and must not be inferred from unit tests.

## 10. Test execution commands

Run backend tests from the project root:

```powershell
python -m pytest -q
python -m pytest tests/test_full_environment_evaluation.py -q
python -m pytest --cov=backend --cov-report=term-missing
```

Run frontend checks from `frontend`:

```powershell
npm test -- --run
npm run build
```

The first command validates Python behavior, the second focuses on deterministic safety/evaluation fixtures, and the frontend commands validate component behavior and production bundling.

## 11. Test data and isolation

Test data should be separated by:

- Test scan ID.
- Test storage directory.
- Test Redis database or container.
- Test PostgreSQL database/schema.
- Test report output directory.
- Test fixture network.

Do not point a test run at production stores. Do not use a real API key to demonstrate secret detection. Use a marker such as `FAKE_TEST_TOKEN_DO_NOT_USE` and assert that it becomes `[REDACTED]`.

## 12. Example fixture request sequence

The following is a conceptual sequence; endpoint fields must match the current schemas:

```text
POST /api/auth/login
POST /api/targets/authorization-requests
POST /api/targets/{request_id}/approve
POST /api/scans
GET  /api/scans/{scan_id}
GET  /api/scans/{scan_id}/workflow
GET  /api/scans/{scan_id}/results
GET  /api/scans/{scan_id}/reports
WS   /api/scans/{scan_id}/events
```

Assertions should verify status codes, response shape, scan ID consistency, task ID presence, and absence of secret values.

## 13. Vulnerability result verification

For each seeded issue, a reviewer should record:

1. Seed condition and fixture version.
2. Request or response evidence.
3. Tool that produced the candidate.
4. Validator decision.
5. Stored finding ID and scan/task IDs.
6. Severity and confidence.
7. Report presence.
8. Remediation and retest result.

The test passes only when the finding is both detected and correctly attributed. A count-only comparison is insufficient.

## 14. Failure-injection tests

Safe failure injection can be performed by:

- Removing a test-only tool binary from the worker image.
- Returning a controlled non-zero exit code from a fixture plugin.
- Delaying a fixture response beyond the configured timeout.
- Temporarily disconnecting the test Redis service.
- Cancelling a scan between two stages.

Do not inject destructive payloads. Confirm that the workflow records the failure, retry/fallback decision, and final status.

## 15. Report assertions

For Markdown, JSON, and PDF artifacts verify:

- Target and scan ID are correct.
- Findings belong only to the requested scan.
- Severity and OWASP/CWE fields are present when mapped.
- Failed and skipped checks are visible.
- Redacted values do not appear in content.
- Filenames cannot escape the report directory.
- Re-running a scan does not overwrite an unrelated scan artifact.

## 16. Acceptance criteria

The controlled test is accepted only if:

- Unauthorized targets are blocked.
- The approved fixture completes or reports a clear partial/failed status.
- Every seeded issue has a known expected result.
- No cross-scan finding leakage occurs.
- Cancellation and timeout behavior is observable.
- Secret markers are redacted.
- Reports are reproducible from persisted data.
