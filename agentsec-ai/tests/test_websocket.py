import json

from fastapi.testclient import TestClient

from backend.main import create_app
from backend.orchestrator.event_bus import event_bus


def test_websocket_streams_scan_event() -> None:
    client = TestClient(create_app())
    with client.websocket_connect("/api/ws/events") as websocket:
        message = websocket.receive_json()
        assert message["event"] == "connected"


def test_redis_event_bus_persists_dict_events_for_live_tool_terminal(monkeypatch) -> None:
    class FakeRedis:
        def __init__(self):
            self.values = []
            self.trim = None
            self.expiration = None

        def pipeline(self):
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def lpush(self, key, value):
            self.values.append((key, value))

        def ltrim(self, key, start, end):
            self.trim = (key, start, end)

        def expire(self, key, seconds):
            self.expiration = (key, seconds)

        def execute(self):
            return []

    fake_redis = FakeRedis()
    monkeypatch.setattr(event_bus, "_sync_redis", fake_redis)
    payload = {
        "event": "tool.command_started",
        "scan_id": "45",
        "task_id": "celery-task-45",
        "command": "httpx -u https://example.org",
    }

    event_bus.publish_to_websocket_sync("45", payload)

    key, serialized = fake_redis.values[0]
    assert key == "agentsec:ws:45"
    assert json.loads(serialized) == payload
    assert fake_redis.trim == (key, 0, 499)
    assert fake_redis.expiration == (key, 86400)
