# Getting started

## Install

```bash
python3 -m pip install -e .
```

## Initialize a managed project

From a repo URL:

```bash
training-manager init --name lavender-2 --repo https://github.com/example/lavender-2.git
```

From a local checkout:

```bash
training-manager init --name lavender-2 --path /path/to/lavender-2
```

## Run the UI

```bash
training-manager serve
```

Open `http://127.0.0.1:14514`.

## Emit training telemetry

```python
from training_manager.sdk import TrainingReporter

reporter = TrainingReporter()
reporter.stage("train")
reporter.metric(step=100, loss=1.23)
reporter.progress(step=100, total_steps=1000, eta_seconds=3600)
reporter.checkpoint("checkpoints/epoch-1.pt")
```
