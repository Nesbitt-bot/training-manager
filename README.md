# training-manager

`training-manager` is a lightweight, host-native web UI for long-running Python and notebook jobs.

It is built for the case where training runs for days or weeks on the host machine, must survive terminal/editor closure, and must remain controllable through a browser.

## Goals

- run host-native jobs under `supervisord` when available
- fallback to direct detached process management when `supervisord` is absent
- one browser UI for:
  - start / stop / restart
  - `git pull` / `git push`
  - logs
  - checkpoints
  - stage timeline
  - ETA and detailed progress
  - scalar metrics / loss charts
- support both `.py` and `.ipynb`
- default UI bind: `127.0.0.1:14514`

## One-line bootstrap on the training host

```bash
python3 -m pip install -e . && training-manager init --repo <REPO_URL> --name lavender-2 && training-manager serve
```

If you already have the repo locally:

```bash
python3 -m pip install -e . && training-manager init --path /path/to/lavender-2 --name lavender-2 && training-manager serve
```

## How it works

Each managed project gets a `.training-manager/` directory with:

- `project.json` — project/job config
- `events.jsonl` — structured stage/checkpoint/progress events
- `metrics.jsonl` — scalar metrics for charting
- `runtime.json` — current runtime state
- `supervisor/` — generated supervisor config when enabled
- `logs/` — stdout/stderr logs

## Notebook support

Notebook jobs are executed with:

```bash
jupyter nbconvert --to notebook --execute --inplace your_notebook.ipynb
```

If `jupyter` is not installed on the host, the UI will report that clearly.

## Training script instrumentation

For rich stage/ETA/checkpoint charts, emit structured events from your training code:

```python
from training_manager.sdk import TrainingReporter

reporter = TrainingReporter()
reporter.stage("data")
reporter.metric(step=1, loss=2.31, lr=1e-4)
reporter.progress(step=10, total_steps=1000, eta_seconds=7200)
reporter.checkpoint("checkpoints/latest.ckpt", status="saved")
```

The UI still works without instrumentation, but charts and stage tracking will be much better with it.

## Publishing status

This repo is scaffolded locally first. Pushing to GitHub depends on host auth and the target remote.
