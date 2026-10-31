"""WordPress security assessment plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="wpscan_plugin", category="vuln", binary_name="wpscan", default_timeout=600)
class Plugin(AbstractPlugin):
	"""Run WPScan against WordPress targets."""
	metadata = metadata
# AgentSec AI — backend/plugins/wpscan_plugin.py