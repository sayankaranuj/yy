"""SQL injection assessment plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="sqlmap_plugin", category="vuln", binary_name="sqlmap", default_timeout=600)
class Plugin(AbstractPlugin):
	"""Run SQLMap with the target supplied by the workflow."""
	metadata = metadata
# AgentSec AI — backend/plugins/sqlmap_plugin.py