"""JavaScript endpoint discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="linkfinder", category="secrets", binary_name="python", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Extract endpoint links from JavaScript assets."""
	metadata = metadata
# AgentSec AI — backend/plugins/linkfinder.py