"""RustScan fallback port scanning plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="rustscan", category="enum", binary_name="rustscan", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Scan target hosts when Naabu is unavailable."""
	metadata = metadata
# AgentSec AI — backend/plugins/rustscan.py