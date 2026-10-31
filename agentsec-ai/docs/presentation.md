
# AgentSec AI — Presentation Questions and Technical Answers

## 1. List all the tools integrated in this project

The project integrates **24 executable security tools**, discovered and registered through the plugin registry in `registry.py`.

### Reconnaissance tools

| Tool | Purpose |
|---|---|
| Subfinder | Passive subdomain enumeration using public sources |
| Amass | Passive asset and subdomain discovery |
| Assetfinder | Finds related domains and subdomains |
| DNSx | DNS resolution and DNS record validation |
| Findomain | Domain and subdomain discovery |

### Enumeration tools

| Tool | Purpose |
|---|---|
| HTTPx | Detects live HTTP/HTTPS services and collects response metadata |
| Naabu | Fast TCP port scanning |
| Nmap | Service and version detection |
| RustScan | High-speed port discovery |
| Katana | Web crawling and endpoint discovery |
| Gau | Retrieves known URLs from public URL providers |
| Waybackurls | Extracts URLs from the Wayback Machine |
| FFUF | Directory and endpoint brute-forcing |
| WhatWeb | Web technology fingerprinting |

### Vulnerability tools

| Tool | Purpose |
|---|---|
| Nuclei | Template-based vulnerability and misconfiguration scanning |
| Dalfox | XSS parameter analysis and testing |
| SQLMap | SQL injection detection and controlled testing |
| WPScan | WordPress vulnerability and configuration scanning |
| Corsy | CORS misconfiguration detection |
| Tplmap | Server-side template injection testing |

### Secret and cloud security tools

| Tool | Purpose |
|---|---|
| TruffleHog | Git repository secret detection |
| SecretFinder | JavaScript secret and token discovery |
| LinkFinder | Finds endpoints and links inside JavaScript files |
| CloudEnum | Cloud asset and bucket enumeration |

Each tool is represented by a plugin adapter. The common adapter behavior is defined in `base_plugin.py`.

The adapter provides:

- Command construction
- Input normalization
- Timeout control
- Process execution
- stdout/stderr collection
- Cancellation handling
- Output parsing
- Error handling
- Tool lifecycle events
- Exit-code reporting
- Result normalization

The system does not directly invoke tools from the frontend. The frontend submits scan requirements to FastAPI, and workers execute tools through the plugin executor.

---

## 2. List all attacks the project can perform

The authoritative attack catalog is defined in `schemas.py`.

The catalog currently exposes **31 selectable attack categories**.

### Reconnaissance attacks

1. Subdomain Enumeration
2. DNS Record Enumeration
3. WHOIS Lookup
4. ASN and IP Range Discovery
5. Certificate Transparency Mining
6. AI OSINT

Important presentation clarification: some catalog entries are conceptual attack categories rather than fully implemented independent plugins. For example, the catalog contains WHOIS, ASN discovery, certificate transparency, and AI OSINT, but the currently executable plugin registry mainly contains the five concrete reconnaissance tools listed above.

### Enumeration attacks

1. Port Scanning
2. Live Host Detection
3. Technology Fingerprinting
4. Web Crawling
5. Directory Brute-forcing
6. JavaScript File Discovery

### Vulnerability attacks

1. Nuclei Template Scanning
2. SQL Injection
3. Cross-Site Scripting
4. Server-Side Request Forgery
5. Local File Inclusion / Remote File Inclusion
6. Server-Side Template Injection
7. Command Injection
8. CORS Misconfiguration
9. IDOR and Broken Access Control
10. GraphQL Security Testing
11. CMS-Specific Testing

### Authentication and authorization attacks

1. Session Cookie Security Testing
2. OAuth Flow Testing
3. Rate Limit Testing

### Secret and cloud attacks

1. JavaScript Secret Extraction
2. Git Repository Scanning
3. Configuration and Backup File Scanning
4. Cloud Bucket Exposure

### Gated exploitation

1. Proof-of-Concept Generation

The exploitation category is intentionally gated. The platform is designed primarily for authorized assessment and evidence collection, not uncontrolled exploitation.

---

## 3. CWE categories related to attacks performed

The project’s attack categories map to several Common Weakness Enumeration categories.

