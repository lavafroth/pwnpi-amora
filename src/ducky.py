"""
Logic to interpret and execute user defined ducky script payloads.
"""
import time

import usb_hid
from adafruit_hid.keyboard import Keyboard

# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from board import LED

from logs import info, warn

# uncomment these lines for non_US keyboards
# replace LANG with appropriate language
# from keyboard_layout_win_LANG import KeyboardLayout
# from keycode_win_LANG import Keycode


kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)


def delay(millis):
    """
    Sleep, do absolutely nothing.
    """
    time.sleep(float(millis) / 1000)


def prefix_checker(line: str):
    """
    Returns a function that checks if line begins with
    any of the prefixes supplied to it.

    Syntax sugar so that we can later use it in conditional
    statements like if something := checker("foo", "bar")
    """

    def checker(*prefixes):
        for prefix in prefixes:
            if line.startswith(prefix):
                return line[len(prefix) + 1:]
        return None

    return checker


def press_keys(line: str):
    """
    Press all the keys and then release them.
    Really useful for keyboard shortcuts like Meta+R.
    """
    # loop on each key filtering empty values
    for key in filter(None, line.upper().split(" ")):
        if command_keycode := Keycode.__dict__.get(key):
            # If this is a valid key, send its keycode
            kbd.press(command_keycode)
            continue
        # If it's not a known key name, log it for diagnosis
        warn(f"unknown key: <{key}>")
    kbd.release_all()


def repeat(contents: str, times: int):
    """
    If the contents supplied is not empty or None,
    repeat those ducky script lines `times` times.
    """
    if not contents:
        return
    for _ in range(times):
        run_script(contents)


def run_script(contents):
    """
    Interpret the ducky script and execute it line by line
    """
    default_delay = 0
    previous_line = None
    for line in filter(None, contents.splitlines()):
        line = line.rstrip()
        after = prefix_checker(line)

        if times := after("REPEAT"):
            repeat(previous_line, int(times))

        elif after("REM"):
            continue
        elif (millis := after("DELAY")) is not None:
            delay(millis or default_delay)
        elif message := after("PRINT"):
            info(message)
        elif path := after("IMPORT"):
            run_script_file(path)
        elif millis := after("DEFAULT_DELAY", "DEFAULTDELAY"):
            default_delay = int(millis)
        elif after("LED") is not None:
            LED.value ^= True
        elif string := after("STRING"):
            layout.write(string)
        else:
            press_keys(line)

        previous_line = line
        delay(default_delay)


def run_script_file(path: str):
    """
    Try reading and running a ducky script from the supplied path.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            run_script(handle.read())
    except OSError as error:
        warn(f"unable to open file {path}: {error}")


async def run_boot_script():
    """
    If a script with the name 'boot.dd' exists,
    run it without user interaction on boot.
    """
    try:
        with open("payloads/boot.dd", "r", encoding="utf-8") as handle:
            run_script(handle.read())
    except OSError:
        info("boot script does not exist, skipping its execution")
