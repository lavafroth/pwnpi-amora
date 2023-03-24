import json
logs = []


def consume() -> str:
    dump = json.dumps(logs)
    logs.clear()
    return dump


def info(message: str):
    logs.append("info: " + message)


def warn(message: str):
    logs.append("warning: " + message)
