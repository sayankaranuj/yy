"""Wayback URL discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="waybackurls", category="enum", binary_name="waybackurls", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Collect historical URLs for a target."""
	metadata = metadata
# AgentSec AI — backend/plugins/waybackurls.py