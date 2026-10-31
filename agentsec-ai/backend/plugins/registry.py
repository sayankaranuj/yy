"""Plugin registry for AgentSec AI.

Provides a simple singleton registry that can auto-discover plugin
modules in the `backend.plugins` package and expose metadata to the
rest of the application.
"""

from __future__ import annotations

import importlib
import os
from dataclasses import asdict
from typing import Callable, Dict, List, Optional

from backend.plugins.base_plugin import PluginMetadata, AbstractPlugin


class PluginNotFoundError(Exception):
    pass


class PluginRegistry:
    def __init__(self) -> None:
        self._store: Dict[str, PluginMetadata] = {}
        self._plugins: Dict[str, Callable[..., AbstractPlugin]] = {}

    def register(self, metadata: PluginMetadata):
        """Decorator for registering a plugin class with metadata.

        Usage:
            @registry.register(PluginMetadata(...))
            class MyPlugin(AbstractPlugin):
                ...
        """

        def _decorator(cls):
            name = metadata.name
            self._store[name] = metadata
            self._plugins[name] = cls
            return cls

        return _decorator

    def add_manual(self, metadata: PluginMetadata, cls: Optional[Callable] = None):
        self._store[metadata.name] = metadata
        if cls is not None:
            self._plugins[metadata.name] = cls

    def list_all(self) -> List[Dict]:
        return [asdict(m) for m in self._store.values()]

    def is_registered(self, name: str) -> bool:
        return name in self._store

    def get_metadata(self, name: str) -> PluginMetadata:
        if name not in self._store:
            raise PluginNotFoundError(name)
        return self._store[name]

    def get(self, name: str):
        if name not in self._store:
            return None
        return self._plugins.get(name) or self._store.get(name)

    def get_plugin_class(self, name: str):
        return self._plugins.get(name)

    def auto_discover(self, package: str = "backend.plugins") -> int:
        """Scan the plugins package directory and register simple metadata
        for every .py file found. If the module defines `metadata` or a
        `register` call, prefer that; otherwise synthesize a minimal
        PluginMetadata so APIs can expose a consistent list.
        Returns the number of discovered plugins.
        """

        root = os.path.join(os.getcwd(), package.replace(".", os.sep))
        if not os.path.isdir(root):
            return 0

        count = 0
        for fn in os.listdir(root):
            if not fn.endswith(".py") or fn == "__init__.py":
                continue
            mod_name = fn[:-3]
            full_mod = f"{package}.{mod_name}"
            try:
                mod = importlib.import_module(full_mod)
            except Exception:
                # If import fails, still synthesize metadata from filename
                meta = PluginMetadata(name=mod_name, description="Autodiscovered")
                if mod_name not in self._store:
                    self.add_manual(meta)
                count += 1
                continue

            # if module defines `metadata` dataclass, use that
            if hasattr(mod, "metadata") and isinstance(getattr(mod, "metadata"), PluginMetadata):
                meta = getattr(mod, "metadata")
                plugin_cls = getattr(mod, "Plugin", None)
                self.add_manual(meta, plugin_cls)
                count += 1
                continue

            # Utility modules are not executable tools and must not appear in
            # the tool inventory or be sent to workers.
            plugin_cls = getattr(mod, "Plugin", None)
            if plugin_cls is None:
                continue
            meta = PluginMetadata(name=mod_name, description=getattr(mod, "__doc__", ""))
            if mod_name not in self._store:
                self.add_manual(meta, plugin_cls)
            count += 1

        return count


# single global registry instance
registry = PluginRegistry()
