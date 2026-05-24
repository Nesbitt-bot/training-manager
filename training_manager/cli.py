from __future__ import annotations

import argparse

from .paths import DEFAULT_HOST, DEFAULT_PORT
from .project import init_project, list_projects
from .server import serve


def main() -> None:
    parser = argparse.ArgumentParser(prog="training-manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--name", required=True)
    p_init.add_argument("--repo")
    p_init.add_argument("--path")
    p_init.add_argument("--command", help="override the detected job command, e.g. 'python3 train.py --notebook toy_torch_training.ipynb'")

    p_serve = sub.add_parser("serve")
    p_serve.add_argument("--host", default=DEFAULT_HOST)
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT)

    sub.add_parser("list")

    args = parser.parse_args()
    if args.cmd == "init":
        cfg = init_project(args.name, repo=args.repo, path=args.path, command=args.command)
        print(cfg["repo_path"])
    elif args.cmd == "serve":
        serve(args.host, args.port)
    elif args.cmd == "list":
        for row in list_projects():
            print(f"{row['name']}\t{row['path']}\t{row['mode']}")


if __name__ == "__main__":
    main()
