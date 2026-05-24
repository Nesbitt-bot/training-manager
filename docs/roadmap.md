# Roadmap

## Near-term

- explicit job editing instead of pure entrypoint inference
- restart action in UI/API
- clearer notebook-job detection and error reporting
- first-class start/stop/pull/push/checkpoint CLI commands
- better log handling for long-running detached jobs

## Next tier

- stream or incrementally fetch logs instead of full refresh polling
- richer charts (multiple axes, smoothing, metric toggles)
- event timeline UI instead of raw JSON dump
- checkpoint browser with file metadata and restore hints
- project settings editor for command/env/checkpoint globs

## Later

- auth / reverse-proxy deployment guidance
- multi-host registry concepts
- artifact links and storage backends
- proper packaging and PyPI release workflow
