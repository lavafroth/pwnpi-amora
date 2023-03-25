import microcontroller
import wifi
import socketpool
import asyncio
import os
import json
from api import handle
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType


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
        with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
            handle(json.loads(request.body), response)

    server.serve_forever(str(wifi.radio.ipv4_address_ap))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    # For some reason, wifi.stop_ap is not implemented.
    except NotImplementedError:
        microcontroller.reset()
