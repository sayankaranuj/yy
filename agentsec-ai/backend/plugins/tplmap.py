"""Server-side template injection assessment plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="tplmap", category="vuln", binary_name="tplmap", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Inspect parameterized URLs for template injection."""
	metadata = metadata
# AgentSec AI — backend/plugins/tplmap.py