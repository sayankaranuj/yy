"""Katana web crawling plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="katana", category="enum", binary_name="katana", default_timeout=300)
class Plugin(AbstractPlugin):
	"""Crawl a web target for endpoints."""
	metadata = metadata
# AgentSec AI — backend/plugins/katana.py