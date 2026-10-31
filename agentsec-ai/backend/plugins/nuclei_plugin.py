"""Nuclei template-based vulnerability scanner plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="nuclei_plugin", category="vuln", binary_name="nuclei", default_timeout=600)
class Plugin(AbstractPlugin):
	"""Run Nuclei templates against a target."""
	metadata = metadata
# AgentSec AI — backend/plugins/nuclei_plugin.py