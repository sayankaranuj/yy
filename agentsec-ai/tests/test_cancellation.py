import sys

from backend.plugins.base_plugin import AbstractPlugin, PluginInput, PluginMetadata
from backend.core.cancellation import (
    clear_scan_cancellation,
    is_scan_cancelled,
    request_scan_cancellation,
)


def test_scan_cancellation_signal_round_trip() -> None:
    scan_id = 987654
    clear_scan_cancellation(scan_id)
    assert not is_scan_cancelled(scan_id)
    request_scan_cancellation(scan_id, ttl=30)
    assert is_scan_cancelled(scan_id)
    clear_scan_cancellation(scan_id)
    assert not is_scan_cancelled(scan_id)


def test_plugin_terminates_subprocess_when_scan_is_cancelled(monkeypatch) -> None:
    plugin = AbstractPlugin()
    plugin.metadata = PluginMetadata(name="cancellation-test", default_timeout=30)
    plugin.build_command = lambda _input: [
        sys.executable,
        "-c",
        "import time; time.sleep(30)",
    ]
    monkeypatch.setattr("backend.plugins.base_plugin.is_scan_cancelled", lambda _scan_id: True)

    output = plugin.execute(PluginInput(scan_id="987655", target="fixture"))

    assert output.status == "cancelled"
    assert output.success is False
    assert output.error_message == "scan cancellation requested"
