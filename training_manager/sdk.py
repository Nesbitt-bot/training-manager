from __future__ import annotations

import os
import time
from pathlib import Path

from .util import append_jsonl


class TrainingReporter:
    def __init__(self, root: str | None = None):
        base = Path(root or os.environ.get("TRAINING_MANAGER_DIR", ".training-manager"))
        self.base = base
        self.events = base / "events.jsonl"
        self.metrics = base / "metrics.jsonl"

    def stage(self, name: str, **extra):
        append_jsonl(self.events, {"ts": time.time(), "type": "stage", "name": name, **extra})

    def metric(self, step: int | None = None, **metrics):
        append_jsonl(self.metrics, {"ts": time.time(), "step": step, **metrics})

    def progress(self, step: int | None = None, total_steps: int | None = None, eta_seconds: float | None = None, **extra):
        append_jsonl(self.events, {"ts": time.time(), "type": "progress", "step": step, "total_steps": total_steps, "eta_seconds": eta_seconds, **extra})

    def checkpoint(self, path: str, status: str = "saved", **extra):
        append_jsonl(self.events, {"ts": time.time(), "type": "checkpoint", "path": path, "status": status, **extra})
