# Maintainer backlog

This file is the working backlog before turning items into GitHub issues.
Keep it practical and sortable.

## Ready next

- [ ] Add CLI commands for `start`, `stop`, `pull`, `push`, and `checkpoint`
- [ ] Let users override the detected command during `init`
- [ ] Surface stderr/exit-code failures more clearly in the UI
- [ ] Add a refresh button and project auto-select highlighting
- [ ] Add a minimal project README example with `TrainingReporter`

## Needs design

- [ ] Decide whether project configs should be editable from the browser
- [ ] Decide how far notebook support should go beyond `nbconvert --execute`
- [ ] Decide whether supervisor and detached mode should share a stricter runtime contract
- [ ] Decide how much history should stay in `runtime.json` vs separate event files

## Good first issues

- [ ] Add timestamps to rendered log view
- [ ] Empty-state polish for projects with no metrics yet
- [ ] Add copyable command snippets in docs
- [ ] Add small fixtures for metrics/events parsing
- [ ] Add screenshots captured from a real run

## Deferred

- [ ] Authentication inside the app itself
- [ ] Multi-user concepts
- [ ] Remote artifact browsing
- [ ] Plugin system / external storage backends
