#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
NOTEBOOK = REPO_ROOT / "train.ipynb"
HEARTBEAT_SEC = 30.0
UV_FALLBACKS = [
    os.environ.get("UV_BIN"),
    "/home/node/.openclaw/workspace/tools/uv/uv",
]


def _find_uv() -> str | None:
    uv = shutil.which("uv")
    if uv:
        return uv
    for candidate in UV_FALLBACKS:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def _reporter():
    try:
        from training_manager.sdk import TrainingReporter
    except Exception:
        return None
    return TrainingReporter(os.environ.get("TRAINING_MANAGER_DIR"))


def _heartbeat(proc: subprocess.Popen, *, stage: str, reporter=None, every_sec: float = HEARTBEAT_SEC):
    started = time.time()
    while proc.poll() is None:
        time.sleep(every_sec)
        if proc.poll() is not None:
            break
        elapsed = int(time.time() - started)
        print(f"[{stage}] still running, {elapsed}s elapsed (pid={proc.pid})", flush=True)
        if reporter is not None:
            reporter.progress(step=elapsed, eta_seconds=None, stage=stage, pid=proc.pid)


def _run(cmd: list[str], *, stage: str, reporter=None) -> None:
    print(f"[{stage}] starting: {' '.join(cmd)}", flush=True)
    if reporter is not None:
        reporter.stage(stage, command=" ".join(cmd))
    proc = subprocess.Popen(cmd, cwd=REPO_ROOT)
    hb = threading.Thread(target=_heartbeat, kwargs={"proc": proc, "stage": stage, "reporter": reporter}, daemon=True)
    hb.start()
    rc = proc.wait()
    hb.join(timeout=1.0)
    print(f"[{stage}] finished with returncode={rc}", flush=True)
    if rc != 0:
        if reporter is not None:
            reporter.checkpoint(stage, status="failed", returncode=rc)
        raise SystemExit(rc)


def main() -> int:
    uv = _find_uv()
    if not uv:
        raise SystemExit("uv is required but was not found on PATH or known fallback locations")
    reporter = _reporter()
    if reporter is not None:
        reporter.stage("bootstrap", cwd=str(REPO_ROOT), notebook=str(NOTEBOOK))
    _run([uv, "sync"], stage="uv-sync", reporter=reporter)
    _run([uv, "run", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", NOTEBOOK.name], stage="notebook-execute:train", reporter=reporter)
    if reporter is not None:
        reporter.checkpoint(str(NOTEBOOK), status="completed")
        reporter.stage("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
