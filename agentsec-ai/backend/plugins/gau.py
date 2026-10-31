"""GAU historical URL discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="gau", category="enum", binary_name="gau", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Collect URLs from public providers."""
	metadata = metadata
# AgentSec AI — backend/plugins/gau.py