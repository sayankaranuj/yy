"""CORS policy assessment plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="corsy", category="vuln", binary_name="python", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Inspect cross-origin response policies."""
	metadata = metadata
# AgentSec AI — backend/plugins/corsy.py