| Attack | Related CWE |
|---|---|
| SQL Injection | CWE-89: Improper Neutralization of Special Elements used in an SQL Command |
| Cross-Site Scripting | CWE-79: Improper Neutralization of Input During Web Page Generation |
| SSRF | CWE-918: Server-Side Request Forgery |
| Local File Inclusion | CWE-22: Improper Limitation of a Pathname to a Restricted Directory |
| Remote File Inclusion | CWE-98: Improper Control of Filename for Include/Require Statement |
| SSTI | CWE-1336: Improper Neutralization of Special Elements Used in a Template Engine |
| Command Injection | CWE-77: Improper Neutralization of Special Elements used in a Command |
| OS Command Injection | CWE-78: Improper Neutralization of Special Elements used in an OS Command |
| CORS Misconfiguration | CWE-942: Permissive Cross-domain Policy with Untrusted Domains |
| IDOR | CWE-639: Authorization Bypass Through User-Controlled Key |
| Broken Access Control | CWE-862: Missing Authorization |
| Authentication weaknesses | CWE-287: Improper Authentication |
| Session weaknesses | CWE-384: Session Fixation |
| Rate-limit weakness | CWE-307: Improper Restriction of Excessive Authentication Attempts |
| Exposed secrets | CWE-798: Use of Hard-coded Credentials |
| Weak credential handling | CWE-522: Insufficiently Protected Credentials |
| Information disclosure | CWE-200: Exposure of Sensitive Information to an Unauthorized Actor |
| Unsafe file upload | CWE-434: Unrestricted Upload of File with Dangerous Type |
| GraphQL security weaknesses | CWE-285: Improper Authorization |
| WordPress or CMS vulnerabilities | Depends on the specific vulnerability; common mappings include CWE-79, CWE-89, CWE-22, CWE-434 and CWE-862 |

### Example

If SQLMap detects a parameter vulnerable to SQL injection, the finding can be represented as:

```text
Title: SQL Injection
Category: Injection
CWE: CWE-89
Severity: High or Critical
Affected URL: Target endpoint
Evidence: Request, parameter, response, and detection result
Remediation: Use parameterized queries and server-side input validation
```

The project also maps severities to OWASP-related classifications through `owasp_mapper.py`.

---

## 4. How the actual orchestrator engine works

The main orchesator is implemented in `orchestrator.py`.

The orchestrator is responsible for converting one scan request into a sequence of distributed Celery tasks.

### Step 1: Scan creation

The frontend sends a request to:

```text
POST /api/scans
```

The request contains:

```json
{
  "name": "Authorized scan",
  "target": "https://example.com",
  "selected_attack_categories": [
    "recon.subdomain_enum",
    "enum.crawling",
    "vuln.nuclei_scan"
  ]
}
```

The FastAPI route:

1. Validates the request with Pydantic.
2. Checks for unsafe input.
3. Normalizes the target.
4. Checks target authorization.
5. Persists the scan.
6. Creates a workflow record.
7. Dispatches background work.

### Step 2: Stage selection

The orchestrator has predefined stage maps:

```python
FULL = [
    "workers.recon.run",
    "workers.enum.run",
    "workers.vuln.run",
    "workers.report.run",
]
```

Other modes include:

```python
RECON_ONLY
VULN_ONLY
QUICK
```

The selected attack categories are translated into worker stages.

For example:

```text
recon.subdomain_enum → workers.recon.run
enum.crawling        → workers.enum.run
vuln.nuclei_scan     → workers.vuln.run
```

The report worker is normally included after the security stages.

### Step 3: Decision engine

The project contains a rule-based decision engine in `decision_engine.py`.

The engine stores rules in registration order:

```text
predicate(context) → action
```

The context may contain:

```python
{
    "scan_id": 22,
    "target": "https://example.com",
    "scan_type": "FULL"
}
```

The first matching rule determines the stage list.

This is not a machine-learning model. It is deterministic rule-based orchestration.

### Step 4: Celery task construction

The orchestrator creates Celery task signatures. Each task receives:

- Scan ID
- Target
- Selected categories where applicable
- Git options where applicable
- A generated task ID
- A queue assignment

Example queue mapping:

```text
workers.recon.run → recon_queue
workers.enum.run  → enum_queue
workers.vuln.run  → vuln_queue
workers.git.run   → secrets_queue
workers.report.run → report_queue
```

### Step 5: Task chaining

When multiple stages exist, the orchestrator builds a Celery chain.

Conceptually:

```text
Recon → Enumeration → Vulnerability → Report
```

The first task is submitted to Redis/Celery. Later tasks are linked as continuation tasks.

### Step 6: Workflow persistence

Before dispatch, the orchestrator persists:

- Workflow status
- Task names
- Task IDs
- Queue information
- Initial task state

The workflow state is stored in either:

