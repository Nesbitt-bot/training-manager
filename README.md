# training-manager

`training-manager` is a lightweight, host-native web UI for long-running Python and notebook jobs.

It is designed for the case where a job runs for hours, days, or weeks on a host machine, must survive terminal/editor closure, and should remain controllable through a browser.

## Features

- manage long-running local jobs through a small web UI
- start / stop jobs
- inspect logs and runtime state
- capture stages, progress, checkpoints, and scalar metrics via a tiny SDK
- run under `supervisord` when available, or plain detached-process mode otherwise
- support both Python scripts and notebook-based workflows
- override the detected command when a project needs a wrapper

## Installation

For local development:

```bash
python3 -m pip install -e .
```

Then start the UI:

```bash
training-manager serve
```

Open:

```text
http://127.0.0.1:14514
```

## Quick start

Initialize a project from a local checkout:

```bash
training-manager init --name my-project --path /path/to/project
```

Initialize a project from a repository URL:

```bash
training-manager init --name my-project --repo https://github.com/example/repo.git
```

If the project needs a specific wrapper command, override detection explicitly:

```bash
training-manager init --name my-project --path /path/to/project \
  --command "python3 train.py --notebook train.ipynb"
```

## Toy notebook example

A small notebook-based Torch training example ships in this repository:

```text
examples/toy-notebook-project/
```

Use it to validate notebook supervision on a smaller host:

```bash
training-manager init \
  --name toy-notebook \
  --path /absolute/path/to/training-manager/examples/toy-notebook-project
training-manager serve
```

## Structured telemetry

Projects can emit events and metrics through the SDK:

```python
from training_manager.sdk import TrainingReporter

reporter = TrainingReporter()
reporter.stage("data")
reporter.metric(step=1, loss=2.31, lr=1e-4)
reporter.progress(step=10, total_steps=1000, eta_seconds=7200)
reporter.checkpoint("checkpoints/latest.ckpt", status="saved")
```

## Logs and diagnostics

Managed-job log:

```text
~/.training-manager/projects/<name>/.training-manager/logs/train.log
```

Manager-internal diagnostics:

```text
~/.training-manager/manager.log
```

## Documentation

The documentation is built with Sphinx from `docs/`.

Build it locally with:

```bash
python3 -m pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

## License

MIT
