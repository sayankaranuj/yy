"""DNS record enrichment plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="dnsx", category="recon", binary_name="dnsx", default_timeout=120)
class Plugin(AbstractPlugin):
	"""Resolve a target with dnsx."""
	metadata = metadata
# AgentSec AI — backend/plugins/dnsx.py