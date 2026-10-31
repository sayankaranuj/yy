import pytest

from backend.config.settings import settings
from backend.plugins.base_plugin import PluginInput, PluginOutput
from backend.workers import recon_agent
from backend.workers.processors import recon_processor


@pytest.mark.asyncio
async def test_recon_plugins_receive_typed_input_with_tool_timeout(monkeypatch) -> None:
    received = []

    def run_plugin(name, plugin_input):
        received.append(plugin_input)
        return PluginOutput(scan_id=plugin_input.scan_id, tool_name=name, success=True)

    class FakeProcessor:
        async def store_subdomains(self, scan_id, subdomains):
            return len(subdomains)

    monkeypatch.setattr(recon_agent.registry, "auto_discover", lambda: None)
    monkeypatch.setattr(recon_agent.executor, "run", run_plugin)
    monkeypatch.setattr(recon_processor, "ReconResultProcessor", FakeProcessor)

    result = await recon_agent._async_start(
        "17",
        "example.com",
        tool_decisions=["amass"],
        task_id="celery-task-17",
    )

    assert len(received) == 1
    assert isinstance(received[0], PluginInput)
    assert received[0].timeout == settings.scan.tool_timeout_seconds
    assert received[0].task_id == "celery-task-17"
    assert result["tool_errors"] == []
