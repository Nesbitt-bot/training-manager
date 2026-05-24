Maintainer notes
================

Repository goals
----------------

This repo should stay:

* easy to install on a plain Linux host
* understandable without framework archaeology
* useful for real training jobs before it becomes fancy

Good next steps
---------------

* explicit job configuration from CLI and UI
* restart action in the UI
* better checkpoint discovery and display
* streaming logs or incremental log fetch
* richer metrics charts
* auth story for remote exposure behind a trusted proxy
* packaging and publishing workflow

Caution
-------

Do not over-abstract the runtime model too early. This project is mainly
valuable because it remains inspectable and boring.
