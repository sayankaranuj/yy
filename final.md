# PHASE 13 (REWRITE) — TRINETLAYER-CLASS OPERATOR CONSOLE FRONTEND

*A complete frontend rebuild prompt — paste into VS Code GitHub Copilot / Copilot Chat as one continuous brief. This replaces the earlier minimal "breach console" direction with a full operator-grade platform: deep per-agent pages, live attack selection, a real streaming terminal, open-source wordlist/payload integration, and a loud, color-rich, heavily animated hacker aesthetic — while every single button still does real work against the real backend.*

---

## 0. MASTER CONTEXT — READ FIRST

```
You are rebuilding the ENTIRE frontend of AgentSec AI — an
autonomous AI-driven attack surface management and pentesting
platform (FastAPI + Celery + PostgreSQL + Redis backend already
built in Phases 0-12, 14-16). The backend is NOT changing. Every
screen you build must call REAL existing endpoints from Phase 10's
REST API and Phase 10's WebSocket — nothing in this rebuild is
allowed to be a static mockup. If a feature needs a backend endpoint
that doesn't exist yet, you generate that endpoint too (small,
additive, following the exact same FastAPI/SQLAlchemy/Celery
patterns already established in backend/api/ and backend/workers/).

REFERENCE PRODUCT (what "trinetlayer-class" means):
The product you are matching the bar of is a professional recon/
secret-scanning SaaS with: a dashboard showing recent scans, an
activity feed, findings-by-severity breakdown, top affected domains,
a dedicated tool page per capability (e.g. "GhostJS" — their JS
secret scanner — with its own feature list, its own scan console,
its own live counters: Live hosts / JS scanned / Packages / Findings
ticking up in real time), and a dedicated page per attack class
(e.g. "Dependency Confusion") with its own live counters and its
own scan trigger. The pattern to copy: EVERY agent and EVERY attack
category in AgentSec AI gets this same treatment — its own URL, its
own live console, its own feature breakdown, its own trigger button,
its own real-time counters — not buried inside one generic scan
page.

WHAT THIS PHASE BUILDS:
1. A full navigation rebuild — every agent (Recon, Enumeration,
   Vulnerability, Secret & Cloud, Exploitation, Strix, Reporting)
   gets its own top-level route with its own deep sub-pages.
2. An "Attack Selector" — before a scan starts, the user can
   deselect any individual check/tool (checkbox tree, not just
   scan-type radio buttons) so they can run ONLY SQLi, or ONLY
   subdomain takeover checks, etc.
3. A real, streaming, full-screen Live Terminal view that renders
   actual stdout/stderr lines from the currently-running tool,
   not a simulated log.
4. A per-agent "Live Operations" page: shows which specific attack
   is executing RIGHT NOW, the exact payload/wordlist entry being
   tried, which tool process is alive, and a running counter of
   attempts.
5. Open-source data integration: real payload/wordlist data pulled
   from public GitHub repositories (SecLists, PayloadsAllTheThings,
   known-breach-safe test credential lists) to drive the
   credential-stuffing and injection-testing displays with
   authentic-looking real attempted values — not placeholder
   "test123" junk.
6. A complete visual overhaul: dense, colorful, high-motion "hacker
   operator" aesthetic — NOT the restrained minimal system from the
   earlier design phase. Think a cross between a SOC dashboard, a
   CTF scoreboard, and a terminal multiplexer. Saturated multi-color
   severity/category palette, particle/grid backgrounds, glitch and
   scan-line motion used liberally (but still respecting
   prefers-reduced-motion and WCAG flash limits), animated data
   flow lines between nodes, and a custom cursor/crosshair on
   targeting screens.
7. EVERY single interactive element must be wired to a real backend
   call. No decorative buttons. If a button says "Run SQLi Only,"
   clicking it must actually dispatch a real scoped Celery task
   through a real new or existing endpoint.

NON-NEGOTIABLE ENGINEERING RULES (carried over from every prior
phase of this project — do not relax these just because the visual
brief changed):
- Every tool failure still returns a PluginOutput, never an
  exception. Nothing in this frontend rebuild changes backend
  failure semantics.
- Private IPs, localhost, cloud metadata IPs still rejected at
  validation. The Attack Selector CANNOT be used to bypass target
  scope validation.
- EXPLOIT_AGENT_ENABLED and STRIX_AGENT_ENABLED still default False.
  The frontend must clearly gray out / lock those two agent pages
  behind their existing safety gates (org scope confirmation modal,
  same as Phase 12) rather than hiding the gate.
- The credential-stuffing / injection "real data from open source"
  requirement (Section 5) must NEVER be used against a live target
  without the user explicitly starting an authorized scan — this is
  display/wordlist content for an authorized Classic/Hybrid/
  Autonomous scan already gated by the existing scope rules, not a
  bypass of them.

TECH STACK ADDITIONS FOR THIS REBUILD:
  react-router-dom@6        (deep nested routing — already present,
                              now actually used for nested agent routes)
  framer-motion             (motion layer, used MUCH more liberally
                              than before)
  three.js + @react-three/fiber + @react-three/drei
                              (3D backgrounds, node graphs, globe)
  xterm.js + xterm-addon-fit (REAL terminal emulator component —
                              not a styled <div> log, an actual
                              terminal buffer)
  recharts                  (all charts/graphs)
  d3-force                  (force-directed attack graph layout)
  react-syntax-highlighter  (payload/code display)
  canvas-confetti           (impact bursts)
  zustand                   (already present — extend for
                              attack-selection + live-ops state)

Install:
  npm install framer-motion three @react-three/fiber @react-three/drei
             xterm xterm-addon-fit recharts d3-force
             react-syntax-highlighter canvas-confetti

Token rule — generate in this exact order, wait for "next" after
each step, never skip ahead:
  Step 1:  Open-source payload/wordlist ingestion service (backend)
  Step 2:  Attack Selector data model + API (backend)
  Step 3:  Live Operations WebSocket event extensions (backend)
  Step 4:  Design tokens — full color system + motion primitives
  Step 5:  Routing architecture (the full sitemap)
  Step 6:  Shared "Operator UI" component kit
  Step 7:  Live Terminal component (xterm.js integration)
  Step 8:  Global Command Center (new home dashboard)
  Step 9:  Attack Selector screen (pre-scan configuration)
  Step 10: Live Operations — Recon Agent page
  Step 11: Live Operations — Enumeration Agent page
  Step 12: Live Operations — Vulnerability Agent page (+ per-attack
           sub-pages: SQLi, XSS, SSRF, IDOR, Auth/Credential, CORS,
           GraphQL, etc.)
  Step 13: Live Operations — Secret & Cloud Agent page
  Step 14: Live Operations — Exploitation Agent page (gated)
  Step 15: Live Operations — Strix Autonomous Agent page (gated)
  Step 16: Live Operations — Reporting Agent page
  Step 17: Global Attack Graph (3D/force-directed cross-agent view)
  Step 18: Findings, Reports, Monitoring pages (restyled to new system)
  Step 19: Final verification
```

---

## STEP 1 — Open-Source Payload/Wordlist Ingestion Service

