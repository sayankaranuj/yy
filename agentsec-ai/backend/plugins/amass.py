"""Amass asset discovery plugin."""
from dataclasses import replace

from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata

metadata = PluginMetadata(name="amass", category="recon", binary_name="amass", default_timeout=120)


class Plugin(AbstractPlugin):
    """Execute Amass with a bounded passive-enumeration window."""

    metadata = metadata

    def execute(self, inp):
        # Amass can wait on multiple external data sources. Keep it bounded
        # independently of the larger scan-wide tool timeout.
        timeout = min(inp.timeout or self.metadata.default_timeout, 120)
        return super().execute(replace(inp, timeout=timeout))


# AgentSec AI — backend/plugins/amass.py