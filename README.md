# PwnPi - A More Offensive Redteam Appliance

PwnPi Amora is a wireless keystroke injection tool built on the Raspberry Pi Pico W using CircuitPython.

The project makes an attempt to provide a fully featured web IDE for building
and deploying keystroke injection scripts.

![Preview](assets/preview.png)

## Getting Started

```sh
uv sync
source .venv/bin/activate
circup install asyncio adafruit_hid adafruit_httpserver
python build.py
```

Copy all files inside the `build/` directory to the board.

Check out the [wiki](https://github.com/lavafroth/pwnpi-amora/wiki/) for getting started.
