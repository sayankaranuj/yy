"""Dalfox XSS assessment plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="dalfox", category="vuln", binary_name="dalfox", default_timeout=300)
class Plugin(AbstractPlugin):
	"""Scan URLs for XSS indicators."""
	metadata = metadata
# AgentSec AI — backend/plugins/dalfox.py