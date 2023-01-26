# PwnPi - A More Offensive Redteam Appliance

PwnPi Amora is a wireless keystroke injection tool built on the Raspberry Pi Pico W using MicroPython.

## Quick Start
- Plug in your Raspberry Pi Pico W while pressing the `BOOTSEL` button.
- Drag and drop the `adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.0-beta.6.uf2` image onto the newly visible drive.
- Copy all the files in this directory except for the `README.md`, `CODE_OF_CONDUCT.md` and `LICENSE` into the drive once it reloads with the label `CIRCUITPY`
- Modify the WiFi SSID and password in setttings.toml
- Save and the board must auto-reload
- Connect to this network and go to [`192.168.4.1`](http://192.168.4.1)
