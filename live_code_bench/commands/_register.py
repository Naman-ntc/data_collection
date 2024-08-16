from typing import Callable, Dict

ALL_COMMANDS: Dict[str, Callable] = {}


def help():
    print("No arguments provided.")
    print("Available commands:")
    for command in ALL_COMMANDS:
        print(f"  {command}")


def register_command(func_or_name: Callable | str):
    if callable(func_or_name):
        func = func_or_name
        name = func.__name__
        ALL_COMMANDS[name] = func
        return func

    else:
        name = func_or_name

        def decorator(func: Callable):
            ALL_COMMANDS[name] = func
            return func

        return decorator


def exec_command(command: str):
    if command in ALL_COMMANDS:
        ALL_COMMANDS[command]()
    else:
        print(f"Unknown command: {command}")
