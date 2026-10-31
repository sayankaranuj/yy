"""Nmap service detection plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="nmap_plugin", category="enum", binary_name="nmap", default_timeout=300)
class Plugin(AbstractPlugin):
	"""Run default Nmap service detection."""
	metadata = metadata
# AgentSec AI — backend/plugins/nmap_plugin.py