```
STEP 1

Generate: backend/services/payload_intel.py
          backend/api/payload_intel.py
          str_replace addition to backend/config/settings.py

CONTEXT:
The frontend needs to show REAL, recognizable attack payloads and
credential lists when displaying "what the tool is about to try" —
not invented strings. This step builds a backend service that
fetches and caches real open-source security testing datasets from
public GitHub repositories, so the Vulnerability Agent's live pages
can show actually-real entries (e.g. real rockyou-derived common
password samples, real SQLi payload strings from
PayloadsAllTheThings, real XSS polyglot strings, real subdomain
wordlist samples from SecLists) as the "currently trying" value in
the Live Terminal and the attempt counters.

CRITICAL SAFETY NOTE: this data is for DISPLAY/DRIVING THE EXISTING
TOOLS (ffuf wordlists, sqlmap payload lists, Hydra candidate lists)
that Phase 3-6 already wrap — it does not grant new capability. The
tools already send these kinds of payloads; this step only makes
the data driving them visible, real, and attributable, instead of
Lorem-ipsum placeholder text in the UI.

─────────────────────────────────────────

payload_intel.py:

PayloadSource dataclass:
  name: str          # e.g. "SecLists - Common Credentials"
  repo_url: str       # e.g. "https://github.com/danielmiessler/SecLists"
  raw_file_url: str   # direct raw.githubusercontent.com URL
  category: str       # "credentials" | "sqli" | "xss" | "subdomains"
                      # | "lfi" | "ssrf" | "api_wordlist"
  license: str        # license of the source repo, always display this
  cached_at: datetime | None
  entry_count: int

PayloadIntelService class:

SOURCES = [
  PayloadSource(
    name="SecLists — Top 1000 Common Passwords",
    repo_url="https://github.com/danielmiessler/SecLists",
    raw_file_url=(
      "https://raw.githubusercontent.com/danielmiessler/"
      "SecLists/master/Passwords/Common-Credentials/"
      "10-million-password-list-top-1000.txt"
    ),
    category="credentials",
    license="MIT"
  ),
  PayloadSource(
    name="SecLists — Top Usernames",
    repo_url="https://github.com/danielmiessler/SecLists",
    raw_file_url=(
      "https://raw.githubusercontent.com/danielmiessler/"
      "SecLists/master/Usernames/top-usernames-shortlist.txt"
    ),
    category="credentials",
    license="MIT"
  ),
  PayloadSource(
    name="PayloadsAllTheThings — SQL Injection",
    repo_url="https://github.com/swisskyrepo/PayloadsAllTheThings",
    raw_file_url=(
      "https://raw.githubusercontent.com/swisskyrepo/"
      "PayloadsAllTheThings/master/SQL%20Injection/"
      "Intruder/exploit/Generic_SQLI.txt"
    ),
    category="sqli",
    license="MIT"
  ),
  PayloadSource(
    name="PayloadsAllTheThings — XSS Polyglots",
    repo_url="https://github.com/swisskyrepo/PayloadsAllTheThings",
    raw_file_url=(
      "https://raw.githubusercontent.com/swisskyrepo/"
      "PayloadsAllTheThings/master/XSS%20Injection/"
      "Intruders/XSS_Polyglots.txt"
    ),
    category="xss",
    license="MIT"
  ),
  PayloadSource(
    name="SecLists — Subdomains Top 5000",
    repo_url="https://github.com/danielmiessler/SecLists",
    raw_file_url=(
      "https://raw.githubusercontent.com/danielmiessler/"
      "SecLists/master/Discovery/DNS/"
      "subdomains-top1million-5000.txt"
    ),
    category="subdomains",
    license="MIT"
  ),
  PayloadSource(
    name="SecLists — LFI Payloads",
    repo_url="https://github.com/danielmiessler/SecLists",
    raw_file_url=(
      "https://raw.githubusercontent.com/danielmiessler/"
      "SecLists/master/Fuzzing/LFI/LFI-Jhaddix.txt"
    ),
    category="lfi",
    license="MIT"
  ),
  PayloadSource(
    name="SecLists — Common API Endpoints",
    repo_url="https://github.com/danielmiessler/SecLists",
    raw_file_url=(
      "https://raw.githubusercontent.com/danielmiessler/"
      "SecLists/master/Discovery/Web-Content/api/"
      "api-endpoints.txt"
    ),
    category="api_wordlist",
    license="MIT"
  ),
]

fetch_and_cache(source: PayloadSource) → async → list[str]:
  STEP 1: Check Redis cache first
    key = f"agentsec:payload_intel:{source.category}:{source.name}"
    cached = await redis.get(key)
    If cached: return json.loads(cached)

  STEP 2: Fetch from GitHub raw content via httpx
    response = await httpx.AsyncClient().get(
      source.raw_file_url, timeout=15,
      headers={"User-Agent": "AgentSec-AI-Intel/1.0"}
    )
    If response.status_code != 200:
      Log warning, return a small built-in fallback list for
      that category (never let a GitHub outage break the UI)
    
    lines = [l.strip() for l in response.text.splitlines()
             if l.strip() and not l.startswith("#")]
    
    Limit to first 2000 lines (these files can be huge —
    we only need representative samples for display + for
    feeding into the already-timeout-bounded tool wrappers)

  STEP 3: Cache in Redis
    await redis.set(key, json.dumps(lines), ex=86400)
      # 24h cache — these public wordlists don't change often

  Return lines

get_sample(category: str, count: int = 20) → async → list[str]:
  Picks `count` random entries from the cached/fetched list for
  that category — used to populate "recently attempted" style
  displays without dumping the whole file into every API response.

get_source_metadata(category: str) → PayloadSource:
  Returns the PayloadSource object (name, repo_url, license) so the
  UI can always show proper attribution — "Sourced from SecLists
  (MIT License) — github.com/danielmiessler/SecLists" — never present
  this data without crediting its origin, both out of correctness
  and because it's good practice to make clear these are public,
  well-known test lists, not secret research.

refresh_all_sources() → async → dict:
  Celery-beat-triggered daily task (add to Phase 16's existing
  beat_schedule.py in the same pattern as check_due_monitors):
    fetch_and_cache() for every SOURCES entry, refreshing the cache
    before it expires, so the UI never has to block on a live
    GitHub fetch during an active scan.

─────────────────────────────────────────

payload_intel.py API router:

GET /api/v1/intel/sources:
  Returns list of all PayloadSource metadata (name, repo_url,
  category, license, entry_count, cached_at) — powers an "Open
  Source Intelligence" credits panel in the UI.

GET /api/v1/intel/sample/{category}:
  Query param: count (default 20, max 100)
  Returns: {category, source: PayloadSource, samples: [str, ...]}
  Used by the live Vulnerability Agent pages to show real payload
  strings as "currently trying: ' OR '1'='1' --" style ticker
  entries, sourced from PayloadsAllTheThings.

Add router to app_factory.py under /api/v1/intel, auth required.

Generate all 3 files. Stop after.
```

---

## STEP 2 — Attack Selector Data Model + API

```
STEP 2

Generate: str_replace addition to backend/models/scan.py
          backend/api/schemas.py additions
          str_replace addition to backend/api/scans.py
          str_replace addition to backend/orchestrator/decision_engine.py

CONTEXT:
Currently a scan picks tools entirely via the Decision Engine based
on scan_type/scan_mode. This step adds an EXPLICIT opt-in/opt-out
layer on top: the user can tick/untick individual checks in the
frontend's Attack Selector before launching, and that selection is
respected as a HARD FILTER over whatever the Decision Engine would
otherwise have chosen — the Decision Engine still decides WHICH of
the selected tools actually fire based on live recon data (e.g. if
the user selected "WordPress testing" but the target isn't running
WordPress, WPScan still correctly never fires) — but anything the
user explicitly excluded NEVER runs, full stop.

─────────────────────────────────────────

scan.py addition:

Add to Scan model:
  selected_attack_categories: JSON, nullable
    # null = run everything the Decision Engine would normally pick
    # (fully backward compatible — every existing scan behaves
    # identically). If set, it's a list of category keys like:
    # ["recon.subdomain_enum", "vuln.sqli", "vuln.xss",
    #  "secrets.js_extraction", "auth.credential_stuffing"]
    # and ANYTHING not in this list is hard-skipped regardless
    # of what the Decision Engine would otherwise have chosen.

─────────────────────────────────────────

schemas.py additions:

ATTACK_CATALOG = {
  # This is the full, authoritative tree the frontend's Attack
  # Selector renders as a checkbox tree. Keys here must exactly
  # match what decision_engine.py checks against.
  "recon": {
    "label": "Reconnaissance",
    "items": {
      "recon.subdomain_enum": "Subdomain Enumeration",
      "recon.dns_enum": "DNS Record Enumeration",
      "recon.whois": "WHOIS Lookup",
      "recon.asn": "ASN & IP Range Discovery",
      "recon.cert_transparency": "Certificate Transparency Mining",
      "recon.osint": "AI OSINT (ScrapeGraphAI)",
    }
  },
  "enum": {
    "label": "Enumeration",
    "items": {
      "enum.port_scan": "Port Scanning",
      "enum.live_hosts": "Live Host Detection",
      "enum.tech_fingerprint": "Technology Fingerprinting",
      "enum.crawling": "Web Crawling",
      "enum.directory_bruteforce": "Directory Brute-forcing",
      "enum.js_discovery": "JavaScript File Discovery",
    }
  },
  "vuln": {
    "label": "Vulnerability Testing",
    "items": {
      "vuln.nuclei_scan": "Nuclei Template Scan",
      "vuln.sqli": "SQL Injection",
      "vuln.xss": "Cross-Site Scripting",
      "vuln.ssrf": "SSRF",
      "vuln.lfi_rfi": "LFI / RFI",
      "vuln.ssti": "Server-Side Template Injection",
      "vuln.cmdi": "Command Injection",
      "vuln.cors": "CORS Misconfiguration",
      "vuln.idor": "IDOR / Broken Access Control",
      "vuln.graphql": "GraphQL Security Testing",
      "vuln.cms": "CMS-Specific Testing (WordPress etc.)",
    }
  },
  "auth": {
    "label": "Authentication & Authorization",
    "items": {
      "auth.credential_stuffing": "Credential Stuffing",
      "auth.jwt": "JWT Misconfiguration",
      "auth.session": "Session Cookie Security",
      "auth.oauth": "OAuth Flow Testing",
      "auth.bypass": "Authentication Bypass",
      "auth.rate_limit": "Rate Limit Testing",
    }
  },
  "secrets": {
    "label": "Secret & Cloud",
    "items": {
      "secrets.js_extraction": "JS Secret Extraction",
      "secrets.git_scan": "Git Repository Scanning",
      "secrets.file_scan": "Config/Backup File Scanning",
      "secrets.cloud_buckets": "Cloud Bucket Exposure",
      "secrets.cloud_metadata": "Cloud Metadata SSRF Checks",
    }
  },
  "exploit": {
    "label": "Exploitation (Gated)",
    "items": {
      "exploit.poc_generation": "Proof-of-Concept Generation",
      "exploit.chain_execution": "Attack Chain Execution",
    }
  },
  "ai_agent": {
    "label": "Autonomous AI Agent (Gated)",
    "items": {
      "ai_agent.strix_validation": "Strix Deep Validation",
    }
  },
}

CreateScanRequest — add field:
  selected_attack_categories: list[str] | None = None
    @field_validator: every entry must exist as a key somewhere
    in ATTACK_CATALOG's flattened items, else reject with 422
    naming the invalid key.

GET /api/v1/scans/attack-catalog:
  New simple endpoint, no auth complexity beyond standard JWT,
  returns ATTACK_CATALOG verbatim — this is literally what the
  frontend's checkbox tree renders, so adding a new check on the
  backend later automatically surfaces in the selector with zero
  frontend changes needed.

─────────────────────────────────────────

scans.py str_replace addition (inside POST / create scan):

  After existing target/mode validation, before scan creation:
    if request.selected_attack_categories is not None:
      scan_config["selected_attack_categories"] = (
        request.selected_attack_categories
      )

  When creating the Scan row:
    scan.selected_attack_categories = (
      request.selected_attack_categories
    )

─────────────────────────────────────────

decision_engine.py str_replace addition:

Add this filter as the LAST step of every decide_*_tools() method
(decide_recon_tools, decide_enum_tools, decide_vuln_tools,
decide_strix_invocation, etc.) — wrap each existing return
statement with:

  def _apply_category_filter(
    tools: list[ToolDecision],
    category_prefix: str,
    selected: list[str] | None
  ) -> list[ToolDecision]:
    if selected is None:
      return tools  # no explicit selection = unchanged behavior
    
    TOOL_TO_CATEGORY = {
      "subfinder": "recon.subdomain_enum",
      "amass": "recon.subdomain_enum",
      "dnsx": "recon.dns_enum",
      "whois_plugin": "recon.whois",
      "asnmap": "recon.asn",
      "crtsh": "recon.cert_transparency",
      "scrapegraph_plugin": "recon.osint",
      "naabu": "enum.port_scan",
      "httpx_plugin": "enum.live_hosts",
      "whatweb": "enum.tech_fingerprint",
      "katana": "enum.crawling",
      "ffuf_plugin": "enum.directory_bruteforce",
      "nuclei_plugin": "vuln.nuclei_scan",
      "sqlmap_plugin": "vuln.sqli",
      "dalfox": "vuln.xss",
      "corsy": "vuln.cors",
      "tplmap": "vuln.ssti",
      "wpscan_plugin": "vuln.cms",
      "jwt_tool_plugin": "auth.jwt",
      "trufflehog": "secrets.git_scan",
      "gitleaks": "secrets.git_scan",
      "secretfinder": "secrets.js_extraction",
      "s3scanner": "secrets.cloud_buckets",
      "cloud_enum": "secrets.cloud_buckets",
      "strix_plugin": "ai_agent.strix_validation",
      # ... full mapping, one entry per registered plugin
    }
    
    return [
      t for t in tools
      if TOOL_TO_CATEGORY.get(t.tool_name) in selected
      # tools with no mapping entry (rare internal helpers)
      # pass through unfiltered — fail open on infra tools,
      # fail closed only on user-visible attack categories
      or t.tool_name not in TOOL_TO_CATEGORY
    ]

  Apply this filter at the end of each decide_* method using the
  scan's own selected_attack_categories (passed through context).

Generate all 4 pieces. Stop after.
```

