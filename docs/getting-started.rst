Getting started
===============

Installation
------------

For local development::

   python3 -m pip install -e .

Start the UI::

   training-manager serve

Open ``http://127.0.0.1:14514``.

Initialize a project
--------------------

From a repository URL::

   training-manager init --name my-project --repo https://github.com/example/repo.git

From an existing local checkout::

   training-manager init --name my-project --path /path/to/project

If the default command detection is not enough, override it explicitly::

   training-manager init --name my-project --path /path/to/project \
     --command "python3 train.py --notebook train.ipynb"

This is the preferred pattern for notebook-first projects that need a wrapper
around environment setup.
