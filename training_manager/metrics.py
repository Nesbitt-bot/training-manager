from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .project import repo_path


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def load_events(name: str) -> list[dict[str, Any]]:
    return _read_jsonl(repo_path(name) / ".training-manager" / "events.jsonl")


def load_metrics(name: str) -> dict[str, Any]:
    rows = _read_jsonl(repo_path(name) / ".training-manager" / "metrics.jsonl")
    series = defaultdict(list)
    last_step = None
    for row in rows:
        step = row.get("step")
        if step is not None:
            last_step = step
        for k, v in row.items():
            if k in {"ts", "step"}:
                continue
            if isinstance(v, (int, float)):
                series[k].append({"x": step if step is not None else len(series[k]), "y": v, "ts": row.get("ts")})
    events = load_events(name)
    progress = [e for e in events if e.get("type") == "progress"]
    stages = [e for e in events if e.get("type") == "stage"]
    checkpoints = [e for e in events if e.get("type") == "checkpoint"]
    eta = progress[-1].get("eta_seconds") if progress else None
    return {
        "series": dict(series),
        "stages": stages,
        "checkpoints": checkpoints,
        "progress": progress[-20:],
        "last_step": last_step,
        "eta_seconds": eta,
    }
