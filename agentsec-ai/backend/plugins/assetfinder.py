"""Assetfinder subdomain discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="assetfinder", category="recon", binary_name="assetfinder", default_timeout=120)
class Plugin(AbstractPlugin):
	"""Execute Assetfinder against a target domain."""
	metadata = metadata
# AgentSec AI — backend/plugins/assetfinder.py