---

## STEP 3 — Live Operations WebSocket Event Extensions

```
STEP 3

Generate: str_replace additions to backend/orchestrator/event_bus.py
          str_replace additions to each worker that needs
          finer-grained event emission (recon_agent.py,
          enum_agent.py, vuln_agent.py, secret_agent.py)

CONTEXT:
Phase 2's WebSocket events (tool_started, tool_complete,
finding_found) are agent-level granularity. The Live Operations
pages for this rebuild need ATTACK-level granularity — "SQLMap is
now trying parameter `username` with payload `' OR 1=1--`" — so the
Live Terminal and per-attack counters feel truly real-time rather
than just "a tool is running."

─────────────────────────────────────────

event_bus.py additions — new Event dataclasses:

AttemptEvent(scan_id, category, tool_name, target_detail,
             payload_sample, attempt_number, total_attempts)
  # Fired on a meaningful sub-step within a tool's execution —
  # NOT every single HTTP request (that would flood the socket),
  # but every N attempts (configurable, default every 1 in 10 for
  # high-volume tools like SQLMap/ffuf, every 1 in 1 for low-volume
  # tools like Nuclei template matches)

TerminalLineEvent(scan_id, tool_name, line, stream, timestamp)
  # stream = "stdout" | "stderr"
  # This is the raw line-by-line text each plugin's subprocess
  # actually printed — piped live instead of only being captured
  # into PluginOutput.raw_output after the process exits.

AgentStatusEvent(scan_id, agent_name, status, active_category)
  # agent_name = "recon" | "enum" | "vuln" | "secrets" |
  #              "exploit" | "strix" | "report"
  # status = "idle" | "active" | "complete" | "skipped" | "failed"
  # active_category = which ATTACK_CATALOG key is currently running
  # Powers the "which agent is lit up right now" view on the
  # Global Command Center and Attack Graph pages.

─────────────────────────────────────────

base_plugin.py str_replace addition (in _execute_subprocess):

Instead of only buffering stdout/stderr until the process exits,
switch to streaming reads using asyncio.StreamReader line-by-line:

  async def _execute_subprocess_streaming(
    self, command, timeout, scan_id, tool_name
  ) → tuple[str, str, int]:
    
    proc = await asyncio.create_subprocess_exec(
      *command,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE
    )
    
    stdout_lines, stderr_lines = [], []
    
    async def _read_stream(stream, lines_buf, stream_name):
      while True:
        line = await stream.readline()
        if not line:
          break
        decoded = line.decode("utf-8", errors="replace").rstrip()
        lines_buf.append(decoded)
        
        # Publish every line to the event bus — the frontend
        # Live Terminal consumes this directly via WebSocket
        await event_bus.publish(TerminalLineEvent(
          scan_id=scan_id, tool_name=tool_name,
          line=decoded, stream=stream_name,
          timestamp=datetime.utcnow().isoformat()
        ))
    
    try:
      await asyncio.wait_for(
        asyncio.gather(
          _read_stream(proc.stdout, stdout_lines, "stdout"),
          _read_stream(proc.stderr, stderr_lines, "stderr"),
          proc.wait()
        ),
        timeout=timeout
      )
    except asyncio.TimeoutError:
      proc.kill()
      return "\n".join(stdout_lines), "TIMEOUT", -1
    
    return ("\n".join(stdout_lines), "\n".join(stderr_lines),
            proc.returncode)

  Swap the existing run() method's call from the buffered version
  to this streaming version. Behavior and return shape (PluginOutput)
  is otherwise 100% unchanged — this purely adds a live side-channel,
  it does not change what gets parsed/stored.

─────────────────────────────────────────

sqlmap_plugin.py / dalfox.py / ffuf_plugin.py str_replace addition:

For the high-volume "trying many payloads" tools specifically, add
a lightweight regex-based line classifier that, when a stdout line
matches a "testing parameter" / "payload:" style pattern specific
to that tool's own output format, also emits an AttemptEvent with
a sample of the actual payload string being tried — sourced from
the SAME payload data the tool is already using (SQLMap's own
tamper/payload files, ffuf's own wordlist file) so the "currently
trying" value shown live in the UI is literally true, not
simulated, and separately cross-referenced against
payload_intel.py's cached SecLists/PayloadsAllTheThings samples
purely for DISPLAY LABELING ("this class of payload resembles
known pattern X from PayloadsAllTheThings") — never substituting
what the real tool actually sends.

Example for sqlmap_plugin.py:
  SQLMAP_ATTEMPT_PATTERN = re.compile(
    r"testing '(?P<payload>.+?)'"
  )
  # SQLMap's own verbose output literally prints this
  
  on each stdout line, if pattern matches:
    await event_bus.publish(AttemptEvent(
      scan_id=input.scan_id, category="vuln.sqli",
      tool_name="sqlmap_plugin",
      target_detail=input.extra_params.get("url"),
      payload_sample=match.group("payload"),
      attempt_number=running_count, total_attempts=None
    ))

Generate all pieces. Stop after.
```

---

## STEP 4 — Design Tokens: Full Color System + Motion Primitives

```
STEP 4

Replace: src/index.css (full replacement)
Generate: tailwind.config.js (full replacement)
          src/styles/motion.js (framer-motion variant presets)

DESIGN DIRECTION FOR THIS REBUILD (explicitly different brief from
any prior minimal design phase): this is a MAXIMALIST, information-
dense, multi-color operator console. Every agent/attack category
gets its OWN signature color so the whole platform reads like a
color-coded wiring diagram of what's happening where. Motion is
everywhere and constant — scanning lines, pulsing nodes, flowing
particle trails between connected elements, animated counters,
glitch transitions between route changes — while still respecting
prefers-reduced-motion (disable ALL of it, not just the extreme
bits) and keeping any true strobe/flash under WCAG 2.3.1 limits
(max 3 flashes/sec, and even then only ever as a brief one-shot,
never a loop).

─────────────────────────────────────────

src/index.css:

@import url('https://fonts.googleapis.com/css2?
  family=Space+Grotesk:wght@400;500;600;700&
  family=JetBrains+Mono:wght@400;500;600;700&
  family=Chakra+Petch:wght@400;500;600;700&
  display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  /* Base surfaces — deep space, not pure flat black, slight
     blue-violet undertone so colored glows have something to
     play against */
  --bg-void:     #050410;
  --bg-base:     #0A0818;
  --bg-surface:  #0F0D22;
  --bg-elevated: #15122C;
  --bg-overlay:  #1C1838;

  --border-subtle:  rgba(255,255,255,0.06);
  --border-default: rgba(255,255,255,0.10);
  --border-strong:  rgba(255,255,255,0.20);

  --text-primary:   #F1F0FF;
  --text-secondary: #9490C4;
  --text-muted:     #514C80;

  /* ── PER-AGENT SIGNATURE COLORS ──────────────────────
     Every agent/attack-category owns one color across the
     ENTIRE app — nav icon, live-counter glow, node color in
     the attack graph, terminal prompt color, everything. */

  --agent-recon:      #00E5FF;  /* cyan — "scanning/sonar" */
  --agent-enum:       #7C4DFF;  /* violet — "mapping" */
  --agent-vuln:       #FF3D71;  /* hot pink/red — "attack" */
  --agent-auth:       #FF9100;  /* amber — "credentials" */
  --agent-secrets:    #FFD600;  /* yellow — "exposure/leak" */
  --agent-cloud:      #00E676;  /* green — "infrastructure" */
  --agent-exploit:    #D500F9;  /* magenta — "exploitation" */
  --agent-strix:      #536DFE;  /* indigo — "AI/autonomous" */
  --agent-report:     #40C4FF;  /* sky blue — "output" */

  /* Severity — kept distinct from agent colors so the two
     color systems never collide visually */
  --critical: #FF1744;
  --high:     #FF6D00;
  --medium:   #FFC400;
  --low:      #00E676;
  --info:     #2979FF;

  /* Status */
  --status-running: #00E5FF;
  --status-done:    #00E676;
  --status-failed:  #FF1744;
  --status-paused:  #FFC400;

  /* Glow intensities — used generously, these are the
     "neon operator console" signature */
  --glow-sm: 0 0 12px;
  --glow-md: 0 0 28px;
  --glow-lg: 0 0 56px;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 22px;

  --font-display: 'Space Grotesk', sans-serif;
  --font-tech:    'Chakra Petch', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html { font-size: 16px; -webkit-font-smoothing: antialiased; }

body {
  background: var(--bg-void);
  color: var(--text-primary);
  font-family: var(--font-tech);
  overflow-x: hidden;
}

h1, h2, h3, .display { font-family: var(--font-display); }
.mono { font-family: var(--font-mono); }

/* ── SCROLLBAR — glowing accent ──────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-surface); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(var(--agent-vuln), var(--agent-strix));
  border-radius: 3px;
}

/* ── GRID BACKGROUND (used on every full-screen page) ── */
.grid-bg {
  background-image:
    linear-gradient(rgba(124,77,255,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124,77,255,0.06) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* ── SCANLINE SWEEP (persistent, GPU, cheap) ─────────── */
@keyframes scanline-sweep {
  0%   { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}
.scanline-sweep {
  position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(
    to bottom, transparent, rgba(0,229,255,0.04), transparent
  );
  height: 200px;
  animation: scanline-sweep 6s linear infinite;
}

/* ── NODE PULSE (used on every "live/active" indicator) ─ */
@keyframes node-pulse {
  0%, 100% { box-shadow: 0 0 0 0 currentColor; opacity: 1; }
  70%       { box-shadow: 0 0 0 14px transparent; opacity: 0.6; }
}
.node-pulse { animation: node-pulse 1.8s ease-out infinite; }

/* ── DATA FLOW DASH (animated connecting lines) ──────── */
@keyframes flow-dash {
  to { stroke-dashoffset: -40; }
}
.flow-line {
  stroke-dasharray: 6 6;
  animation: flow-dash 1s linear infinite;
}

/* ── GLITCH (route-transition only, one-shot) ────────── */
@keyframes glitch-slice {
  0%   { clip-path: inset(0 0 100% 0); }
  10%  { clip-path: inset(20% 0 65% 0); transform: translateX(-4px); }
  20%  { clip-path: inset(55% 0 20% 0); transform: translateX(4px); }
  30%  { clip-path: inset(0 0 100% 0); transform: translateX(0); }
  100% { clip-path: inset(0 0 100% 0); }
}
.glitch-once { animation: glitch-slice 260ms steps(3,end) 1; }

/* ── TYPEWRITER CARET (terminal prompts) ─────────────── */
@keyframes caret-blink {
  0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; }
}
.caret { animation: caret-blink 1s steps(1) infinite; }

/* ── SHIMMER (loading states) ────────────────────────── */
@keyframes shimmer { 0%{background-position:-200% 0} 100%{background-position:200% 0} }

::selection { background: rgba(255,61,113,0.35); color: #fff; }

@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
  .scanline-sweep, .glitch-once, .flow-line { display: none !important; }
}

─────────────────────────────────────────

tailwind.config.js:

Map every CSS variable above into Tailwind's theme.colors
(agent.recon, agent.enum, agent.vuln, agent.auth, agent.secrets,
agent.cloud, agent.exploit, agent.strix, agent.report, plus
critical/high/medium/low/info), fontFamily.display/tech/mono,
boxShadow.glow-sm/md/lg using the --glow-* tokens combined with
currentColor, and animation entries for node-pulse, scanline-sweep,
shimmer, glitch-once. Follow the exact same structural pattern as
earlier phases' tailwind.config.js (extend, not override, base
theme) — just swap in this new richer palette and font set.

─────────────────────────────────────────

src/styles/motion.js:

Framer Motion variant presets reused across every page so motion
language stays consistent despite being used heavily:

export const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0,
    transition: { duration: 0.5, ease: [0.16,1,0.3,1] } }
}

export const staggerContainer = {
  hidden: {},
  show: { transition: { staggerChildren: 0.06 } }
}

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.92 },
  show: { opacity: 1, scale: 1,
    transition: { type: "spring", stiffness: 380, damping: 28 } }
}

