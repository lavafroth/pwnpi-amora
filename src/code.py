"""
The entrypoint for our circuitpython board.
"""

import asyncio
import json
import os

import microcontroller
import socketpool
import wifi
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer

from api import handle


async def main():
    """
    Begin a wifi access point defined by the SSID and PASSWORD environment
    variables.
    Spawn a socketpool on this interface.
    Serve the web interface over this socketpool indefinitely using an HTTP
    server.
    """
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
    def javascript(request: HTTPRequest):
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
