from __future__ import annotations

import os
import shlex
import shutil
import time
from pathlib import Path
from typing import Any

from .paths import PROJECTS_DIR, REGISTRY_PATH, ensure_state_root
from .util import log_manager, read_json, run, write_json, which


MANAGER_REPO_ROOT = Path(__file__).resolve().parents[1]


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


def _manager_pythonpath() -> str:
    current = os.environ.get("PYTHONPATH")
    parts = [str(MANAGER_REPO_ROOT)]
    if current:
        parts.append(current)
    return os.pathsep.join(parts)


def detect_command(repo_path: Path) -> list[str]:
    for candidate in ["train.py", "scripts/train.py", "main.py"]:
        if (repo_path / candidate).exists():
            cmd = ["python3", candidate]
            log_manager("detected project command", repo=str(repo_path), command=cmd)
            return cmd
    notebooks = sorted(repo_path.glob("*.ipynb"))
    if notebooks:
        cmd = ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", notebooks[0].name]
        log_manager("detected notebook command", repo=str(repo_path), command=cmd)
        return cmd
    cmd = ["python3", "-m", "http.server", "0"]
    log_manager("using placeholder project command", level="WARNING", repo=str(repo_path), command=cmd)
    return cmd


def _normalize_command(command: str | list[str] | None) -> list[str] | None:
    if command is None:
        return None
    if isinstance(command, str):
        return shlex.split(command)
    return [str(x) for x in command]


def init_project(
    name: str,
    repo: str | None = None,
    path: str | None = None,
    command: str | list[str] | None = None,
) -> dict[str, Any]:
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
    chosen_command = _normalize_command(command) or detect_command(root)
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
            "command": chosen_command,
            "env": {
                "TRAINING_MANAGER_DIR": str(root / ".training-manager"),
                "PYTHONPATH": _manager_pythonpath(),
            },
            "log_file": str(root / ".training-manager" / "logs" / "train.log"),
            "checkpoint_globs": ["checkpoints/**", "*.ckpt", "*.pt", "*.pth", "*.safetensors"],
        },
    }
    (root / ".training-manager" / "logs").mkdir(parents=True, exist_ok=True)
    write_json(project_file(name), cfg)
    reg = registry()
    reg["projects"][name] = {"path": str(root), "repo_url": repo}
    save_registry(reg)
    log_manager(
        "initialized project",
        name=name,
        repo=str(repo) if repo else None,
        path=str(path) if path else None,
        managed_path=str(root),
        command=chosen_command,
        mode=cfg["mode"],
    )
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
    log_manager("updated project config", name=name, command=cfg.get("default_job", {}).get("command"))
