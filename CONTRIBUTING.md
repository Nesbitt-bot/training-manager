# Contributing

## Local setup

```bash
python3 -m pip install -e .
```

## Basic smoke test

```bash
training-manager --help
training-manager list
training-manager serve
```

## Development expectations

- keep the core flow host-native and debuggable
- prefer small explicit state files over hidden magic
- do not assume Docker, Kubernetes, or cloud training infra
- avoid adding heavyweight dependencies without a clear operational need
- preserve detached-process fallback when supervisor is unavailable

## Docs

- update `README.md` for user-facing behavior changes
- update files in `docs/` for maintainer-facing architecture or workflow changes
- if the GitHub Pages site exists, keep it aligned with the repo docs
