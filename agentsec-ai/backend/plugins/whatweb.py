"""WhatWeb technology fingerprinting plugin."""
from backend.plugins.base_plugin import AbstractPlugin, PluginMetadata
metadata = PluginMetadata(name="whatweb", category="enum", binary_name="whatweb", default_timeout=180)
class Plugin(AbstractPlugin):
	"""Fingerprint technologies exposed by a web target."""
	metadata = metadata
# AgentSec AI — backend/plugins/whatweb.py