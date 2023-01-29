# PwnPi - A More Offensive Redteam Appliance

PwnPi Amora is a wireless keystroke injection tool built on the Raspberry Pi Pico W using CircuitPython.

## Quick Start

- Download the UF2 image from the [latest release](https://github.com/lavafroth/pwnpi-amora/releases/latest)
- Plug in your Raspberry Pi Pico W while pressing the `BOOTSEL` button. Once plugged in, it should be visible as a USB drive.
- Drag and drop the `amora.uf2` file onto the newly visible drive. The board will auto-reload.

## Developer Setup

> Note: The board auto-reloads after every copy action finishes. Don't worry, your device isn't broken.

- Download the latest CircuitPython UF2 (preferably stable release if it exists) file from [here](https://circuitpython.org/board/raspberry_pi_pico_w/).
- Plug in your Raspberry Pi Pico W while pressing the `BOOTSEL` button. Once plugged in, it should be visible as a USB drive.
- Drag and drop the `adafruit-circuitpython-raspberry_pi_pico_w-xx_XX-x.x.x.x.uf2` image onto the newly visible drive. It will reload with the label `CIRCUITPY`.
- Download the `adafruit-circuitpython-bundle-8.x-mpy-xxxxxxxx.zip` bundle from [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest).
- Extract `adafruit_hid`, `adafruit_httpserver`, `asyncio` and `adafruit_ticks.mpy` from the zip file to the `lib` directory of the `CIRCUITPY` drive.
- Copy all the files from the `amora` directory to the root of the drive.

## Usage

- Connect to the newly spawned WiFi network. Default SSID and password are `amora`:`pwnpiamora`
- Visit the web editor at [`192.168.4.1`](http://192.168.4.1)

## FAQ

### How do I change the wireless network name or password?

Modify the WiFi SSID and password in `settings.toml`.

### How is the binary release different from manual setup?

The binary release has the web files minified and embedded inside the `code.py` file.
There is no static directory. Although this saves some space in terms of flash memory, it makes it difficult to customize the UI or functionality.

If you wish to style the UI different or add extra functionality to the code, please follow the [developer setup](https://github.com/lavafroth/pwnpi-amora#developer-setup).

## Video Guide

[![Video Thumbnail](https://thumbnails.odycdn.com/optimize/s:720:400/quality:85/plain/https://thumbs.odycdn.com/782a20086911e18bedf17c8651b84c07.webp)](https://odysee.com/@lavafroth:d/amora_setup_guide:8)

## Acknowledgement

A huge thank you to David Bailey (dbisu, @dbisu) for his pico-ducky project which has served as the foundation for the HID side of this project. Although, the old code is almost nonexistent due to intensive refactoring.
