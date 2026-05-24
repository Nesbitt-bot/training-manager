# training-manager

`training-manager` is a lightweight, host-native web UI for long-running Python and notebook jobs.

It is built for the case where training runs for days or weeks on the host machine, must survive terminal/editor closure, and must remain controllable through a browser.

## Why this exists

Most training workflows still assume a human babysits a terminal, a notebook tab, or a tmux session. That is fragile on personal workstations and research boxes.

`training-manager` gives maintainers a minimal control plane for local or remote training projects:

- initialize a managed training project from a git repo or local path
- start and stop long-running jobs
- inspect logs and runtime state in a browser
- capture metrics, stages, checkpoints, and ETA via a tiny Python SDK
- prefer `supervisord` when available, but still work in plain detached-process mode

## Current feature set

- run host-native jobs under `supervisord` when available
- fallback to direct detached process management when `supervisord` is absent
- one browser UI for:
  - start / stop
  - `git pull` / `git push`
  - logs
  - checkpoints
  - stage timeline
  - ETA and detailed progress
  - scalar metrics / loss charts
- support both `.py` and `.ipynb`
- default UI bind: `127.0.0.1:14514`

## Install

### Editable install for development

```bash
python3 -m pip install -e .
```

### Planned package install

Once published on PyPI:

```bash
pip install training-manager
```

## Quick start

### Manage a repo directly from GitHub

```bash
python3 -m pip install -e .
training-manager init --repo <REPO_URL> --name lavender-2
training-manager serve
```

### Manage an existing local checkout

```bash
python3 -m pip install -e .
training-manager init --path /path/to/lavender-2 --name lavender-2
training-manager serve
```

Then open:

```text
http://127.0.0.1:14514
```

## Lavender-2 example

Lavender-2 now exposes a repo-root `train.py` wrapper specifically so
`training-manager` can supervise the full notebook pipeline without
pretending the notebook itself is already a clean CLI.

```bash
training-manager init --path /absolute/path/to/Lavender-2 --name lavender-2
training-manager serve
```

In the UI:

1. select `lavender-2`
2. click **Start**
3. watch the log pane for `uv sync` and `NbConvertApp`
4. watch stages / checkpoints as the notebook progresses

## Demo media

These are currently lightweight placeholder mockups kept stable so they
can be replaced later with real captures without churn.

### Dashboard overview

![training-manager dashboard overview](docs/media/dashboard-overview.svg)

### Project detail view

![training-manager project detail](docs/media/project-detail.svg)

### Planned GIF

A future `docs/media/training-run.gif` should show:

- starting a managed project
- logs becoming active
- metrics chart gaining points
- checkpoint/state updates appearing in the event panel

## CLI reference

### `training-manager init`

Initialize a managed project.

```bash
training-manager init --name lavender-2 --repo https://github.com/example/lavender-2.git
```

or:

```bash
training-manager init --name lavender-2 --path /srv/lavender-2
```

Arguments:

- `--name` — logical project name used in the state registry
- `--repo` — git URL to clone into the managed projects area
- `--path` — existing local path to copy into the managed projects area

### `training-manager serve`

Start the local web UI.

```bash
training-manager serve --host 127.0.0.1 --port 14514
```

### `training-manager list`

List known projects.

```bash
training-manager list
```

## Managed project layout

Each managed project gets a `.training-manager/` directory with:

- `project.json` — project/job config
- `events.jsonl` — structured stage/checkpoint/progress events
- `metrics.jsonl` — scalar metrics for charting
- `runtime.json` — current runtime state
- `supervisor/` — generated supervisor config when enabled
- `logs/` — stdout/stderr logs

Global state lives under:

```text
~/.training-manager/
```

## How job detection currently works

By default, `training-manager` looks for one of these entrypoints in the managed repo:

1. `train.py`
2. `scripts/train.py`
3. `main.py`
4. otherwise the first notebook in the repo root
5. otherwise a placeholder `python3 -m http.server 0`

That fallback is intentionally simple. Future maintainers will probably want a richer per-project job-definition model.

## Notebook support

Notebook jobs are executed with:

```bash
jupyter nbconvert --to notebook --execute --inplace your_notebook.ipynb
```

If `jupyter` is not installed on the host, the UI will report that clearly.

## Instrumenting training code

For rich stage/ETA/checkpoint charts, emit structured events from training code:

```python
from training_manager.sdk import TrainingReporter

reporter = TrainingReporter()
reporter.stage("data")
reporter.metric(step=1, loss=2.31, lr=1e-4)
reporter.progress(step=10, total_steps=1000, eta_seconds=7200)
reporter.checkpoint("checkpoints/latest.ckpt", status="saved")
```

The UI still works without instrumentation, but charts and stage tracking are much better with it.

## Maintainer planning

Before publishing or opening issues, keep the local planning docs tidy:

- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/maintainer-backlog.md`](docs/maintainer-backlog.md)
- [`docs/github-labels.md`](docs/github-labels.md)
- [`.github/labels.json`](.github/labels.json)

Issue templates live under [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).

## Docs

Maintainer docs live in [`docs/`](docs/).

If GitHub Pages is enabled for the repository, the docs site can be published from the included workflow.

## Development

```bash
git clone <repo>
cd training-manager
python3 -m pip install -e .
training-manager serve
```

## Project status

This is still a small, practical scaffold rather than a polished platform. The point is to make long-running training easier to supervise, not to hide the mechanics.

## License

MIT