- PostgreSQL in the active deployment
- JSON files in development/test fallback mode

The persistence logic is implemented in `workflow_store.py`.

### Step 7: Failure and fallback behavior

The orchestrator checks whether the broker is reachable before dispatching. It also uses retry/fallback logic to handle transient task-publishing failures.

If a task cannot be dispatched, the workflow is marked as failed rather than incorrectly reported as successful.

---

## 5. How workers work and communicate

The worker system is implemented with Celery and Redis.

### Worker architecture

The project runs separate worker services:

```text
worker_recon
worker_enum
worker_vuln
worker_secrets
worker_report
```

Each worker listens to a dedicated queue.

For example, the Docker configuration maps:

```text
recon_queue  → worker_recon
enum_queue   → worker_enum
vuln_queue   → worker_vuln
report_queue → worker_report
```

The configuration is in `docker-compose.yml`.

### Communication flow

```text
Frontend
   ↓ HTTP JSON
FastAPI backend
   ↓ Celery message
Redis broker
   ↓ queue routing
Dedicated Celery worker
   ↓
Security tool process
   ↓
Worker result
   ↓
PostgreSQL workflow/result tables
   ↓
Frontend API and WebSocket
```

### Worker lifecycle

Celery lifecycle signals are registered in `celery_app.py`.

Important lifecycle events include:

- `task_prerun`
- `task_postrun`
- `task_failure`

When a task starts:

```text
queued → running
```

When it succeeds:

```text
running → completed
```

When it fails:

```text
running → failed
```

When a task is cancelled:

```text
running → cancelled
```

The lifecycle state is persisted using `progress.py`.

### Tool execution inside a worker

A worker creates a `PluginInput` object:

```python
PluginInput(
    scan_id=scan_id,
    target=target,
    task_id=task_id,
    timeout=300
)
```

The plugin executor then:

1. Finds the plugin by name.
2. Builds the command.
3. Starts the process with `subprocess.Popen`.
4. Captures stdout and stderr.
5. Continuously drains both streams using threads.
6. Checks timeout and cancellation.
7. Terminates the process group if required.
8. Parses the output.
9. Stores the normalized result.

### Why stdout and stderr are drained separately

A subprocess can deadlock if one pipe buffer becomes full while the parent waits for the other pipe.

The executor avoids this by continuously reading both streams in separate daemon threads.

This is especially important for tools such as Amass, Nuclei and Katana, which can produce a large amount of output.

### Worker-to-frontend communication

Workers persist results to the workflow store. The backend exposes those results through API routes such as:

```text
GET /api/scans/{scan_id}/workflow
GET /api/scans/{scan_id}/results
GET /api/reports/{scan_id}
```

The project also publishes live lifecycle events over Redis/WebSocket, including:

```text
scan.started
tool.started
tool.completed
scan.completed
scan.failed
```

---

## 6. Algorithms used in the project

### 6.1 Rule-based decision algorithm

The decision engine evaluates predicates sequentially:

```text
for each rule:
    if predicate(context) is true:
        return associated action
```

This gives deterministic routing behavior.

Complexity:

```text
O(R)
```

where `R` is the number of registered rules.

### 6.2 Plugin discovery algorithm

The plugin registry scans the Python package directory, imports modules, and checks whether each module contains:

- Plugin metadata
- A `Plugin` class

Utility modules without executable plugin classes are excluded.

This prevents helper modules from being incorrectly counted as tools.

### 6.3 Target normalization algorithm

The target authorization code:

1. Removes surrounding whitespace.
2. Lowercases hostnames.
3. Parses HTTP and HTTPS URLs.
4. Validates schemes.
5. Rejects credentials in URLs.
6. Rejects query strings and fragments for authorization records.
7. Extracts hostname and port.
8. Validates domains and IP addresses.
9. Rejects private or non-routable public targets.
10. Compares normalized host/port values.

For ordinary web paths:

```text
https://example.com/app/login
```

the authorization scope is:

```text
example.com
```

For a port-specific target:

```text
https://example.com:8443/app/login
```

the authorization scope is:

```text
example.com:8443
```

### 6.4 URL parsing

The project uses Python URL parsing functions such as:

```python
urlsplit()
urlparse()
```

These are used by:

- Target validation
- Git repository validation
- Tool command construction
- Host and port extraction

### 6.5 Deduplication algorithm

Findings are deduplicated using identity keys such as:

```text
(title, affected_url)
```

Subdomains are deduplicated using a set:

```python
subs = set()
```

