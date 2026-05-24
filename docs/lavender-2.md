# Lavender-2 integration

This page documents the two useful `training-manager` modes for Lavender-2.

## 1. Local validation on a small host

Use the toy notebook instead of the full LLM notebook.

```bash
training-manager init --path /absolute/path/to/Lavender-2 --name lavender-toy \
  --command "python3 train.py --notebook toy_torch_training.ipynb"
training-manager serve
```

Why this mode exists:

- validates `.ipynb` supervision
- validates Torch training under notebook execution
- validates `TrainingReporter` stages / metrics / checkpoints
- does not require the full LLM hardware budget

## 2. Real full-pipeline execution on a richer host

```bash
training-manager init --path /absolute/path/to/Lavender-2 --name lavender-full \
  --command "python3 train.py --notebook full_llm_pipeline.ipynb"
training-manager serve
```

## Environment notes

`training-manager` injects:

- `TRAINING_MANAGER_DIR` — target directory for events / metrics / runtime files
- `PYTHONPATH` — includes the local `training-manager` source tree so
  `training_manager.sdk` is importable from managed jobs without separately
  installing the package into every project venv

## Diagnostics

Manager-internal diagnostics are appended to:

```text
~/.training-manager/manager.log
```

That file is where command-detection failures, JSON parse errors, API handler
errors, failed subprocess calls, and stop/start edge cases now land.
