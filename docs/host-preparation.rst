Host preparation
================

This page is a generic checklist for machines that will run
``training-manager`` and managed jobs.

Baseline requirements
---------------------

* Python 3.11 or newer
* enough disk for the managed project, virtual environment, logs, and artifacts
* ability to run long-lived local processes
* browser access to the host, or SSH tunneling to the local UI port

Optional host features
----------------------

* ``supervisord`` and ``supervisorctl`` if you want supervisor-backed mode
* GPU drivers / CUDA runtime when the managed project actually needs them
* reverse proxy / authentication if the UI will leave localhost

Recommended checks
------------------

Confirm Python::

   python3 --version

Confirm process-manager availability if desired::

   command -v supervisord
   command -v supervisorctl

Confirm the UI port is free::

   ss -ltn | grep 14514 || true

Run the UI locally::

   training-manager serve

Then open::

   http://127.0.0.1:14514

Managed project expectations
----------------------------

``training-manager`` supervises a command; it does not replace the managed
project's own environment rules.

Examples:

* a plain Python project may run ``python3 train.py``
* a notebook-first project may run a wrapper such as
  ``python3 train.py --notebook train.ipynb``
* a project may perform its own environment setup internally before launching
  the real job

Logs to know
------------

Managed job log::

   ~/.training-manager/projects/<name>/.training-manager/logs/train.log

Manager internal log::

   ~/.training-manager/manager.log

Use the manager log first when a project fails before its own job log becomes
informative.
