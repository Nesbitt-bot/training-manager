from __future__ import annotations

from pathlib import Path
import time

from .project import project_config, runtime_state, save_runtime, tm_dir
from .util import run


def supervisor_conf_dir(name: str) -> Path:
    return tm_dir(name) / "supervisor"


def supervisor_conf_path(name: str) -> Path:
    return supervisor_conf_dir(name) / f"{name}.conf"


def supervisor_sock_path(name: str) -> Path:
    return supervisor_conf_dir(name) / "supervisor.sock"


def supervisor_pid_path(name: str) -> Path:
    return supervisor_conf_dir(name) / "supervisord.pid"


def ensure_program(name: str) -> Path:
    cfg = project_config(name)
    job = cfg["default_job"]
    conf = supervisor_conf_path(name)
    conf.parent.mkdir(parents=True, exist_ok=True)
    env = ",".join(f"{k}='{v}'" for k, v in job.get("env", {}).items())
    content = f"""
[unix_http_server]
file={supervisor_sock_path(name)}
chmod=0700

[supervisord]
logfile={supervisor_conf_dir(name) / 'supervisord.log'}
pidfile={supervisor_pid_path(name)}
childlogdir={supervisor_conf_dir(name)}

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix://{supervisor_sock_path(name)}

[program:{name}]
command={' '.join(job['command'])}
directory={job['cwd']}
autostart=false
autorestart=false
redirect_stderr=true
stdout_logfile={job['log_file']}
stopsignal=TERM
environment={env}
""".strip() + "\n"
    conf.write_text(content)
    return conf


def _ensure_daemon(conf: Path) -> None:
    run(["supervisord", "-c", str(conf)], check=False)


def supervisor_start(name: str) -> dict:
    conf = ensure_program(name)
    _ensure_daemon(conf)
    run(["supervisorctl", "-c", str(conf), "reread"], check=False)
    run(["supervisorctl", "-c", str(conf), "update"], check=False)
    cp = run(["supervisorctl", "-c", str(conf), "start", name], check=False)
    save_runtime(name, {"backend": "supervisor", "conf": str(conf), "started_at": time.time(), "stdout": cp.stdout, "stderr": cp.stderr})
    return {"ok": cp.returncode == 0, "stdout": cp.stdout, "stderr": cp.stderr, "conf": str(conf)}


def supervisor_stop(name: str) -> dict:
    conf = runtime_state(name).get("conf") or str(supervisor_conf_path(name))
    cp = run(["supervisorctl", "-c", conf, "stop", name], check=False)
    return {"ok": cp.returncode == 0, "stdout": cp.stdout, "stderr": cp.stderr}


def supervisor_status(name: str) -> dict:
    conf = runtime_state(name).get("conf") or str(supervisor_conf_path(name))
    cp = run(["supervisorctl", "-c", conf, "status", name], check=False)
    text = (cp.stdout or cp.stderr).strip()
    running = "RUNNING" in text
    return {"ok": cp.returncode == 0, "backend": "supervisor", "running": running, "raw": text, "conf": conf}
