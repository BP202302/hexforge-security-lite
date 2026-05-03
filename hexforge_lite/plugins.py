from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import List, Type

from .config import BASE_DIR, ENABLE_PLUGINS
from .modules.base import BaseModule

PLUGIN_ROOT = BASE_DIR / "plugins" / "examples"


class SafePluginModule(BaseModule):
    """Wrapper that prevents community plugins from breaking the scan pipeline."""

    def __init__(self, inner: BaseModule) -> None:
        self.inner = inner
        self.name = f"plugin:{inner.name}"

    def run(self, context):
        try:
            results = self.inner.run(context)
            return results if isinstance(results, list) else []
        except Exception:
            return []


def _load_module(path: Path) -> ModuleType | None:
    spec = importlib.util.spec_from_file_location(f"hexforge_lite_plugin_{path.stem}", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    return module


def _plugin_classes(module: ModuleType) -> list[Type[BaseModule]]:
    classes: list[Type[BaseModule]] = []
    for value in module.__dict__.values():
        if isinstance(value, type) and issubclass(value, BaseModule) and value is not BaseModule:
            if getattr(value, "lite_safe", False) is True:
                classes.append(value)
    return classes


def load_lite_plugins(plugin_root: Path | None = None) -> List[BaseModule]:
    """Load opt-in Lite plugins from the local plugin directory.

    Only classes that inherit BaseModule and explicitly set lite_safe = True are loaded.
    This keeps the plugin system useful while making accidental execution less likely.
    """
    if not ENABLE_PLUGINS:
        return []
    root = plugin_root or PLUGIN_ROOT
    if not root.exists() or not root.is_dir():
        return []
    loaded: list[BaseModule] = []
    for path in sorted(root.glob("*.py")):
        if path.name.startswith("_"):
            continue
        module = _load_module(path)
        if module is None:
            continue
        for cls in _plugin_classes(module):
            try:
                loaded.append(SafePluginModule(cls()))
            except Exception:
                continue
    return loaded[:8]
