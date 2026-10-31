A. Detection accuracy (most important)

Scan known-vulnerable targets (DVWA, OWASP Juice Shop, scanme.nmap.org, both already in your feature list). Compare found vs. known vulnerabilities to get true positives, false negatives, and recall.
Baseline comparison: run Nuclei alone, or Nmap + Nuclei manually, on the same targets, against AgentSec AI. This is your equivalent of the SafePay four-model table.
False-positive rate before vs. after your 7-question validation gate. Manually verify findings to count them.

B. Recon and enumeration coverage
4. Subdomain count from AgentSec vs. each single tool (Subfinder alone, Amass alone) on the same domain, to show multi-tool merging adds coverage.
5. Duplicate reduction from merging and deduplication.

C. Fallback and resilience
6. Fault injection: deliberately kill or time out Naabu, then record whether RustScan takes over, how long recovery takes, and whether the scan completes.
7. Repeat for Subfinder→Amass and SQLMap→Nuclei.
8. Worker crash test: stop a Celery worker mid-scan and check whether the task is retried or recovered.

D. Performance
9. Scan time per phase (recon, enum, vuln, secrets, report) and total, in a table like SafePay's Table VI.
10. Sequential vs. parallel time (vuln and secrets agents run in parallel), showing the speedup.
11. Concurrent scans (1, 3, 5 targets): time, CPU/RAM use, and queue behaviour.
12. Orchestrator decision latency (event received → next task dispatched).

E. Orchestrator logic
13. Decision correctness: feed each event type (recon_complete, tool_failed, etc.) and verify the right action is dispatched. A test-case table works well.
14. Rule-based vs. AI-assisted mode: compare Classic, Hybrid, and Autonomous (Strix) on the same target for findings, time, and cost. Only include this if you actually run all three.

F. Continuous monitoring
15. Diff-scan accuracy: change a test target (open a port, add a subdomain), rescan, and check whether the diff engine catches every planted change.
16. Confirm no notification is sent on a clean diff.

G. Security and safety controls (mirrors SafePay's live API tests)
17. Private IP, localhost, and cloud-metadata-IP targets rejected
18. JWT alg:none rejected, expired token rejected, refresh-token blacklist after logout
19. Role-based access (Viewer can't start scans) and IDOR checks
20. Rate limiting works
21. Kill switches: exploit and Strix agents refuse to run when disabled
22. Strix budget/turn cap enforced; scope-confirmation gate blocks without sign-off
23. Secret masking in stored findings and reports

H. Reporting
24. OWASP/CWE mapping correctness on a sample of findings (manually checked)
25. Report generation time and completeness

I. Software quality
26. Your pytest coverage numbers, but only report what you actually measured.

## Controlled local evaluation results

The following results were measured on 2026-10-05 with
`tests/test_full_environment_evaluation.py`. The suite uses local fixtures and
pure orchestration components; it does not attack public systems.

| Area | Measured result |
|---|---|
| True/false-positive fixture accuracy | 1 TP, 0 FP, 0 FN, recall 1.00 |
| Fallback injection | Decision and merge behavior verified for `subfinder -> amass`, `nuclei -> dalfox`, and low-quality output |
| Worker recovery contract | Recon and vulnerability Celery tasks expose retry configuration |
| Performance/concurrency | Five sequential and five parallel decision evaluations completed under 1 second each |
| Diff scanning | Planted `port:8080` change detected; clean diff produced no changes |
| JWT controls | Expired and `alg:none` tokens rejected by the configured decoder |
| Rate-limit configuration | Positive bounded per-minute limit verified; live HTTP rejection load test remains separate |
| Kill switches | Exploit mode disabled path and Strix disabled configuration verified |
| Secret masking | Key/value secret evidence is redacted before JSON persistence and report rendering |
| CWE/OWASP mapping | SQL injection sample mapped to CWE-89 and SQL Injection |
| Report completeness | Markdown/JSON report generation path and required finding fields covered by existing report tests |
| Evaluation test result | 14 passed |
| Evaluation-only coverage | 25% of `backend` statements; this is not a project-wide coverage claim |

## Environment-gated comparisons

The worker image contains `nmap`, `nuclei`, `subfinder`, and `amass`. It does
not contain `rustscan` or `sqlmap`. Therefore, real same-target Nmap/Nuclei
and Subfinder/Amass result-count comparisons require a controlled local target
and installation of the missing fallback binaries. No public target is used as
a substitute.

Worker crash recovery, live HTTP rate-limit rejection thresholds, RBAC/IDOR
role matrices, and Classic/Hybrid/Autonomous comparisons require dedicated
runtime fixtures and are not inferred from unit tests.

