import logs
import os
import json
from ducky import run_script_file


def create(path, contents=b""):
    with open(path, "wb") as h:
        h.write(contents)


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
        with open(path) as h:
            response.send(json.dumps({"contents": h.read()}))
    elif action == "store":
        create(path, body["contents"].encode())
    elif action == "delete":
        os.remove(path)
    elif action == "create":
        create(filename)
    elif action == "run":
        run_script_file(path)
