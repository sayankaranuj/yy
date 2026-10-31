"""JavaScript secret extraction plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="secretfinder", category="secrets", binary_name="python", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Extract likely secrets from JavaScript responses."""
	metadata = metadata
# AgentSec AI — backend/plugins/secretfinder.py