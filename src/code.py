"""
The entrypoint for our circuitpython board.
"""

import asyncio
import os

import microcontroller
import socketpool
import wifi
from adafruit_httpserver import POST, FileResponse, Request, Server

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
    server = Server(pool)

    @server.route("/")
    def base(request: Request):
        return FileResponse(request, "index.html", root_path="/static")

    @server.route("/main.css")
    def css(request: Request):
        return FileResponse(request, "main.css", root_path="/static")

    @server.route("/script.js")
    def javascript(request: Request):
        return FileResponse(request, "script.js", root_path="/static")

    @server.route("/api", POST)
    def api(request: Request):
        return handle(request)

    server.serve_forever(str(wifi.radio.ipv4_address_ap))


async def run_boot_script():
    """
    If a script with the name 'boot.dd' exists,
    run it without user interaction on boot.
    """
    boot_script = 'payloads/boot.dd'
    if os.path.exists(boot_script):
        run_script_file(boot_script)


if __name__ == "__main__":
    try:
        asyncio.gather(main(), run_boot_script())
    # For some reason, wifi.stop_ap is not implemented.
    except NotImplementedError:
        microcontroller.reset()
