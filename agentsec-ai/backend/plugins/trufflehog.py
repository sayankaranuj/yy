"""TruffleHog secret discovery plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="trufflehog", category="secrets", binary_name="trufflehog", default_timeout=600)
class Plugin(AbstractPlugin):
	"""Scan repositories for verified secrets."""
	metadata = metadata
# AgentSec AI — backend/plugins/trufflehog.py