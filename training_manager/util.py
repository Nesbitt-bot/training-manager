from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import MANAGER_LOG_PATH, ensure_state_root


def log_manager(message: str, *, level: str = "INFO", **fields: Any) -> None:
    ensure_state_root()
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": message,
        **fields,
    }
    with MANAGER_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_json(path: Path, default: Any):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        log_manager(
            "failed to parse json",
            level="ERROR",
            path=str(path),
            error=str(exc),
        )
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    except Exception as exc:
        log_manager(
            "failed to write json",
            level="ERROR",
            path=str(path),
            error=str(exc),
        )
        raise


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as exc:
        log_manager(
            "failed to append jsonl",
            level="ERROR",
            path=str(path),
            error=str(exc),
        )
        raise


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    cp = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=False)
    if cp.returncode != 0:
        log_manager(
            "subprocess returned non-zero",
            level="ERROR",
            command=cmd,
            cwd=str(cwd) if cwd else None,
            returncode=cp.returncode,
            stdout=cp.stdout[-4000:],
            stderr=cp.stderr[-4000:],
        )
        if check:
            cp.check_returncode()
    return cp


def which(name: str) -> str | None:
    out = subprocess.run(["bash", "-lc", f"command -v {name} || true"], text=True, capture_output=True)
    value = out.stdout.strip()
    if not value:
        log_manager("command not found on PATH", level="WARNING", command=name)
    return value or None
