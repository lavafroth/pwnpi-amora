import json
import os

import logs
from ducky import run_script, run_script_file


def create(path, contents=b""):
    with open(path, "wb") as file:
        file.write(contents)


def handle(body, response):
    action = body["action"]
    if action == "list":
        response.send(json.dumps(os.listdir("payloads")))
        return

    if action == "logs":
        response.send(logs.consume())
        return

    filename = body.get("filename")
    path = f"payloads/{filename}"
    if action == "load":
        with open(path) as file:
            response.send(json.dumps({"contents": file.read()}))
    elif action == "store":
        create(path, body["contents"].encode())
    elif action == "delete":
        os.remove(path)
    elif action == "create":
        create(path)
    elif action == "run":
        if filename is not None:
            run_script_file(path)
        elif contents := body["contents"]:
            run_script(contents)
