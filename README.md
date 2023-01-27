# PwnPi - A More Offensive Redteam Appliance

PwnPi Amora is a wireless keystroke injection tool built on the Raspberry Pi Pico W using CircuitPython.

## Quick Start
- Download the latest CircuitPython U2F (preferably stable release if it exists) file from [here](https://circuitpython.org/board/raspberry_pi_pico_w/).
- Plug in your Raspberry Pi Pico W while pressing the `BOOTSEL` button. Once plugged in, it should be visible as a USB drive.
- Drag and drop the `adafruit-circuitpython-raspberry_pi_pico_w-xx_XX-x.x.x.x.uf2` image onto the newly visible drive. After a while, it will reload with the label `CIRCUITPY`.
- Download the `adafruit-circuitpython-bundle-8.x-mpy-xxxxxxxx.zip` bundle from [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest).
- Extract `adafruit_hid`, `adafruit_httpserver`, `asyncio` and `adafruit_ticks.mpy` from the zip file to the `lib` directory of the `CIRCUITPY` drive. The board will reload.
- Modify the WiFi SSID and password in `amora/settings.toml`.
- Copy all the files from the `amora` directory to the drive. The board will reload again.
- Connect to the newly spawned network and go to [`192.168.4.1`](http://192.168.4.1)

## Acknowledgement

A huge thank you to David Bailey (dbisu, @dbisu) for his pico-ducky project.
A lot of the HID code from his project was the foundation for this project.
However, a lot of it has undergone so much of refactoring that the old code is almost nonexistent. 