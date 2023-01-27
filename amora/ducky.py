import usb_hid
from adafruit_hid.keyboard import Keyboard

# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode

# uncomment these lines for non_US keyboards
# replace LANG with appropriate language
# from keyboard_layout_win_LANG import KeyboardLayout
# from keycode_win_LANG import Keycode

import time
from board import LED
import asyncio

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)


def delay(millis):
    time.sleep(float(millis) / 1000)


def prefix_checker(line: str):
    def checker(*prefixes):
        for prefix in prefixes:
            if line.startswith(prefix):
                return line[len(prefix) + 1 :]

    return checker


# TODO: send this to the logs pane of the web interface
def log(message: str):
    print("[log]: " + message)


def run_script(contents):
    default_delay = 0
    previous_line = None
    for line in filter(None, contents.splitlines()):
        line = line.rstrip()
        after = prefix_checker(line)
        # we only run a command once by default
        run_n_times = 1
        if repeat := after("REPEAT"):
            if not previous_line:
                continue
            run_n_times = int(repeat)
            line = previous_line

        for _ in range(run_n_times):
            if after("REM"):
                continue
            if (millis := after("DELAY")) is not None:
                if millis == "":
                    millis = default_delay
                delay(millis)
            elif message := after("PRINT"):
                log(message)
            elif path := after("IMPORT"):
                run_script_file(path)
            elif millis := after("DEFAULT_DELAY", "DEFAULTDELAY"):
                default_delay = int(millis) * 10
            elif after("LED") is not None:
                led.value ^= True
            elif string := after("STRING"):
                layout.write(string)
            else:
                # loop on each key filtering empty values
                for key in filter(None, line.split(" ")):
                    key = key.upper()
                    if command_keycode := Keycode.__dict__.get(key):
                        # If this is a valid key, send its keycode
                        kbd.press(command_keycode)
                        continue
                    # If it's not a known key name, log it for diagnosis
                    log(f"unknown key: <{key}>")
                kbd.release_all()

        previous_line = line
        delay(default_delay)


def run_script_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            run_script(handle.read())
    except OSError as e:
        log(f"unable to open file {path}: {e}")
