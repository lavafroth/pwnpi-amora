"""
A very bare-bones logging implementation
for the bottom pane of the Web UI.
"""

logs = []


def consume() -> str:
    """
    Convert all the log entries from the module's global mutable
    list to json return them, clearing the list after the dump.
    """
    dump = logs.copy()
    logs.clear()
    return dump


def info(message):
    """
    Add a log entry with the message prepended with the info marker
    """
    logs.append("info: " + str(message))


def warn(message: str):
    """
    Add a log entry with the message prepended with the warning marker
    """
    logs.append("warn: " + str(message))
