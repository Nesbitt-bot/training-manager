CLI reference
=============

``training-manager init``
-------------------------

Initialize a managed project.

Examples::

   training-manager init --name my-project --repo https://github.com/example/repo.git
   training-manager init --name my-project --path /srv/my-project
   training-manager init --name my-project --path /srv/my-project \
     --command "python3 train.py --notebook train.ipynb"

Arguments:

* ``--name``: logical project name used in the registry
* ``--repo``: git URL to clone into the managed projects area
* ``--path``: existing local path to copy into the managed projects area
* ``--command``: optional override for the detected job command

``training-manager serve``
--------------------------

Start the local web UI::

   training-manager serve --host 127.0.0.1 --port 14514

``training-manager list``
-------------------------

List known projects::

   training-manager list
