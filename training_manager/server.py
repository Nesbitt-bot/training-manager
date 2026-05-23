from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .metrics import load_metrics
from .paths import DEFAULT_HOST, DEFAULT_PORT
from .project import list_projects
from .runtime import git_pull, git_push, log_tail, save_checkpoint_commit, start_job, status, stop_job

STATIC = Path(__file__).resolve().parent / "static"


def _json(handler: BaseHTTPRequestHandler, payload: dict, status_code: int = 200):
    body = json.dumps(payload).encode()
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            body = (STATIC / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/app.js":
            body = (STATIC / "app.js").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/style.css":
            body = (STATIC / "style.css").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/css")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/projects":
            return _json(self, {"projects": list_projects()})
        if parsed.path.startswith("/api/project/") and parsed.path.endswith("/status"):
            name = parsed.path.split("/")[3]
            return _json(self, status(name))
        if parsed.path.startswith("/api/project/") and parsed.path.endswith("/logs"):
            name = parsed.path.split("/")[3]
            qs = parse_qs(parsed.query)
            lines = int(qs.get("lines", ["200"])[0])
            return _json(self, {"text": log_tail(name, lines=lines)})
        if parsed.path.startswith("/api/project/") and parsed.path.endswith("/metrics"):
            name = parsed.path.split("/")[3]
            return _json(self, load_metrics(name))
        return _json(self, {"error": "not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/project/"):
            parts = parsed.path.split("/")
            name = parts[3]
            action = parts[4]
            if action == "start":
                return _json(self, start_job(name))
            if action == "stop":
                return _json(self, stop_job(name))
            if action == "pull":
                return _json(self, git_pull(name))
            if action == "push":
                return _json(self, git_push(name))
            if action == "checkpoint":
                return _json(self, save_checkpoint_commit(name))
        return _json(self, {"error": "not found"}, 404)

    def log_message(self, format, *args):
        return


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"training-manager listening on http://{host}:{port}")
    httpd.serve_forever()