export const slideFromRight = {
  hidden: { x: 480, opacity: 0 },
  show: { x: 0, opacity: 1,
    transition: { type: "spring", stiffness: 340, damping: 34 } },
  exit: { x: 480, opacity: 0, transition: { duration: 0.25 } }
}

export const routeTransition = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.15 } }
}

export const pulseGlow = (color) => ({
  animate: {
    boxShadow: [
      `0 0 0px ${color}`, `0 0 24px ${color}`, `0 0 0px ${color}`
    ]
  },
  transition: { duration: 2, repeat: Infinity, ease: "easeInOut" }
})

Generate all 3 files. Stop after.
```

---

## STEP 5 — Routing Architecture (Full Sitemap)

```
STEP 5

Generate: src/App.jsx (full replacement)
          src/routes/sitemap.js (route metadata, used by nav + breadcrumbs)

THE FULL SITEMAP THIS PHASE BUILDS:

/                                      → Global Command Center
/login, /register                     → Auth

/scans                                → Scan list
/scans/new                            → Attack Selector (pre-scan config)
/scans/:id                            → Scan overview (hub page, links out
                                         to every agent's live-ops view
                                         scoped to this scan)
/scans/:id/terminal                   → Full-screen Live Terminal
/scans/:id/graph                      → 3D/force-directed Attack Graph

/scans/:id/recon                      → Recon Agent live ops
/scans/:id/recon/subdomains           → Subdomain enum detail + live feed
/scans/:id/recon/dns                  → DNS enum detail
/scans/:id/recon/osint                → AI OSINT detail

/scans/:id/enum                       → Enumeration Agent live ops
/scans/:id/enum/ports                 → Port scan detail + live feed
/scans/:id/enum/crawl                 → Crawling detail
/scans/:id/enum/directories           → Directory brute-force detail

/scans/:id/vuln                       → Vulnerability Agent live ops (hub)
/scans/:id/vuln/sqli                  → SQL Injection live attack page
/scans/:id/vuln/xss                   → XSS live attack page
/scans/:id/vuln/ssrf                  → SSRF live attack page
/scans/:id/vuln/idor                  → IDOR live attack page
/scans/:id/vuln/cors                  → CORS live attack page
/scans/:id/vuln/graphql               → GraphQL live attack page
/scans/:id/vuln/auth                  → Auth/credential live attack page
  /scans/:id/vuln/auth/credential-stuffing  → dedicated sub-page
  /scans/:id/vuln/auth/jwt                   → dedicated sub-page

/scans/:id/secrets                    → Secret & Cloud Agent live ops
/scans/:id/secrets/js                 → JS secret extraction detail
/scans/:id/secrets/git                → Git scanning detail
/scans/:id/secrets/cloud              → Cloud bucket detail

/scans/:id/exploit                    → Exploitation Agent (gated)
/scans/:id/strix                      → Strix Autonomous Agent (gated)
/scans/:id/report                     → Reporting Agent live ops +
                                         final report viewer

/findings                             → Global findings dashboard
/findings/:id                         → Finding deep-dive

/reports                              → Reports list
/monitors                             → Continuous monitoring (Phase 16)
/monitors/:id                         → Monitor detail + diff history

/tools                                → Tool/plugin health dashboard
/intel                                → Open-source intel sources page
                                         (shows payload_intel.py sources,
                                         licenses, last refresh — the
                                         "where does this data come from"
                                         transparency page)

/analytics, /notifications, /profile,
/settings, /organization/scope        → unchanged from prior phases,
                                         restyled to new token system

─────────────────────────────────────────

App.jsx:

