# training-manager

A lightweight web UI and process wrapper for long-running Python and notebook training jobs.

## What it is

`training-manager` is meant for the awkward middle ground between:

- raw terminal sessions that die when a shell closes
- giant orchestration stacks that are overkill for a single workstation or lab box

It gives future maintainers a small control surface for training repos that need to keep running while still being inspectable from a browser.

## Core ideas

- host-native first
- readable local state
- simple Python packaging
- graceful fallback when `supervisord` is missing
- structured training telemetry when available, plain logs when not

## Start here

- [Getting started](getting-started.md)
- [Architecture](architecture.md)
- [Environment setup](environment-setup.md)
- [Lavender-2 integration](lavender-2.md)
- [Maintainer notes](maintainer-notes.md)
