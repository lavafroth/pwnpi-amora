# PwnPi - A More Offensive Redteam Appliance

PwnPi Amora is a wireless keystroke injection tool built on the Raspberry Pi Pico W using CircuitPython.

Web IDE for and deploying keystroke injection scripts over WiFi.

![Preview](assets/preview.png)

## Getting Started

- Clone this repo
- Hold the BOOTSEL button an plug the device in
- Run the following inside the project directory

```sh
uv sync
source .venv/bin/activate
```

To completely clean the board you can optionally run

```sh
circuitpython-tool uf2 nuke
```

Now install the board firmware

```sh
circuitpython-tool uf2 install --board raspberry_pi_pico_w
```

Mount the drive after it appears as `CIRCUITPY`.

```sh
circup install asyncio adafruit_hid adafruit_httpserver
```

- Copy all files inside the `src/` directory to the board.
- Unmount and eject the drive.
- Plug the device back in.
- Connect to `http://192.168.4.1`