Use React Router v6 nested routes so every /scans/:id/* page shares
a common <ScanShell> layout (persistent top bar showing target +
live status + agent nav rail) without re-fetching scan context on
every sub-navigation.

<Route path="/scans/:id" element={<ScanShell />}>
  <Route index element={<ScanOverview />} />
  <Route path="terminal" element={<LiveTerminalFullscreen />} />
  <Route path="graph" element={<AttackGraph3D />} />
  <Route path="recon" element={<ReconAgentOps />}>
    <Route path="subdomains" element={<SubdomainDetail />} />
    <Route path="dns" element={<DNSDetail />} />
    <Route path="osint" element={<OSINTDetail />} />
  </Route>
  <Route path="enum" element={<EnumAgentOps />}>
    ...
  </Route>
  <Route path="vuln" element={<VulnAgentOps />}>
    <Route path="sqli" element={<SQLiLiveAttack />} />
    <Route path="xss" element={<XSSLiveAttack />} />
    <Route path="ssrf" element={<SSRFLiveAttack />} />
    <Route path="idor" element={<IDORLiveAttack />} />
    <Route path="cors" element={<CORSLiveAttack />} />
    <Route path="graphql" element={<GraphQLLiveAttack />} />
    <Route path="auth" element={<AuthLiveAttack />}>
      <Route path="credential-stuffing" element={<CredStuffingDetail />} />
      <Route path="jwt" element={<JWTDetail />} />
    </Route>
  </Route>
  <Route path="secrets" element={<SecretsAgentOps />}>
    ...
  </Route>
  <Route path="exploit" element={<ExploitAgentOps />} />
  <Route path="strix" element={<StrixAgentOps />} />
  <Route path="report" element={<ReportAgentOps />} />
</Route>

Wrap each <Route element> in <AnimatePresence mode="wait"> with the
routeTransition variant from motion.js so navigating between agent
pages always plays the subtle fade, and occasionally (on entering
any /vuln/* live attack page specifically) triggers the one-shot
.glitch-once class on the page's root container — this is the
"stepping into an active attack view" signature moment, deliberately
NOT applied to passive pages like /findings or /settings.

Generate both files. Stop after.
```

---

## STEP 6 — Shared Operator UI Component Kit

```
STEP 6

Generate these components in one response — this is the toolkit
every Live Operations page in Steps 10-16 is built from.

─────────────────────────────────────────

src/components/ops/AgentStatusOrb.jsx:

A circular glowing orb representing one agent's live state.
Props: agentKey ('recon'|'enum'|'vuln'|...), status, size

  Color: var(--agent-{agentKey}) always — this orb is the single
  visual anchor tying an agent to its signature color everywhere
  it appears (nav rail, Command Center, Attack Graph node).

  status === 'active':   node-pulse animation, full color, glow-md
  status === 'idle':     30% opacity, no pulse
  status === 'complete': solid color, small checkmark glyph inside
  status === 'failed':   color shifts to critical red, no pulse,
                          small X glyph inside
  status === 'skipped':  outline only, no fill (user deselected
                          this category in the Attack Selector)

  Framer-motion layoutId={`agent-orb-${agentKey}`} so this exact
  orb visually MORPHS/FLIES between the sidebar nav, the Command
  Center grid, and the Attack Graph node when navigating — this is
  the single most important motion signature of the whole rebuild,
  implement it carefully using shared layoutId across those three
  usages.

─────────────────────────────────────────

src/components/ops/LiveCounter.jsx:

Props: value, label, agentColor, icon

  Large animated number (font-mono, text-5xl/6xl), counts up with
  a quick "odometer" style digit-roll animation (framer-motion
  AnimatePresence on each digit character swapping, not just a
  linear tween — real slot-machine digit roll) every time `value`
  changes via WebSocket push, not just on mount.
  
  Label beneath in font-tech uppercase, small, tracked, colored
  at 70% opacity of agentColor.
  
  On increment: a brief colored flash-ring expands outward from
  the number and fades (scale 1→1.4, opacity 1→0, 400ms) — this
  is the "we just found something" micro-feedback, fires on every
  single WebSocket-driven value change.

─────────────────────────────────────────

src/components/ops/LiveTerminal.jsx:

THE core component — a REAL xterm.js terminal instance, not a
styled div feed. Wraps xterm + xterm-addon-fit.

Props: scanId, toolFilter (optional — show only one tool's output)

  useEffect on mount:
    const term = new Terminal({
      theme: {
        background: '#050410',
        foreground: '#F1F0FF',
        cursor: '#FF3D71',
        selectionBackground: 'rgba(255,61,113,0.3)',
      },
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: 13,
      cursorBlink: true,
      scrollback: 5000,
    })
    const fitAddon = new FitAddon()
    term.loadAddon(fitAddon)
    term.open(containerRef.current)
    fitAddon.fit()
    
    Color-code written lines by content using ANSI escape codes
    before calling term.writeln():
      [ERROR]/stderr lines  → \x1b[31m (red)
      [FOUND]/match lines   → \x1b[35m (magenta/pink — vuln color)
      [INFO] lines          → \x1b[36m (cyan — recon color)
      tool name prefixes    → bold, colored per agent signature
    
    window.addEventListener('resize', () => fitAddon.fit())

  Subscribe to the existing WebSocket connection (reuse the
  useWebSocket hook from Phase 11, extended to also expose
  `terminalLines` array sourced from the new TerminalLineEvent
  type added in Step 3). On each new line, term.writeln() it
  immediately — real streaming, not buffered/batched.

  A blinking caret-style "LIVE" badge pinned top-right of the
  terminal chrome (pulse-dot style) while the scan is RUNNING,
  turns to a static "SESSION ENDED" label once COMPLETED.

  Toolbar above the terminal: tool filter chips (one per agent
  color) to toggle which tools' lines are shown, a "Download Log"
  button (exports the full scrollback as a .txt), and a
  fullscreen-toggle icon linking to /scans/:id/terminal.

─────────────────────────────────────────

src/components/ops/AttemptTicker.jsx:

Props: category, agentColor

  A horizontally auto-scrolling marquee-style ticker (CSS
  transform translateX animation, pure CSS not JS-driven for
  performance) showing the last ~15 AttemptEvent payload_sample
  values for this category as they stream in, each rendered as a
  small pill: font-mono text-xs, agentColor-tinted background.
  
  New entries fade+slide in from the right edge, old ones scroll
  off the left — genuinely continuous motion for as long as that
  attack category is actively running, stops immediately (freezes
  on last state) the moment the category's AgentStatusEvent flips
  away from 'active'.

  Beneath the ticker: small attribution line, font-mono text-2xs
  text-muted: "payload patterns referenced from {source.name}" —
  pulled from GET /api/v1/intel/sample/{category}, satisfying the
  open-source attribution requirement directly in the live-attack
  UI itself.

─────────────────────────────────────────

src/components/ops/AttackSelectorTree.jsx:

Props: value (selected keys array), onChange

  Renders ATTACK_CATALOG (fetched from
  GET /api/v1/scans/attack-catalog) as a collapsible checkbox tree.
  Each top-level group (Reconnaissance, Enumeration, Vulnerability
  Testing, etc.) has a header in that agent's signature color with
  a "select all / none" toggle, and checkbox rows beneath for each
  individual check.
  
  The "Exploitation (Gated)" and "Autonomous AI Agent (Gated)"
  groups render with a small lock icon beside the group header and
  are visually dimmed (not disabled from being ticked, but the
  parent Attack Selector screen shows the existing org-scope-
  confirmation gate modal the instant either of those groups gets
  checked, exactly matching Phase 12's existing SCOPE_NOT_CONFIRMED
  flow — this is a frontend convenience trigger for an unchanged
  backend gate, never a bypass).

  Live entry-count badges per group (font-mono, small) showing
  "6/6 selected" style counters, updating live as checkboxes toggle.

─────────────────────────────────────────

src/components/ops/PhaseRail.jsx:

A persistent vertical rail (used inside <ScanShell>) showing all
7 agents as a connected vertical sequence of AgentStatusOrb
components joined by animated .flow-line SVG paths between
consecutive ones — the line's flow-dash animation only plays
between two agents where the upstream one is 'complete' and the
downstream one is 'active', visually showing data/control literally
flowing down the pipeline in real time. Clicking any orb navigates
to that agent's live-ops route.

Generate all 5 components. Stop after.
```

---

## STEP 7 — (folded into Step 6's LiveTerminal — proceed to Step 8)

## STEP 8 — Global Command Center

```
STEP 8

Generate: src/pages/dashboard/CommandCenter.jsx

This replaces the old User Dashboard as the app's home route (/).

─────────────────────────────────────────

BACKGROUND LAYER (entire page):
  <Canvas> from @react-three/fiber, fixed full-bleed behind
  everything else at low opacity (~0.5 overall page opacity
  applied to the canvas wrapper):
    A slowly rotating field of small glowing points representing
    every scan this org has ever run (positions pseudo-random but
    stable per scan id via a seeded hash so the field doesn't
    jitter between renders), colored by that scan's highest
    severity finding (critical=red glow, clean=dim gray). This is
    pure ambient atmosphere, not interactive, and respects
    prefers-reduced-motion (renders a single static frame if set).

─────────────────────────────────────────

TOP: HERO STRIP

  "COMMAND CENTER" — font-display text-5xl, letter-spacing tight,
  with a thin animated underline that draws itself left-to-right
  on mount (width 0% → 100%, 600ms)
  
  Right: "NEW OPERATION" button — large, bg gradient sweeping
  between agent-vuln and agent-strix colors (animated gradient
  shift, slow, continuous, subtle), routes to /scans/new

─────────────────────────────────────────

AGENT STATUS GRID (7 cards, one per agent, NOT findings-count
cards like before — this is "what's happening across every active
scan right now"):

  Each card: bg-elevated, border-top 3px solid var(--agent-{key}),
  radius-lg, glow-sm in that agent's color on hover
  
  Contains:
    AgentStatusOrb (large, layoutId shared with PhaseRail/Graph)
    Agent name, font-tech uppercase
    "{N} active across org" live count (font-mono)
    Mini sparkline (recharts) of that agent's finding-contribution
    rate over last 24h

  Clicking navigates to a new /agents/:agentKey cross-scan view
  (optional extra page — if time allows, else route to most recent
  active scan's agent page)

─────────────────────────────────────────

LIVE OPERATIONS FEED (full width, below grid):

  A single shared <LiveTerminal> component (Step 6) subscribed
  across ALL currently-running scans org-wide (not scoped to one
  scan_id — pass scanId={null} meaning "all"), so the Command
  Center shows a genuinely live multiplexed terminal of everything
  happening across the whole platform right now. This is the
  single most "hacker movie" element of the home page and should
  be given real visual weight — at least 50% of the viewport height.

─────────────────────────────────────────

BOTTOM: THREE COLUMNS

  Left: Recent Scans (font-mono target names, status orbs inline,
    risk score in severity color) — click → /scans/:id

  Center: Findings-by-severity live donut (recharts), animated
    slice-grow on mount, center shows total count large

  Right: Top Affected Domains (bar list, bars animate in width
    from 0 on load, bar fill = gradient of that domain's worst
    severity color)

Generate CommandCenter.jsx only. Stop after.
```

---

## STEP 9 — Attack Selector Screen

```
STEP 9

Generate: src/pages/scans/NewOperation.jsx

Route: /scans/new

─────────────────────────────────────────

LAYOUT: single centered column, max-width 900px, multi-step
wizard feel but all on one scrollable page (no forced pagination).

STEP A — TARGET:
  Large input, font-mono text-2xl, placeholder "example.com",
  real-time client validation using the exact same rules as the
  backend validator (instant red border + message on private
  IP/localhost before the user even submits)
  
  Scan mode selector: 3 large selectable cards (CLASSIC / HYBRID /
  AUTONOMOUS) each with that mode's own accent treatment —
  CLASSIC in neutral gray, HYBRID in a cyan→indigo gradient border,
  AUTONOMOUS in a full agent-strix indigo glow border with a small
  animated "AI" badge pulsing — selecting HYBRID/AUTONOMOUS without
  org scope confirmed immediately expands an inline (not modal)
  warning panel with a "Confirm Authorized Scope" button that
  opens the existing Phase 12 confirmation flow.

STEP B — ATTACK SELECTION:
  <AttackSelectorTree> component from Step 6, full width, this is
  the centerpiece of the page — visually large, each group
  expandable, colored by agent.

  Live summary bar pinned above the tree as it's being configured:
  "{N} checks selected across {M} agent categories" — font-mono,
  updates instantly on every toggle.

  Quick-select presets (pill buttons above the tree):
    "Full Assessment" (selects everything)
    "Recon Only"
    "OWASP Top 10 Focus"
    "Credential Security Only"
    "Quick Scan" (minimal fast subset)
  Clicking a preset animates the tree's checkboxes toggling in a
  quick staggered sequence (not instant) so the user visually sees
  what got selected rather than it just snapping.

STEP C — LAUNCH:
  A large "LAUNCH OPERATION" button, full width, height 64px,
  font-display uppercase text-xl, background is an animated
  scanning-line sweep effect across the button itself while idle
  (subtle, continuous), turns into a loading spinner + "INITIALIZING
  RECONNAISSANCE..." on click.

  On successful POST /api/v1/scans (with selected_attack_categories
  included in the payload exactly as built by the tree), navigate
  immediately to /scans/:id with a route-level glitch-once transition.

Generate NewOperation.jsx only. Stop after.
```

---

## STEP 10 — Live Operations: Recon Agent Page

```
STEP 10

Generate: src/pages/scans/agents/ReconAgentOps.jsx
          src/pages/scans/agents/recon/SubdomainDetail.jsx
          src/pages/scans/agents/recon/DNSDetail.jsx
          src/pages/scans/agents/recon/OSINTDetail.jsx

Route group: /scans/:id/recon/*
Agent color: var(--agent-recon) — cyan, throughout

─────────────────────────────────────────

ReconAgentOps.jsx (hub page at /scans/:id/recon):

HEADER: AgentStatusOrb (large) + "RECONNAISSANCE" title +
  elapsed time since this agent started (live-ticking font-mono)

LIVE COUNTER ROW (4x <LiveCounter>, cyan-tinted):
  Subdomains Found | DNS Records | ASN Ranges | Sources Queried

TOOL GRID (one tile per tool this agent runs — Subfinder, Amass,
  Assetfinder, Findomain, Chaos, dnsx, whois, ASNmap, crt.sh,
  ScrapeGraphAI):
  Each tile: tool name, small status orb (running/done/failed/
  skipped-if-deselected), a tiny live sparkline of results found
  over time, click → filters the embedded <LiveTerminal
  toolFilter={toolName}> below to just that tool's lines

EMBEDDED LIVE TERMINAL (Step 6 component, scoped to scan_id)

DISCOVERED ASSETS LIVE FEED: as subdomains stream in via
  WebSocket's asset_found events, each appears as a new row
  sliding in (framer-motion AnimatePresence, slide+fade), colored
  dot for alive/dead status, click → navigates to
  /scans/:id/recon/subdomains with that entry highlighted

Three sub-nav tabs at top (Subdomains / DNS / OSINT) linking to
the three detail pages below, each tab badge showing live count.

─────────────────────────────────────────

SubdomainDetail.jsx:

Full <DataTable> (restyled to the new token system — cyan accent
instead of the old brand purple) of every discovered subdomain,
with live row-insertion animation as new ones stream in during an
active scan. Columns: name, alive status, IP, HTTP status, source
tool (colored pill matching which recon tool found it), discovered-
at timestamp (relative, live-updating "3s ago").

A small force-directed mini-graph (d3-force, SVG) at the top
showing the root domain as a central node with discovered
subdomains branching outward, nodes appearing with a spring pop-in
animation as they're found live — this is a genuinely fun,
information-dense visualization, not decoration, since it shows
the actual shape of the discovered attack surface growing in
real time.

─────────────────────────────────────────

DNSDetail.jsx:

Table of DNS records per subdomain (A/CNAME/MX/TXT/NS), grouped,
expandable rows, syntax-highlighted raw record values
(react-syntax-highlighter, dns/plain language mode).

─────────────────────────────────────────

OSINTDetail.jsx:

Renders the ScrapeGraphAI-sourced OSINT data (Phase 7's
OSINTData) as a readable intelligence brief: company info, tech
stack keywords from job postings, team members, social links,
bug bounty program detection — styled as cards with a cyan
left-accent, each populating with a typewriter-style text reveal
animation the first time the data arrives via WebSocket.

Generate all 4 files. Stop after.
```

---

## STEP 11 — Live Operations: Enumeration Agent Page

```
STEP 11

Generate: src/pages/scans/agents/EnumAgentOps.jsx
          src/pages/scans/agents/enum/PortsDetail.jsx
          src/pages/scans/agents/enum/CrawlDetail.jsx
          src/pages/scans/agents/enum/DirectoriesDetail.jsx

Agent color: var(--agent-enum) — violet

Same structural pattern as Step 10 (header + orb, live counter
row, tool grid, embedded terminal, live feed, sub-nav tabs) but
content specific to enumeration:

LIVE COUNTER ROW: Live Hosts | Open Ports | Technologies | Endpoints

PortsDetail.jsx:
  A radial/circular port visualization (SVG, custom, not a
  library) — ports arranged around a circle 0-65535 scaled
  logarithmically, each open port lights up as a glowing dot
  colored by danger level (dangerous ports in critical red with a
  pulse, normal ports in violet), appearing live as Naabu/Nmap
  report them. Hovering a dot shows a tooltip card: port number,
  service, banner, host IP. This single visualization should feel
  like a "radar sweep" of the target's exposed surface.

CrawlDetail.jsx:
  Live-populating tree view of the crawled site structure
  (Katana's discovered URL tree rendered as an actual expandable
  file-tree UI, not a flat table) — admin paths highlighted violet-
  bold, API paths get a small "API" badge, JS files get a small
  "JS" badge linking directly to /scans/:id/secrets/js filtered to
  that file.

DirectoriesDetail.jsx:
  ffuf/feroxbuster results as a live-updating bar chart of status
  codes found (200/301/403/401 etc, recharts), plus the raw
  discovered-path list with the wordlist-attribution line from
  payload_intel.py ("wordlist sourced from SecLists") beneath it.

Generate all 4 files. Stop after.
```

---

## STEP 12 — Live Operations: Vulnerability Agent (+ Per-Attack Pages)

```
STEP 12

Generate: src/pages/scans/agents/VulnAgentOps.jsx
          src/pages/scans/agents/vuln/SQLiLiveAttack.jsx
          src/pages/scans/agents/vuln/XSSLiveAttack.jsx
          src/pages/scans/agents/vuln/SSRFLiveAttack.jsx
          src/pages/scans/agents/vuln/IDORLiveAttack.jsx
          src/pages/scans/agents/vuln/CORSLiveAttack.jsx
          src/pages/scans/agents/vuln/GraphQLLiveAttack.jsx
          src/pages/scans/agents/vuln/AuthLiveAttack.jsx
          src/pages/scans/agents/vuln/CredStuffingDetail.jsx
          src/pages/scans/agents/vuln/JWTDetail.jsx

THIS IS THE CENTERPIECE OF THE ENTIRE REBUILD — the pages the
brief specifically asked for: "a separate page of showcasing
attacks... who live attack performing information and how the
attack is getting performed."

Agent color: var(--agent-vuln) — hot pink/red (the "attack" color)

─────────────────────────────────────────

VulnAgentOps.jsx (hub at /scans/:id/vuln):

HEADER: large pulsing AgentStatusOrb in agent-vuln red, "ACTIVE
  EXPLOITATION TESTING" title in font-display, elapsed timer

ATTACK CATEGORY GRID — one large tile per attack type, each tile
  is a live-updating mini-dashboard, NOT just a static nav link:

  Each tile (SQLi, XSS, SSRF, IDOR, CORS, GraphQL, Auth, CMS,
  SSTI, CMDi, LFI/RFI):
    Top: attack name + small icon (crosshair-style icon per type)
    Status orb: idle/active/complete/skipped
    If active: live AttemptTicker (Step 6) running across the
      bottom of the tile showing real payload samples streaming by
    Live mini-counter: "{N} attempts · {M} confirmed"
    Click → navigates to that attack's dedicated full page

  Tiles for deselected categories (per Attack Selector) render
  with a "SKIPPED — not selected" diagonal stripe overlay and
  30% opacity, clearly showing the user's choice was honored.

Below the grid: embedded <LiveTerminal toolFilter="vuln"> scoped
to all vuln-category tools together.

─────────────────────────────────────────

SQLiLiveAttack.jsx (full page at /scans/:id/vuln/sqli):

This page's job: make the user feel like they're watching SQLMap
actually work, understand WHAT it's trying and WHY, in real time.

TOP: Large status banner — "SQL INJECTION TESTING" with the
  target URL(s) and parameter(s) currently being tested shown in
  a monospace readout that updates live, e.g.:
    TARGET: https://example.com/login
    PARAMETER: username
    TECHNIQUE: time-based blind
  This text block re-renders with a brief highlight flash
  whenever any field changes (new parameter, new technique).

LIVE ATTEMPT STREAM (large, center-focus):
  A vertically stacking live feed (not the compact ticker — this
  page gets the FULL detail version) of each attempt:
    [12:04:17] Trying: ' OR '1'='1' -- 
    [12:04:17] Response: 200 OK, 1842 bytes, 0.4s
    [12:04:18] Trying: ' OR SLEEP(5)--
    [12:04:23] Response: 200 OK, 1840 bytes, 5.2s  ⚠ DELAY DETECTED
  Each line color-coded (normal=secondary text, delay/anomaly
  detected=amber highlight with a small warning glyph, confirmed
  vulnerable=critical red with a glow and a brief screen-edge
  flash — ONE-SHOT only, reusing the WCAG-safe strobe pattern).
  
  New lines slide up from bottom with stagger, auto-scroll,
  pause-on-hover so the user can read a specific moment.

  Payload source attribution strip beneath: pulls from
  GET /api/v1/intel/sample/sqli — "Payload patterns referenced:
  PayloadsAllTheThings (MIT) — github.com/swisskyrepo/..." with
  a few real example strings shown as reference chips.

RIGHT SIDEBAR (30% width):
  "HOW THIS WORKS" collapsible explainer panel — plain-language,
  always available, not just on hover — explaining what SQL
  injection is, what SQLMap is doing (boolean-based / time-based /
  UNION-based techniques), written for a reader who wants to
  actually learn, not just watch. This directly supports the "user
  can understand how the attack is being performed" requirement.

  Live stats: Payloads Tried | Avg Response Time | Anomalies
  Detected | Confirmed Findings (each a <LiveCounter>)

  If a finding IS confirmed: a prominent card appears (slides in),
  severity-red bordered, with "View Full Finding →" linking to the
  standard finding detail overlay.

─────────────────────────────────────────

XSSLiveAttack.jsx:

Same structural pattern as SQLi page. Live attempt stream shows
dalfox's actual payloads (<script>alert(1)</script>, polyglot
strings sourced from payload_intel.py's XSS category). Distinctive
addition: a small sandboxed <iframe> preview area (srcdoc, fully
sandboxed, no actual execution against the real target — purely
illustrative) showing what a successful reflected-XSS payload
visually does in a browser context, for educational clarity, NOT
connected to the live target in any way.

─────────────────────────────────────────

SSRFLiveAttack.jsx:

Live stream shows which internal-looking URLs are being tried
against discovered parameters (169.254.169.254-style metadata
probes explicitly called out with a distinct icon + explanation
"testing if this server can be tricked into calling cloud
metadata services"). A simple two-node diagram (SVG, animated
connecting line) showing Attacker → Vulnerable Server → Internal
Target, with the line animating a traveling dot when a request is
"in flight."

─────────────────────────────────────────

IDORLiveAttack.jsx:

Live stream shows ID substitution attempts: "Trying
/api/users/1 → /api/users/2 ... comparing responses" with a
side-by-side diff view (two columns) highlighting what changed
between the two responses when a potential IDOR is detected.

─────────────────────────────────────────

CORSLiveAttack.jsx:

Live stream of Origin-header tests against each endpoint, shown
as a simple before/after: "Sent Origin: evil.com → Received
Access-Control-Allow-Origin: evil.com ⚠". A simple badge matrix
(endpoint × test type) filling in green/red as each combination
completes.

─────────────────────────────────────────

GraphQLLiveAttack.jsx:

If introspection succeeds, renders the discovered schema as an
interactive, collapsible tree (types → fields → arguments), with
sensitive-looking fields (anything matching password/token/secret/
key in the field name) auto-highlighted in amber. Live stream
below shows batching/aliasing attack attempts.

─────────────────────────────────────────

AuthLiveAttack.jsx (hub) + CredStuffingDetail.jsx + JWTDetail.jsx:

AuthLiveAttack.jsx: tile grid linking to the two sub-pages plus
  session-cookie and auth-bypass live feeds inline.

CredStuffingDetail.jsx — THIS IS WHERE THE OPEN-SOURCE DATA
REQUIREMENT IS MOST VISIBLE:
  Fetches GET /api/v1/intel/sample/credentials (real username/
  password samples sourced from SecLists via payload_intel.py).
  
  Renders a live "attempt table" — two columns streaming in
  together (username attempted | password attempted), each row
  sourced from the real cached SecLists data as the backend's
  Hydra/custom auth-test module actually works through them
  (respecting the existing Phase 6 safety limit of ~20 max
  attempts per endpoint — the UI must reflect that real cap, not
  imply unlimited brute-forcing).
  
  A live progress bar: "{N} of {max} candidate pairs tested"
  
  Big attribution card at top: "Candidate credentials sourced from
  SecLists' Top 1000 Common Passwords / Top Usernames lists (MIT
  License) — github.com/danielmiessler/SecLists — used here only
  to test for default/weak credentials on YOUR authorized target,
  within the platform's existing 20-attempt safety cap per
  endpoint." This attribution + safety framing must always be
  visible on this specific page, not collapsible, given it's the
  most sensitive-feeling page in the whole rebuild.

JWTDetail.jsx:
  Live stream of jwt_tool's actual test sequence (alg:none attempt,
  weak-secret dictionary attempt, RS256→HS256 confusion attempt),
  each shown with the actual before/after JWT string (header.payload
  truncated, signature redacted) using react-syntax-highlighter in
  a JSON-ish display mode so the user can literally see the token
  being manipulated.

Generate all 10 files. Stop after.
```

---

## STEP 13 — Live Operations: Secret & Cloud Agent Page

```
STEP 13

Generate: src/pages/scans/agents/SecretsAgentOps.jsx
          src/pages/scans/agents/secrets/JSDetail.jsx
          src/pages/scans/agents/secrets/GitDetail.jsx
          src/pages/scans/agents/secrets/CloudDetail.jsx

Agent color: var(--agent-secrets) — yellow, with cloud-specific
sub-sections using var(--agent-cloud) — green, so the page
visually splits into two color zones matching the two concerns.

─────────────────────────────────────────

SecretsAgentOps.jsx:

Live counter row: JS Files Scanned | Secrets Found | Repos
  Scanned | Cloud Resources Checked

Live feed: as JSSecretExtractor/TruffleHog/Gitleaks findings
  stream in, each appears as a redacted-preview card:
    Secret type badge (AWS Key / GitHub Token / JWT / etc, each
    badge a distinct hue within the yellow family so types are
    scannable at a glance)
    Truncated value: "AKIA****...EXAMPLE" (never full value,
    matching the existing backend truncation rule exactly)
    Source file/URL link
    Verification status: if the backend's SecretValidator (Phase
    7) confirmed it's LIVE, a pulsing "⚠ ACTIVE KEY" badge in
    critical red overlaid on the otherwise-yellow card — this is
    the one place yellow and red intentionally coexist, since an
    active secret genuinely is both "a secret" and "critical"

─────────────────────────────────────────

JSDetail.jsx:

Live-populating list of JS files being analyzed, each file
expandable to show a syntax-highlighted snippet (react-syntax-
highlighter, javascript language) around the exact line a secret
pattern matched, with the matched substring highlighted inline.

─────────────────────────────────────────

GitDetail.jsx:

If a .git exposure or GitHub dork hit is found, shows the exposed
file tree / commit info as a simple git-log-style monospace list.

─────────────────────────────────────────

CloudDetail.jsx (agent-cloud green theme):

Live bucket-probe feed: as S3Scanner/cloud_enum tries candidate
bucket names (generated via the existing _generate_bucket_names
heuristic from Phase 7), each candidate streams by in a ticker
similar to AttemptTicker, going green-highlighted + "EXISTS" the
moment one resolves, red-highlighted + "PUBLIC — READ" or
"PUBLIC — WRITE" if actually exposed.

A simple cloud-provider icon row (AWS/Azure/GCP) each lighting up
as that provider's checks begin.

Generate all 4 files. Stop after.
```

---

## STEP 14 — Live Operations: Exploitation Agent Page (Gated)

```
STEP 14

Generate: src/pages/scans/agents/ExploitAgentOps.jsx

Agent color: var(--agent-exploit) — magenta

GATING UI (shown whenever EXPLOIT_AGENT_ENABLED is False or the
org hasn't confirmed scope — check via a new lightweight GET
/api/v1/settings/capability-flags endpoint, or reuse existing
org/settings data already fetched):

  Full-page lock-state view: large lock icon (not a generic
  Lucide lock — render a custom SVG shield-with-lock glyph in
  magenta outline), "EXPLOITATION AGENT — LOCKED" in font-display,
  explanation text: "This capability generates proof-of-concept
  exploits for confirmed findings. It is disabled by default and
  requires organization authorization." + a "Learn More" expandable
  section explaining the safety model (exact same explanation
  content as Phase 8's safety rules, written for an end user not
  a developer) + (if the ONLY blocker is scope confirmation, not
  the global flag) a "Confirm Authorized Scope" button wired to
  the existing Phase 12 flow.

UNLOCKED STATE (when actually enabled + confirmed + this scan has
eligible critical findings):

  Live counter row: Eligible Findings | PoCs Generated | Evidence
    Files Collected | Chains Executed

  Live feed: each PoC generation attempt shown as a card —
    finding title, exploit type badge, a live-typing effect
    (character-by-character reveal, like a terminal typing out
    code) of the generated Python PoC script as it's produced,
    using react-syntax-highlighter python mode once the typing
    animation completes.

  Evidence gallery: thumbnail grid of any before/after screenshots
    EvidenceCollector captured (Phase 8), click to enlarge.

  A persistent, non-dismissible safety banner pinned to the top of
  this page at all times (not collapsible like the lock-state
  explainer): "All actions on this page are logged to the audit
  trail and scoped to non-destructive proof-of-concept generation
  only." — magenta-bordered, always visible, small font-mono text.

Generate ExploitAgentOps.jsx only. Stop after.
```

---

## STEP 15 — Live Operations: Strix Autonomous Agent Page (Gated)

```
STEP 15

Generate: src/pages/scans/agents/StrixAgentOps.jsx

Agent color: var(--agent-strix) — indigo

Same gating pattern as Step 14 (lock-state view when disabled/
unconfirmed, using the exact Phase 11/12 safety language).

UNLOCKED + RUNNING STATE:

  This page should feel distinctly "more alive" than the others —
  Strix is an actual reasoning agent, so lean into that:

  Large central element: an animated "thinking" indicator — a
  cluster of small indigo particles orbiting a central point
  (three.js, lightweight, @react-three/fiber), pulsing faster
  when AttemptEvents are arriving frequently, slower when idle —
  this is a genuine activity-rate visualization, not decoration,
  driven by actual event frequency over a rolling 5-second window.

  Live counter row: Turns Used / Max Turns | Budget Spent / Max
    Budget (rendered as a radial progress ring, not just text —
    a literal "fuel gauge" for the autonomous run) | Findings
    Discovered | Findings Corroborated

  Reasoning stream: since Strix's own internal reasoning isn't
    piped line-by-line like a simple CLI tool (it's a long-running
    agent), this section shows periodic status snapshots pulled
    from the existing StrixCompleteEvent-adjacent WebSocket pushes
    the backend already emits (ToolStartedEvent/ToolCompleteEvent
    equivalent for the strix_plugin), styled as large, spaced-out
    "log entries" rather than a dense terminal feed, since updates
    arrive far less frequently than other agents:
      "🔍 Probing authentication flow at /api/login"
      "🧪 Testing privilege escalation via role parameter"
      "✅ Confirmed: IDOR on /api/orders/{id}"
    Each entry fades in large and holds for a few seconds before
    settling into the scroll history — deliberately slower, more
    deliberate pacing than the rapid-fire SQLi/XSS pages, matching
    Strix's actual slower cadence.

  When complete: shows the final cost/turns/findings summary with
    the same corroboration-badge treatment described in the Phase
    12 report-merge work (🤖 AI-Validated indicator) carried
    through consistently into this live page too.

Generate StrixAgentOps.jsx only. Stop after.
```

---

## STEP 16 — Live Operations: Reporting Agent Page

```
STEP 16

Generate: src/pages/scans/agents/ReportAgentOps.jsx

Agent color: var(--agent-report) — sky blue

Shows the report-generation pipeline live (this is normally fast,
but should still visibly show its stages rather than just a
spinner):

  Stepper (horizontal, 5 steps, each lighting up in sequence as
  WebSocket progress updates arrive):
    Aggregating Findings → AI Analysis → Building Attack Paths →
    Prioritizing Risk → Rendering PDF

  During "AI Analysis" step specifically: show a live-typing
  effect of the executive summary text as Claude's response
  streams in conceptually (even if the actual API call isn't
  token-streamed, reveal the final text with a fast typewriter
  animation once received, so it FEELS like it's being written
  live) — this is a deliberate, honest UI choice: label it
  clearly enough that it's understood as a reveal animation of a
  completed response, not literally streaming tokens, by keeping
  the reveal fast (under 2 seconds total regardless of text length).

  On completion: large "REPORT READY" state with a prominent
  "Open Report" button routing to /scans/:id/report (the restyled
  Phase 13-original report viewer, now reskinned to this agent's
  sky-blue accent + new fonts, structurally unchanged from the
  original Reports Dashboard spec).

Generate ReportAgentOps.jsx only. Stop after.
```

---

## STEP 17 — Global Attack Graph

```
STEP 17

Generate: src/pages/scans/AttackGraph3D.jsx

Route: /scans/:id/graph

A full-screen, immersive 3D visualization using @react-three/fiber
+ @react-three/drei's OrbitControls:

  Center node: the target domain (large sphere, white, labeled)
  
  Seven orbiting nodes around it: one per agent, using the SAME
  AgentStatusOrb visual language (framer-motion layoutId morph
  from the PhaseRail/Command Center versions so navigating here
  feels like "zooming into" the same orbs seen elsewhere) —
  rendered as actual 3D spheres in Three.js, colored per-agent,
  pulsing when active.

  Each agent node has smaller satellite nodes orbiting IT,
  representing individual findings discovered by that agent —
  satellite color = severity, satellite size = CVSS score. New
  findings fly in from the target center outward to their agent's
  orbit with a spring-eased trajectory the instant a finding_found
  WebSocket event arrives.

  Attack chains (Phase 6/9's chain detection) render as glowing
  connecting lines directly between two finding-satellites that
  belong to a detected chain, even across different agent orbits
  — visually these are the most striking lines in the whole scene,
  rendered thicker and animated with the flow-dash traveling-dot
  effect.

  Click any satellite → opens the standard finding detail overlay
  (reused component, unchanged) as a panel sliding in from the
  right without leaving the 3D view.

  Bottom-left HUD overlay (2D, not 3D): live counts per agent,
  small, font-mono, non-intrusive.

  Respect prefers-reduced-motion: disables auto-rotation and all
  flight-in animations, finding satellites simply appear instantly
  in their final position instead.

Generate AttackGraph3D.jsx only. Stop after.
```

---

## STEP 18 — Findings / Reports / Monitoring Restyle

```
STEP 18

Generate: str_replace restyling passes over the existing
  VulnerabilityDashboard.jsx, ReportsDashboard.jsx,
  MonitoringDashboard.jsx (from prior phases)

Apply the new token system (agent colors, Space Grotesk/Chakra
Petch/JetBrains Mono fonts, grid-bg backgrounds, node-pulse status
indicators, glow treatments) to these three existing pages so the
whole app feels like one coherent product rather than two
different design eras bolted together. Preserve every existing
functional behavior exactly (filters, overlays, diff history,
pagination) — this step is visual token replacement only, not a
structural rebuild, since these pages' functionality was already
correct from their original phase.

Specifically:
  - VulnerabilityDashboard: severity colors swap to the new
    critical/high/medium/low/info values, finding-overlay border
    accents use agent-vuln pink instead of the old brand purple,
    tool badges colored per the TOOL_TO_CATEGORY → agent color
    mapping from Step 2 so a SQLMap-sourced finding shows a
    vuln-pink tag, a TruffleHog-sourced one shows a secrets-yellow
    tag, etc. — this cross-references the new color system
    meaningfully rather than just reskinning.
  - ReportsDashboard: report cards get a thin top border in the
    worst-offending agent's color (if one agent found the critical
    finding driving the report's risk score, that agent's hue
    leads the card's accent)
  - MonitoringDashboard: diff-history timeline entries colored by
    which agent's findings changed (new recon asset = cyan entry,
    new vuln finding = pink entry, etc.)

Generate the three restyle diffs. Stop after.
```

---

## STEP 19 — Final Verification

```
STEP 19 — FINAL VERIFICATION

─── FUNCTIONAL (every effect must be backed by a real call) ───

□ Attack Selector tree renders from GET /api/v1/scans/attack-catalog
  (not hardcoded in frontend)
□ Deselecting a category and launching a scan: verify via Flower/
  Celery logs that the excluded tool genuinely never dispatches
□ Live Terminal shows REAL stdout lines from an actual running
  tool (verify by watching a live Subfinder run — the lines
  shown must match what `docker compose logs worker_recon` shows
  for that same tool invocation)
□ CredStuffingDetail page's username/password pairs match actual
  entries in the cached SecLists file (spot-check 3 values)
□ /api/v1/intel/sources returns real GitHub repo URLs + correct
  license strings
□ HYBRID/AUTONOMOUS mode selection on /scans/new correctly blocks
  with the exact same SCOPE_NOT_CONFIRMED error as Phase 12 when
  org hasn't confirmed
□ Exploit/Strix agent pages show the lock-state correctly when
  their respective *_AGENT_ENABLED flags are False
□ Private IP entered in Attack Selector's target field is rejected
  client-side AND still rejected server-side if client validation
  is bypassed (test via direct API call)

─── VISUAL / MOTION ───

□ Every agent consistently uses its ONE signature color across
  nav rail, Command Center grid, PhaseRail, and Attack Graph node
  (spot check: agent-vuln pink appears in all four places for the
  Vulnerability agent, nowhere else)
□ AgentStatusOrb's layoutId morph animates smoothly when
  navigating between Command Center → scan's PhaseRail →
  AttackGraph3D (no jarring pop, genuine shared-element transition)
□ LiveCounter digit-roll animation fires on every WebSocket value
  change, not just once on mount
□ Route transitions between /vuln/* live attack pages trigger the
  one-shot glitch, other routes (findings, settings) do not
□ CriticalStrobe-equivalent flash moments (SQLi confirmed finding,
  critical finding card) never exceed 3 flashes/sec and are
  single-shot per unique finding ID
□ prefers-reduced-motion disables: matrix/particle backgrounds,
  scanline sweep, glitch transitions, flow-dash lines, 3D
  auto-rotation and fly-in animations — verify each individually
  via DevTools media feature emulation

─── PERFORMANCE ───

□ Three.js Command Center background + Attack Graph both capped
  to reasonable frame budgets (30fps acceptable for ambient scenes,
  pause rendering when document.visibilityState !== 'visible')
□ xterm.js scrollback capped at 5000 lines per terminal instance
  (prevents unbounded memory growth on long scans)
□ WebSocket message volume: verify AttemptEvent throttling (every
  Nth attempt, not every single one) actually keeps the socket
  from flooding on a fast tool like ffuf — check Network tab
  message rate during an active directory brute-force
□ Lighthouse Performance ≥ 75 (lower bar than the prior minimal
  design given the deliberately heavier visual load — but it must
  not fall below usable)

─── ACCESSIBILITY ───

□ Every status/severity indicator pairs color with a text label
  or icon, never color alone
□ Focus rings visible throughout despite the dark/neon palette
□ All icon-only controls carry aria-label
□ Live-region announcements (aria-live="polite") on the
  LiveCounter and key status-change moments so screen readers get
  meaningful updates from the real-time pages, not silence

Phase 13 (rebuild) complete when every functional checkbox passes
AND the visual/motion checklist is verified across at least: 
Command Center, one full vuln live-attack page (SQLi), the
Attack Selector, and the Attack Graph.
```

---

## Summary — What Changed vs. the Earlier Minimal Spec

| Aspect | Earlier (minimal) spec | This rebuild |
|---|---|---|
| Visual direction | One accent color, restrained | 9 agent signature colors, maximalist |
| Fonts | Oswald/Anton/Inter/Plex Mono | Space Grotesk/Chakra Petch/Plex Mono |
| Terminal | Styled `<div>` log | Real xterm.js instance, real streamed stdout |
| Attack control | Scan-type radio buttons only | Full checkbox-tree Attack Selector, hard-filtered server-side |
| Per-attack visibility | Findings table only | Dedicated live page per attack type with real payload streams |
| Open-source data | None | SecLists/PayloadsAllTheThings fetched, cached, attributed, and actually used |
| 3D | Login hero + AI graph only | Command Center field, AI Dashboard graph, Strix "thinking" cluster, full Attack Graph |
| Motion | Entry + rare critical moments | Continuous (scanlines, tickers, flow-lines) + one-shot signature moments preserved |