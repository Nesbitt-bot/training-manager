from __future__ import annotations

import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Any

from .project import project_config, repo_path, runtime_state, save_runtime
from .util import run, which


def _job(name: str) -> dict[str, Any]:
    return project_config(name)["default_job"]


def _env(job: dict[str, Any]) -> dict[str, str]:
    env = os.environ.copy()
    env.update({k: str(v) for k, v in job.get("env", {}).items()})
    return env


def git_pull(name: str) -> dict[str, Any]:
    p = repo_path(name)
    cp = run(["git", "pull", "--ff-only"], cwd=p, check=False)
    return {"ok": cp.returncode == 0, "stdout": cp.stdout, "stderr": cp.stderr}


def git_push(name: str) -> dict[str, Any]:
    p = repo_path(name)
    cp = run(["git", "push"], cwd=p, check=False)
    return {"ok": cp.returncode == 0, "stdout": cp.stdout, "stderr": cp.stderr}


def save_checkpoint_commit(name: str, message: str | None = None) -> dict[str, Any]:
    p = repo_path(name)
    msg = message or f"checkpoint: {name} {int(time.time())}"
    cp = run(["git", "add", "-A"], cwd=p, check=False)
    if cp.returncode != 0:
        return {"ok": False, "stdout": cp.stdout, "stderr": cp.stderr}
    cp2 = run(["git", "commit", "-m", msg], cwd=p, check=False)
    return {"ok": cp2.returncode == 0, "stdout": cp2.stdout, "stderr": cp2.stderr}


def start_job(name: str) -> dict[str, Any]:
    cfg = project_config(name)
    job = cfg["default_job"]
    if cfg.get("mode") == "supervisor" and which("supervisorctl") and which("supervisord"):
        from .supervisor_backend import ensure_program, supervisor_start
        ensure_program(name)
        return supervisor_start(name)
    log_path = Path(job["log_file"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    f = log_path.open("ab")
    proc = subprocess.Popen(
        job["command"],
        cwd=job["cwd"],
        env=_env(job),
        stdout=f,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    state = {
        "backend": "detached",
        "pid": proc.pid,
        "started_at": time.time(),
        "log_file": str(log_path),
        "command": job["command"],
        "cwd": job["cwd"],
    }
    save_runtime(name, state)
    return {"ok": True, **state}


def stop_job(name: str) -> dict[str, Any]:
    cfg = project_config(name)
    st = runtime_state(name)
    if cfg.get("mode") == "supervisor" and which("supervisorctl") and which("supervisord"):
        from .supervisor_backend import supervisor_stop
        return supervisor_stop(name)
    pid = st.get("pid")
    if not pid:
        return {"ok": False, "error": "no pid"}
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    save_runtime(name, {**st, "stopped_at": time.time()})
    return {"ok": True, "pid": pid}


def status(name: str) -> dict[str, Any]:
    cfg = project_config(name)
    st = runtime_state(name)
    if cfg.get("mode") == "supervisor" and which("supervisorctl") and which("supervisord"):
        from .supervisor_backend import supervisor_status
        return supervisor_status(name)
    pid = st.get("pid")
    running = False
    if pid:
        try:
            os.kill(pid, 0)
            running = True
        except OSError:
            running = False
    return {"ok": True, "backend": st.get("backend", "detached"), "running": running, **st}


def log_tail(name: str, lines: int = 200) -> str:
    st = runtime_state(name)
    path = Path(st.get("log_file") or _job(name)["log_file"])
    if not path.exists():
        return ""
    data = path.read_text(errors="ignore").splitlines()
    return "\n".join(data[-lines:])
