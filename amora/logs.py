import json
logs = []


def consume() -> str:
    dump = json.dumps(logs)
    logs.clear()
    return dump


def log(message: str):
    logs.append("info: " + message)
