"""Findomain subdomain discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="findomain", category="recon", binary_name="findomain", default_timeout=120)
class Plugin(AbstractPlugin):
	"""Execute Findomain against a target domain."""
	metadata = metadata
# AgentSec AI — backend/plugins/findomain.py