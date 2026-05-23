from __future__ import annotations

import os
import shutil
import time
from pathlib import Path
from typing import Any

from .paths import PROJECTS_DIR, REGISTRY_PATH, ensure_state_root
from .util import read_json, run, write_json, which


def registry() -> dict[str, Any]:
    ensure_state_root()
    return read_json(REGISTRY_PATH, {"projects": {}})


def save_registry(data: dict[str, Any]) -> None:
    write_json(REGISTRY_PATH, data)


def project_dir(name: str) -> Path:
    return PROJECTS_DIR / name


def tm_dir(name: str) -> Path:
    return project_dir(name) / ".training-manager"


def project_file(name: str) -> Path:
    return tm_dir(name) / "project.json"


def runtime_file(name: str) -> Path:
    return tm_dir(name) / "runtime.json"


def project_config(name: str) -> dict[str, Any]:
    return read_json(project_file(name), {})


def runtime_state(name: str) -> dict[str, Any]:
    return read_json(runtime_file(name), {})


def save_runtime(name: str, data: dict[str, Any]) -> None:
    write_json(runtime_file(name), data)


def detect_command(repo_path: Path) -> list[str]:
    for candidate in ["train.py", "scripts/train.py", "main.py"]:
        if (repo_path / candidate).exists():
            return ["python3", candidate]
    notebooks = sorted(repo_path.glob("*.ipynb"))
    if notebooks:
        return ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", notebooks[0].name]
    return ["python3", "-m", "http.server", "0"]


def init_project(name: str, repo: str | None = None, path: str | None = None) -> dict[str, Any]:
    ensure_state_root()
    root = project_dir(name)
    if root.exists() and any(root.iterdir()):
        raise RuntimeError(f"project already exists: {root}")
    root.parent.mkdir(parents=True, exist_ok=True)
    if repo:
        run(["git", "clone", repo, str(root)])
    elif path:
        shutil.copytree(path, root, dirs_exist_ok=True)
    else:
        root.mkdir(parents=True, exist_ok=True)
    cfg = {
        "name": name,
        "repo_path": str(root),
        "repo_url": repo,
        "created_at": time.time(),
        "host": "127.0.0.1",
        "port": 14514,
        "mode": "supervisor" if which("supervisord") and which("supervisorctl") else "detached",
        "default_job": {
            "name": "train",
            "cwd": str(root),
            "command": detect_command(root),
            "env": {"TRAINING_MANAGER_DIR": str(root / ".training-manager")},
            "log_file": str(root / ".training-manager" / "logs" / "train.log"),
            "checkpoint_globs": ["checkpoints/**", "*.ckpt", "*.pt", "*.pth", "*.safetensors"],
        },
    }
    (root / ".training-manager" / "logs").mkdir(parents=True, exist_ok=True)
    write_json(project_file(name), cfg)
    reg = registry()
    reg["projects"][name] = {"path": str(root), "repo_url": repo}
    save_registry(reg)
    return cfg


def list_projects() -> list[dict[str, Any]]:
    reg = registry()
    out = []
    for name in sorted(reg.get("projects", {})):
        cfg = project_config(name)
        rt = runtime_state(name)
        out.append({
            "name": name,
            "path": cfg.get("repo_path"),
            "mode": cfg.get("mode"),
            "job": cfg.get("default_job", {}),
            "runtime": rt,
        })
    return out


def repo_path(name: str) -> Path:
    cfg = project_config(name)
    return Path(cfg["repo_path"])


def update_project_config(name: str, cfg: dict[str, Any]) -> None:
    write_json(project_file(name), cfg)