This gives average-case lookup complexity of:

```text
O(1)
```

per insertion.

### 6.6 Finding validation algorithm

The vulnerability validator calculates a confidence score from:

- Evidence presence
- Severity impact
- Evidence length
- False-positive heuristics

Conceptually:

```text
confidence =
    reproducibility score
    + impact score
    + evidence quality
    + false-positive score
```

The result is normalized and filtered.

This is a heuristic algorithm, not a trained machine-learning classifier.

### 6.7 State machine algorithm

The state machine stores valid transitions:

```text
current state → next state
```

Invalid transitions raise an exception.

This prevents illegal lifecycle changes such as:

```text
cancelled → completed
```

### 6.8 JWT authentication

Authentication uses signed JSON Web Tokens.

The backend:

1. Validates username and password.
2. Creates a JWT.
3. Signs it with the configured secret.
4. Sends it to the frontend.
5. The frontend sends it in the `Authorization` header.
6. FastAPI middleware verifies the token.

### 6.9 Password hashing

Passwords are not stored as plaintext. The authentication layer uses Passlib and bcrypt-compatible hashing.

The general model is:

```text
password → salted hash → stored credential
```

During login:

```text
submitted password → verify against stored hash
```

### 6.10 Timeout algorithm

Every subprocess receives a deadline:

```python
deadline = current_time + timeout
```

The executor periodically checks:

```text
if current_time >= deadline:
    terminate process
    mark tool as timed out
```

### 6.11 Process-group cancellation

The executor starts processes in a new session. This allows the system to terminate the entire process group rather than only the parent process.

This is important for tools that create child processes.

### 6.12 External crawler and scanner algorithms

The integrated third-party tools internally use their own algorithms:

- Katana: depth-limited web crawling, generally depth-first or breadth-first
- Nmap: service discovery and version probing
- RustScan: asynchronous high-speed port scanning
- Naabu: optimized TCP port scanning
- FFUF: wordlist-based request generation
- Nuclei: template-driven request execution and matcher evaluation
- SQLMap: SQL injection detection and database fingerprinting techniques
- Subfinder: passive source aggregation
- Amass: asset discovery and graph-oriented enumeration
- WhatWeb: HTTP fingerprinting and signature matching

The AgentSec AI project controls their execution, scope, limits and result collection. It does not reimplement the internal scanning algorithms of those tools.

---

## 7. Python libraries used

The main dependency list is in `requirements.txt`.

### Web framework

- `fastapi`
- `uvicorn`
- `python-multipart`

FastAPI provides API routing, validation and dependency injection. Uvicorn runs the ASGI application.

### Data validation and configuration

- `pydantic`
- `pydantic-settings`
- `python-dotenv`

These libraries validate request models and load environment configuration.

### Database

- `sqlalchemy`
- `asyncpg`
- `alembic`

SQLAlchemy provides ORM/database access. AsyncPG provides asynchronous PostgreSQL communication. Alembic supports migrations.

### Distributed task processing

- `celery`
- `redis`
- `kombu`

Celery executes background tasks. Redis acts as broker, result backend and event transport. Kombu supports messaging transport abstraction.

### Authentication and cryptography

- `python-jose`
- `cryptography`
- `passlib`
- `bcrypt`

These support JWT signing, token verification, secure password hashing and cryptographic operations.

### HTTP and network communication

- `httpx`
- `aiohttp`
- `dnspython`

These support asynchronous HTTP requests, public source retrieval and DNS-related operations.

### AI/LLM dependencies

- `openai`
- `anthropic`

These packages are present for future or optional provider integration. The current AI status endpoint reports that no LLM provider is wired into the scan workflow.

### Reports and templating

- `weasyprint`
- `pydyf`
- `jinja2`

WeasyPrint generates PDFs. Jinja2 supports templating. Pydyf is used by the PDF rendering dependency chain.

### Data and utilities

- `python-dateutil`
- `ujson`
- `loguru`

These support date processing, JSON operations and logging.

### Testing

- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `factory-boy`
- `fakeredis`
- `respx`

These support unit tests, asynchronous tests, coverage, test data generation, Redis mocking and HTTP mocking.

---

## 8. Why intelligence is used in the project

The project uses “intelligence” in several different senses.

### 8.1 Security intelligence

The platform combines outputs from many tools:

```text
subdomains
DNS records
ports
technologies
URLs
directories
vulnerabilities
secrets
cloud assets
```

This provides broader situational awareness than using one scanner alone.

### 8.2 Orchestration intelligence

