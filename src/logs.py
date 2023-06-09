"""
A very bare-bones logging implementation
for the bottom pane of the Web UI.
"""

import json

logs = []


def consume() -> str:
    """
    Convert all the log entries from the module's global mutable
    list to json return them, clearing the list after the dump.
    """
    dump = json.dumps(logs)
    logs.clear()
    return dump


def info(message: str):
    """
    Add a log entry with the message prepended with the info marker
    """
    logs.append("info: " + message)


def warn(message: str):
    """
    Add a log entry with the message prepended with the warning marker
    """
    logs.append("warning: " + message)
