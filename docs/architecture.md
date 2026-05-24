# Architecture

## State model

Global state root:

```text
~/.training-manager/
```

Important files:

- `registry.json` — known projects
- `projects/<name>/.training-manager/project.json` — project config
- `projects/<name>/.training-manager/runtime.json` — current runtime state
- `projects/<name>/.training-manager/events.jsonl` — stage/progress/checkpoint events
- `projects/<name>/.training-manager/metrics.jsonl` — scalar metrics
- `projects/<name>/.training-manager/logs/train.log` — aggregated job log

## Runtime model

Two execution modes exist:

1. `supervisor` mode when `supervisord` and `supervisorctl` are available
2. `detached` mode using `subprocess.Popen(..., start_new_session=True)` otherwise

## Web server

The UI is served by Python's built-in `ThreadingHTTPServer`.

That keeps the project dependency-light, though it also means the current API surface is intentionally small and synchronous.

## Job detection

Default command detection is heuristic-based and currently checks for:

- `train.py`
- `scripts/train.py`
- `main.py`
- first notebook in repo root
- placeholder fallback

Future maintainers may want explicit per-project commands instead of inference.
