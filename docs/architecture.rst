Architecture
============

State model
-----------

Global state root::

   ~/.training-manager/

Important files:

* ``registry.json`` — known projects
* ``manager.log`` — manager-internal diagnostics
* ``projects/<name>/.training-manager/project.json`` — project config
* ``projects/<name>/.training-manager/runtime.json`` — current runtime state
* ``projects/<name>/.training-manager/events.jsonl`` — stage/progress/checkpoint events
* ``projects/<name>/.training-manager/metrics.jsonl`` — scalar metrics
* ``projects/<name>/.training-manager/logs/train.log`` — aggregated job log

Runtime model
-------------

Two execution modes exist:

#. ``supervisor`` mode when ``supervisord`` and ``supervisorctl`` are available
#. ``detached`` mode using ``subprocess.Popen(..., start_new_session=True)`` otherwise

Command detection
-----------------

By default, ``training-manager`` looks for one of these entrypoints in the
managed repo:

#. ``train.py``
#. ``scripts/train.py``
#. ``main.py``
#. the first notebook in the repo root
#. otherwise ``python3 -m http.server 0`` as a placeholder fallback

For projects that need a more specific wrapper, use ``--command`` during
initialization.
