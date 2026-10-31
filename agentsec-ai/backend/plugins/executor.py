"""Plugin executor used by agents to run plugins.

This executor keeps execution simple for unit tests: if a plugin class
is registered and defines an `execute` method it will be invoked and its
PluginOutput returned. If the plugin is not present, a synthetic empty
PluginOutput is returned.
"""

from __future__ import annotations

import logging
import hashlib
import json
from typing import Any, Dict, Optional

from backend.plugins.base_plugin import PluginInput, PluginOutput
from backend.plugins.registry import registry

logger = logging.getLogger(__name__)


class PluginExecutor:
    def __init__(self) -> None:
        self.registry = registry

    def run(self, plugin_name: str, inp: PluginInput, extra_params: Optional[Dict[str, Any]] = None) -> PluginOutput:
        """Execute an installed plugin and surface missing implementations as failures."""

        aliases = {
            "httpx": "httpx_plugin",
            "nmap": "nmap_plugin",
            "nuclei": "nuclei_plugin",
            "sqlmap": "sqlmap_plugin",
            "ffuf": "ffuf_plugin",
            "wpscan": "wpscan_plugin",
        }
        registered_name = aliases.get(plugin_name, plugin_name)
        if not self.registry.is_registered(registered_name):
            self.registry.auto_discover()
        plugin_cls = self.registry.get_plugin_class(registered_name)

        if plugin_cls is None:
            message = f"Plugin implementation is not registered: {registered_name}"
            logger.error(message)
            return PluginOutput(
                scan_id=inp.scan_id,
                tool_name=registered_name,
                success=False,
                error_message=message,
            )

        # instantiate and call execute (support sync execute)
        plugin = plugin_cls()
        from backend.core.eventbus import EventBus

        started = {"scan_id": inp.scan_id, "tool_name": plugin_name, "target": inp.target}
        EventBus().publish("tool.started", started)
        self._publish_live(inp.scan_id, {"event": "tool.started", **started})
        out = plugin.execute(inp)
        if not isinstance(out, PluginOutput):
            # Try to coerce common dict-like responses
            if isinstance(out, dict):
                parsed = out.get("parsed", [])
                result = PluginOutput(
                    scan_id=inp.scan_id,
                    tool_name=registered_name,
                    raw=str(out),
                    parsed=parsed,
                    record_count=len(parsed),
                )
                completed = {"scan_id": inp.scan_id, "tool_name": plugin_name, "records": result.record_count}
                EventBus().publish("tool.completed", completed)
                self._publish_live(inp.scan_id, {"event": "tool.completed", **completed})
                return result
            raise RuntimeError("Plugin did not return PluginOutput")

        completed = {"scan_id": inp.scan_id, "tool_name": registered_name, "records": out.record_count, "success": out.success}
        EventBus().publish("tool.completed", completed)
        self._publish_live(inp.scan_id, {"event": "tool.completed", **completed})
        return out

    @staticmethod
    def _publish_live(scan_id: str, event: dict[str, Any]) -> None:
        """Persist a tool lifecycle event for scan WebSocket clients."""

        try:
            from backend.orchestrator.event_bus import event_bus

            event.setdefault(
                "event_id",
                hashlib.sha256(
                    json.dumps(event, sort_keys=True, default=str).encode()
                ).hexdigest()[:24],
            )
            event_bus.publish_to_websocket_sync(str(scan_id), event)
        except Exception:
            logger.debug("Unable to publish plugin event for scan %s", scan_id, exc_info=True)


executor = PluginExecutor()
