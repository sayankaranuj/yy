import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

os.environ.setdefault("AGENTSEC_SCAN_STORE", str(ROOT / "tests" / "test_scan_store.json"))
os.environ.setdefault("AGENTSEC_FINDINGS_STORE", str(ROOT / "tests" / "test_findings_store.json"))
# Keep the unit suite isolated from the Docker production backend configured in
# the repository .env file.
os.environ["STORAGE_BACKEND"] = "json"
os.environ["AUTH_ENABLED"] = "false"
os.environ["ALLOWED_HOSTS"] = "testserver,localhost,127.0.0.1"
