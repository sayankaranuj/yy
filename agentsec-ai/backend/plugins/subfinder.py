"""Subfinder passive subdomain discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="subfinder", category="recon", binary_name="subfinder", fallback_plugin="amass", default_timeout=120)
class Plugin(AbstractPlugin):
	"""Execute subfinder against a target domain."""
	metadata = metadata
# AgentSec AI — backend/plugins/subfinder.py