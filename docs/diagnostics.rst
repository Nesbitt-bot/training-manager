Diagnostics
===========

Managed job log
---------------

Each managed project writes its aggregated stdout/stderr log to::

   ~/.training-manager/projects/<name>/.training-manager/logs/train.log

Manager internal log
--------------------

Manager-internal diagnostics are appended to::

   ~/.training-manager/manager.log

This log is where the package records things like:

* command-detection choices
* JSON / JSONL parse failures
* failed subprocess calls
* API handler errors
* git pull / push failures
* stop-job escalation and lingering-process state

Structured telemetry
--------------------

When a managed job imports ``training_manager.sdk.TrainingReporter``, it can
append telemetry to the project-local files:

* ``events.jsonl``
* ``metrics.jsonl``

Those files drive the stage, progress, checkpoint, and chart views in the UI.
