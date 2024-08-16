import sys
from pprint import pprint
from time import sleep
from typing import Callable

from .commands._register import exec_command, help


def _start(args=sys.argv):
    for i, arg in enumerate(args):
        print(f"Arg #{i}: {arg}")
    return args


def _has_no_args(args):
    return len(args) <= 1


def main():
    """
    Execution entry point.
    """
    args = _start()

    if _has_no_args(args):
        help()
        return

    (
        exec_path,
        command,
        *rest,
    ) = args

    print("=" * 80)
    exec_command(command)
