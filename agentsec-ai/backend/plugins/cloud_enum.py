"""Cloud asset enumeration plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="cloud_enum", category="cloud", binary_name="python", default_timeout=600)
class Plugin(AbstractPlugin):
	"""Enumerate cloud naming patterns safely."""
	metadata = metadata
# AgentSec AI — backend/plugins/cloud_enum.py