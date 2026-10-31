"""Fast TCP port scanning plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="naabu", category="enum", binary_name="naabu", fallback_plugin="rustscan", default_timeout=300)
class Plugin(AbstractPlugin):
	"""Scan target hosts for open TCP ports."""
	metadata = metadata
# AgentSec AI — backend/plugins/naabu.py