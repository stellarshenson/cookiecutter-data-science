#!/usr/bin/env python3
"""Docker entrypoint for {{ cookiecutter.project_name }}."""

import argparse
import sys
from importlib.metadata import version

__version__ = version("{{ cookiecutter.project_name }}")


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(
        description="{{ cookiecutter.description }}"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=["run", "train", "predict"],
        help="Command to execute (default: run)",
    )
    args = parser.parse_args()

    if args.command == "run":
        print(f"Running {{ cookiecutter.project_name }} v{__version__}")
        # Add your main execution logic here
    elif args.command == "train":
        from {{ cookiecutter.module_name }}.modeling.train import main as train_main
        train_main()
    elif args.command == "predict":
        from {{ cookiecutter.module_name }}.modeling.predict import main as predict_main
        predict_main()

    return 0


if __name__ == "__main__":
    sys.exit(main())
