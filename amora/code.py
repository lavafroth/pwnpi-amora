import microcontroller
import wifi
import socketpool
import asyncio
import os
import json
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
from ducky import run_script_file


async def main():
    wifi.radio.start_ap(ssid=os.getenv("SSID"), password=os.getenv("PASSWORD"))
    pool = socketpool.SocketPool(wifi.radio)
    server = HTTPServer(pool)

    @server.route("/")
    def base(request: HTTPRequest):
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send_file("static/index.html")

    @server.route("/main.css")
    def css(request: HTTPRequest):
        with HTTPResponse(request, content_type=MIMEType.TYPE_CSS) as response:
            response.send_file("static/main.css")

    @server.route("/script.js")
    def js(request: HTTPRequest):
        with HTTPResponse(request, content_type=MIMEType.TYPE_JS) as response:
            response.send_file("static/script.js")

    @server.route("/api", HTTPMethod.POST)
    def api(request: HTTPRequest):
        body = json.loads(request.body)
        action = body["action"]
        with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
            if action == "list":
                response.send(json.dumps(os.listdir("payloads")))
            elif action == "load":
                with open("payloads/" + body["filename"]) as h:
                    response.send(json.dumps({"contents": h.read()}))
            elif action == "store":
                with open(f"payloads/" + body["filename"], "wb") as h:
                    h.write(body["contents"].encode())
            elif action == "delete":
                os.remove("payloads/" + body["filename"])
            elif action == "create":
                with open(f"payloads/" + body["filename"], "wb") as h:
                    h.write(b"")
            elif action == "run":
                run_script_file(f"payloads/" + body["filename"])

    server.start(str(wifi.radio.ipv4_address_ap))
    while True:
        try:
            server.poll()
        except OSError as error:
            print(error)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except NotImplementedError:
        microcontroller.reset()
