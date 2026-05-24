# Environment setup

## training-manager host requirements

- Python 3.11+
- ability to run long-lived local processes
- optional `supervisord` / `supervisorctl`
- browser access to the host or an SSH tunnel to `127.0.0.1:14514`

## Installing training-manager locally

```bash
python3 -m pip install -e .
training-manager serve
```

## Managed-project expectations

A managed project may have its own environment rules. `training-manager`
does not replace them; it only supervises the configured command.

For example, Lavender-2 is `uv`-managed, so its wrapper command is:

```bash
python3 train.py --notebook toy_torch_training.ipynb
```

and that wrapper itself performs `uv sync` plus notebook execution.

## Logs you should know about

### Managed job log

Stored per project at:

```text
~/.training-manager/projects/<name>/.training-manager/logs/train.log
```

### Manager internal log

Stored globally at:

```text
~/.training-manager/manager.log
```

This log is the first place to look when the UI shows vague failure or when a
project failed before its own job log became informative.
