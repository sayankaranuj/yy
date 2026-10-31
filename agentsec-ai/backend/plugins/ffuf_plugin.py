"""FFUF content discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="ffuf_plugin", category="enum", binary_name="ffuf", default_timeout=300)
class Plugin(AbstractPlugin):
	"""Discover paths and parameters with FFUF."""
	metadata = metadata
# AgentSec AI — backend/plugins/ffuf_plugin.py