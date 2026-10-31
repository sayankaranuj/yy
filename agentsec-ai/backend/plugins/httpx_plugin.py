"""HTTP probing and technology detection plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="httpx_plugin", category="enum", binary_name="httpx", default_timeout=300)
class Plugin(AbstractPlugin):
	"""Probe HTTP services for reachability and metadata."""
	metadata = metadata
# AgentSec AI — backend/plugins/httpx_plugin.py