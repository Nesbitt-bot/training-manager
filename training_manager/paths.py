from __future__ import annotations

from pathlib import Path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 14514
HOME = Path.home()
STATE_ROOT = HOME / ".training-manager"
PROJECTS_DIR = STATE_ROOT / "projects"
REGISTRY_PATH = STATE_ROOT / "registry.json"
MANAGER_LOG_PATH = STATE_ROOT / "manager.log"


def ensure_state_root() -> None:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    MANAGER_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
