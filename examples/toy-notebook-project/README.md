# Toy notebook project

This is a tiny example project shipped with `training-manager`.

Purpose:

- prove that `training-manager` can supervise notebook-based Torch training
- emit `TrainingReporter` stages / metrics / checkpoints
- stay CPU-friendly enough for local validation on a small host

Run it under `training-manager` with:

```bash
training-manager init --path /absolute/path/to/training-manager/examples/toy-notebook-project --name toy-notebook
training-manager serve
```

The project wrapper uses `uv sync` and then executes `train.ipynb` through
`jupyter nbconvert --execute`.
This example exists only as a managed-job fixture; it is not intended to be a
published standalone package.
