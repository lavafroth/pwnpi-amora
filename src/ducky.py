"""
Execute user defined python scripts in a sandbox
"""

import time

import usb_hid
from adafruit_hid.keyboard import Keyboard

# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from board import LED
import digitalio
from logs import info, warn

led = digitalio.DigitalInOut(LED)
led.direction = digitalio.Direction.OUTPUT


# uncomment these lines for non_US keyboards
# replace LANG with appropriate language
# from keyboard_layout_win_LANG import KeyboardLayout
# from keycode_win_LANG import Keycode


kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)


def delay(millis=1000.0):
    """
    Sleep, do absolutely nothing.
    """
    time.sleep(float(millis) / 1000)


def press(*keys):
    """
    Press all the keys and then release them.
    """

    # If a single key is invalid, fail fast
    for key in keys:
        if key not in Keycode.__dict__:
            warn(f"unknown key: <{key}>")
            return

    for key in keys:
        if command_keycode := Keycode.__dict__.get(key):
            # If this is a valid key, send its keycode
            kbd.press(command_keycode)
    kbd.release_all()


def toggle_led(value: bool):
    led.value = value


def run_script(contents: str):
    """
    Interpret the ducky script and execute it line by line
    """
    exec(
        contents,
        dict(
            print=info,
            write=layout.write,
            toggle_led=toggle_led,
            delay=delay,
            press=press,
        ),
    )


def run_script_file(path: str):
    """
    Try reading and running a python script from the supplied path.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            run_script(handle.read())
    except OSError as error:
        warn(f"unable to open file {path}: {error}")


async def run_boot_script():
    """
    Try reading and running a python script from the supplied path.
    """
    try:
        with open("boot_payload.py", "r", encoding="utf-8") as handle:
            run_script(handle.read())
    except OSError:
        info("not boot script set")