The decision engine selects stages based on:

- Scan type
- Target
- Selected attack categories
- Workflow state

This avoids running unnecessary tools.

### 8.3 Finding intelligence

The platform normalizes raw tool output into common fields:

```text
title
severity
status
affected_url
description
evidence
task_id
scan_id
```

This makes different scanners comparable.

### 8.4 Risk intelligence

The report layer adds:

- Severity
- CWE-related classification
- OWASP mapping
- Evidence
- Remediation
- Failed checks
- Coverage limitations
- Tool versions
- Execution timeline

### 8.5 AI/LLM status

The current implementation does **not** have a fully operational LLM-powered OSINT or analysis pipeline.

The project includes:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
```

and the corresponding Python SDKs, but `ai_status.py` currently reports that no LLM analysis provider is wired into the scan workflow.

Therefore, the technically accurate statement for the presentation is:

> AgentSec AI currently uses rule-based orchestration, security-tool intelligence and evidence aggregation. LLM integration is prepared at the dependency and configuration level but is not yet connected to the active scan workflow.

### 8.6 Payload intelligence

The payload intelligence service in `payload_intel.py` retrieves bounded samples from public sources such as:

- SecLists
- PayloadsAllTheThings

It caches and attributes these sources. This is security payload intelligence, not autonomous AI reasoning.

---

## 9. What is the technology stack?

### Frontend

- React
- Vite
- JavaScript/JSX
- React Router
- Lucide React
- Force Graph visualization
- CSS-based interface

The frontend communicates with the backend using REST APIs and WebSockets.

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- AsyncPG

### Task and worker system

- Celery
- Redis
- Kombu
- Separate queue-specific worker containers

### Database

- PostgreSQL 16
- SQLAlchemy ORM
- AsyncPG driver
- JSON fallback storage for tests/development

### Security tools

- Go-based ProjectDiscovery tools
- Python-based tools
- Ruby-based WPScan
- Native Linux utilities such as Nmap, SQLMap and WhatWeb

### Reports

- Markdown
- JSON
- PDF through WeasyPrint
- Jinja2-related templating support

### Deployment

- Docker
- Docker Compose
- Nginx
- Linux containers
- Persistent PostgreSQL volume
- Persistent Redis volume

### Observability and operations

- Flower for Celery monitoring
- Structured workflow lifecycle events
- WebSocket live event stream
- Health and readiness endpoints
- Tool preflight checks

---

## 10. What is FastAPI and how is it implemented?

FastAPI is a modern Python web framework for building APIs using Python type hints.

It is built on:

- Starlette for the web/ASGI layer
- Pydantic for validation and serialization
- ASGI for asynchronous request handling

### FastAPI application creation

The application is created in `main.py`.

The application:

1. Creates the FastAPI instance.
2. Registers middleware.
3. Initializes the database during application lifespan.
4. Registers API routers.
5. Exposes health endpoints.

Conceptually:

```python
app = FastAPI(
    title="AgentSec AI",
    lifespan=lifespan
)
```

### Lifespan initialization

The lifespan function initializes database structures before serving requests:

```python
@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield
```

### Router architecture

The project separates API functionality into routers:

- Authentication
- Scans
- Targets
- Reports
- Findings
- Workflow
- Tasks
- Plugins
- Dashboard
- Database status
- AI status
- Payload intelligence
- WebSockets

The routers are included through `router.py`.

### Pydantic validation

For example, `ScanCreateRequest` validates:

- Scan name
- Target
- Attack categories
- Git options

Invalid categories are rejected using the authoritative attack catalog.

### Authentication middleware

The middleware in `main.py` protects API routes.

It:

1. Checks whether authentication is enabled.
2. Allows public health and authentication routes.
3. Requires a Bearer token for protected routes.
4. Decodes the JWT.
5. Rejects invalid or expired tokens with HTTP 401.

### Asynchronous request handling

FastAPI endpoints are declared using:

```python
async def
```

This allows the application to perform non-blocking operations while waiting for:

- PostgreSQL
- Redis
- HTTP APIs
- Background workflow operations

### Scan endpoint

The scan endpoint:

```text
POST /api/scans
```

performs:

1. Request validation
2. Target normalization
3. Authorization verification
4. Rate-limit checking
5. Database persistence
6. Workflow initialization
7. Celery task dispatch

### Health endpoints

The application provides:

```text
GET /health
GET /health/ready
```

`/health` confirms that the process is responding.

`/health/ready` verifies that the backend can connect to PostgreSQL.

### WebSocket endpoint

The frontend receives live scan events through a WebSocket route. Events include tool start, tool completion, workflow updates and errors.

### Why FastAPI is suitable here

FastAPI is suitable because it provides:

- High-performance asynchronous APIs
- Automatic OpenAPI documentation
- Strong request validation
- Type-safe data models
- Easy integration with async PostgreSQL
- Easy integration with Celery and Redis
- WebSocket support
- Clear separation through routers

---

# Important technical limitations to mention honestly

These points may be asked during the presentation:

1. **AI OSINT is not fully implemented as an LLM-powered workflow.**
2. Some attack catalog categories are conceptual and do not yet map to dedicated executable plugins.
3. The system depends on external security tools and their own availability.
4. Results depend on target authorization, network access, DNS resolution and rate limits.
5. “No findings” does not always mean “secure”; it may mean a tool returned no result, was skipped, timed out or lacked coverage.
6. Nuclei uses a bounded template profile by default to avoid loading the entire template repository at once.
7. Report completeness depends on successful worker result persistence.
8. The platform is designed for authorized security testing only.

---

# Questions that may be asked during the presentation

## Architecture questions

1. Why did you choose FastAPI instead of Flask or Django?
2. Why are Celery and Redis required?
3. Why did you separate workers by queue?
4. What happens if Redis becomes unavailable?
5. What happens if a worker crashes during a scan?
6. How do you prevent one scan from blocking all other scans?
7. How do you track task-level progress?
8. How is workflow state persisted?
9. Why is PostgreSQL used instead of only JSON storage?
10. Why is JSON fallback storage present?

## Security questions

11. How do you prevent scanning unauthorized targets?
12. How are target URLs normalized?
13. How do you prevent command injection when constructing tool commands?
14. Why do you use argument arrays instead of shell command strings?
15. How are credentials prevented from appearing in logs and reports?
16. How does cancellation terminate child processes?
17. How are JWT tokens validated?
18. How are passwords stored?
19. How are private IP addresses handled?
20. How do you prevent SSRF in the platform itself?

## Tool questions

21. Why do you need multiple subdomain tools?
22. What is the difference between Nmap, Naabu and RustScan?
23. What is the difference between Gau and Waybackurls?
24. Why is Nuclei configured with limited template directories?
25. Why can a tool return zero findings even when the target is vulnerable?
26. What happens when a security tool is missing?
27. How do tool adapters normalize different output formats?
28. What is the difference between tool failure and no findings?
29. Why does Katana require depth, rate and duration limits?
30. Which tools require API keys?

## Findings and reports questions

31. How are duplicate findings removed?
32. How is severity calculated?
33. How do you map findings to CWE and OWASP?
34. How do you preserve raw evidence?
35. How do you generate PDF reports?
36. What happens when a worker returns findings but persistence fails?
37. How do you distinguish failed, skipped and successful checks?
38. How do you prove that a finding belongs to a specific scan?
39. What information is included in the report timeline?
40. Does a report with zero findings mean the target is secure?

## AI and intelligence questions

41. Is the system actually using artificial intelligence?
42. Where are OpenAI or Anthropic used?
43. Is AI OSINT fully implemented?
44. What is the difference between rule-based intelligence and machine learning?
45. How could an LLM be integrated in the future?
46. How would you prevent an LLM from inventing findings?
47. How would you validate LLM-generated remediation?
48. How can threat intelligence improve prioritization?

## Performance and reliability questions

49. How are subprocess deadlocks prevented?
50. How are timeouts enforced?
51. How are high-volume outputs handled?
52. How do you prevent duplicate WebSocket events?
53. How does the system recover from Celery retries?
54. What happens when a scan is cancelled?
55. How do you test real tool execution?
56. What is the current limitation of the local test environment?
57. How would you scale the project for multiple users?
58. How would you implement horizontal worker scaling?
59. How would you monitor production failures?
60. What improvements would you implement next?

## Strong short answer for the most difficult question

If asked, “Is this truly an AI security scanner?”, the technically accurate response is:

> The current platform is an intelligent security orchestration and evidence aggregation system. It combines multiple security scanners, applies rule-based workflow decisions, normalizes findings, validates evidence, tracks distributed execution and generates structured reports. The project includes OpenAI and Anthropic dependencies and configuration support, but a production LLM analysis provider is not yet connected to the active scan workflow. Therefore, the current intelligence layer is primarily deterministic orchestration and security-data correlation, with LLM integration planned as a future extension.

