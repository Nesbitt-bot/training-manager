Examples
========

Toy notebook project
--------------------

A small notebook-based Torch training example ships in the repository at::

   examples/toy-notebook-project/

Use it to validate that ``training-manager`` can supervise ``.ipynb`` training,
collect metrics, and collect checkpoints without needing a large training box.

Example::

   training-manager init \
     --name toy-notebook \
     --path /absolute/path/to/training-manager/examples/toy-notebook-project
   training-manager serve

The example project uses a small wrapper script that performs ``uv sync`` and
then executes ``train.ipynb`` through ``jupyter nbconvert --execute``.
