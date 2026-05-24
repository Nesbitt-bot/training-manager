from __future__ import annotations

import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Any

from .project import project_config, repo_path, runtime_state, save_runtime
from .util import log_manager, run, which


def _job(name: str) -> dict[str, Any]:
    return project_config(name)["default_job"]


def _env(job: dict[str, Any]) -> dict[str, str]:
    env = os.environ.copy()
    env.update({k: str(v) for k, v in job.get("env", {}).items()})
    return env


def _proc_state(pid: int | None) -> str | None:
    if not pid:
        return None
    cp = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], text=True, capture_output=True)
    value = cp.stdout.strip()
    return value or None


def _is_running(pid: int | None) -> bool:
    state = _proc_state(pid)
    if not state:
        return False
    return not state.startswith("Z")


def git_pull(name: str) -> dict[str, Any]:
    p = repo_path(name)
    cp = run(["git", "pull", "--ff-only"], cwd=p, check=False)
    if cp.returncode != 0:
        log_manager("git pull failed", level="ERROR", name=name, cwd=str(p), stdout=cp.stdout[-4000:], stderr=cp.stderr[-4000:])
    return {"ok": cp.returncode == 0, "stdout": cp.stdout, "stderr": cp.stderr}


def git_push(name: str) -> dict[str, Any]:
    p = repo_path(name)
    cp = run(["git", "push"], cwd=p, check=False)
    if cp.returncode != 0:
        log_manager("git push failed", level="ERROR", name=name, cwd=str(p), stdout=cp.stdout[-4000:], stderr=cp.stderr[-4000:])
    return {"ok": cp.returncode == 0, "stdout": cp.stdout, "stderr": cp.stderr}


def save_checkpoint_commit(name: str, message: str | None = None) -> dict[str, Any]:
    p = repo_path(name)
    msg = message or f"checkpoint: {name} {int(time.time())}"
    cp = run(["git", "add", "-A"], cwd=p, check=False)
    if cp.returncode != 0:
        return {"ok": False, "stdout": cp.stdout, "stderr": cp.stderr}
    cp2 = run(["git", "commit", "-m", msg], cwd=p, check=False)
    if cp2.returncode != 0:
        log_manager("checkpoint commit failed", level="ERROR", name=name, cwd=str(p), message_text=msg, stdout=cp2.stdout[-4000:], stderr=cp2.stderr[-4000:])
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
    log_manager("started job", name=name, pid=proc.pid, cwd=job["cwd"], command=job["command"], log_file=str(log_path))
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
    result: dict[str, Any] = {"pid": pid}
    try:
        os.killpg(pid, signal.SIGTERM)
        result["sent"] = "SIGTERM"
    except ProcessLookupError:
        result["sent"] = "missing"
    time.sleep(2)
    if _is_running(pid):
        try:
            os.killpg(pid, signal.SIGKILL)
            result["escalated"] = "SIGKILL"
        except ProcessLookupError:
            pass
        time.sleep(1)
    still_running = _is_running(pid)
    proc_state = _proc_state(pid)
    save_runtime(name, {**st, "stopped_at": time.time(), "running": still_running, "proc_state": proc_state})
    log_manager("stopped job", level="WARNING" if still_running else "INFO", name=name, pid=pid, proc_state=proc_state, still_running=still_running, result=result)
    return {"ok": not still_running, **result, "running": still_running, "proc_state": proc_state}


def status(name: str) -> dict[str, Any]:
    cfg = project_config(name)
    st = runtime_state(name)
    if cfg.get("mode") == "supervisor" and which("supervisorctl") and which("supervisord"):
        from .supervisor_backend import supervisor_status
        return supervisor_status(name)
    pid = st.get("pid")
    running = _is_running(pid)
    proc_state = _proc_state(pid)
    return {"ok": True, "backend": st.get("backend", "detached"), "running": running, "proc_state": proc_state, **st}


def log_tail(name: str, lines: int = 200) -> str:
    st = runtime_state(name)
    path = Path(st.get("log_file") or _job(name)["log_file"])
    if not path.exists():
        log_manager("requested log tail for missing file", level="WARNING", name=name, path=str(path))
        return ""
    data = path.read_text(errors="ignore").splitlines()
    return "\n".join(data[-lines:])
