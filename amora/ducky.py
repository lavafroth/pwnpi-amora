# License: GPLv3.0
# copyright (c) 2023 Dave Bailey, Himadri Bhattacharjee
# Authors: Dave Bailey (dbisu, @daveisu); Himadri Bhattacharjee (lavafroth, @lavafroth)

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

defaultDelay = 0

duckyCommands = {
    "WINDOWS": Keycode.WINDOWS,
    "GUI": Keycode.GUI,
    "APP": Keycode.APPLICATION,
    "MENU": Keycode.APPLICATION,
    "SHIFT": Keycode.SHIFT,
    "ALT": Keycode.ALT,
    "CONTROL": Keycode.CONTROL,
    "CTRL": Keycode.CONTROL,
    "DOWNARROW": Keycode.DOWN_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFTARROW": Keycode.LEFT_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHTARROW": Keycode.RIGHT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "UPARROW": Keycode.UP_ARROW,
    "UP": Keycode.UP_ARROW,
    "BREAK": Keycode.PAUSE,
    "PAUSE": Keycode.PAUSE,
    "CAPSLOCK": Keycode.CAPS_LOCK,
    "DELETE": Keycode.DELETE,
    "END": Keycode.END,
    "ESC": Keycode.ESCAPE,
    "ESCAPE": Keycode.ESCAPE,
    "HOME": Keycode.HOME,
    "INSERT": Keycode.INSERT,
    "NUMLOCK": Keycode.KEYPAD_NUMLOCK,
    "PAGEUP": Keycode.PAGE_UP,
    "PAGEDOWN": Keycode.PAGE_DOWN,
    "PRINTSCREEN": Keycode.PRINT_SCREEN,
    "ENTER": Keycode.ENTER,
    "SCROLLLOCK": Keycode.SCROLL_LOCK,
    "SPACE": Keycode.SPACE,
    "TAB": Keycode.TAB,
    "BACKSPACE": Keycode.BACKSPACE,
    "A": Keycode.A,
    "B": Keycode.B,
    "C": Keycode.C,
    "D": Keycode.D,
    "E": Keycode.E,
    "F": Keycode.F,
    "G": Keycode.G,
    "H": Keycode.H,
    "I": Keycode.I,
    "J": Keycode.J,
    "K": Keycode.K,
    "L": Keycode.L,
    "M": Keycode.M,
    "N": Keycode.N,
    "O": Keycode.O,
    "P": Keycode.P,
    "Q": Keycode.Q,
    "R": Keycode.R,
    "S": Keycode.S,
    "T": Keycode.T,
    "U": Keycode.U,
    "V": Keycode.V,
    "W": Keycode.W,
    "X": Keycode.X,
    "Y": Keycode.Y,
    "Z": Keycode.Z,
    "F1": Keycode.F1,
    "F2": Keycode.F2,
    "F3": Keycode.F3,
    "F4": Keycode.F4,
    "F5": Keycode.F5,
    "F6": Keycode.F6,
    "F7": Keycode.F7,
    "F8": Keycode.F8,
    "F9": Keycode.F9,
    "F10": Keycode.F10,
    "F11": Keycode.F11,
    "F12": Keycode.F12,
}


def convertLine(line):
    newline = []
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            newline.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    # print(newline)
    return newline


def runScriptLine(line):
    if (
        parse_line_header(["REM"], line, lambda _: _)
        or parse_line_header(["DELAY"], line, lambda x: time.sleep(float(x) / 1000))
        or parse_line_header(["PRINT"], line, lambda x: print("[log]: " + x))
        or parse_line_header(["IMPORT"], line, runScript)
        or parse_line_header(["DEFAULT_DELAY", "DEFAULTDELAY"], line, set_delay)
        or parse_line_header(["LED"], line, invert_led)
        or parse_line_header(["STRING"], line, layout.write)
    ):
        return

    for k in convertLine(line):
        kbd.press(k)
    kbd.release_all()


def parse_line_header(headers, line, func):
    for header in headers:
        if line.startswith(header):
            func(line[len(header) + 1 :])
            return True
    return False


def set_delay(delay):
    global defaultDelay
    defaultDelay = int(delay) * 10


def invert_led(*args):
    led.value ^= True


def runScript(duckyScriptPath: str):
    global defaultDelay

    try:
        with open(duckyScriptPath, "r", encoding="utf-8") as handle:
            contents = handle.read()
    except OSError as e:
        print(f"Unable to open file {duckyScriptPath}: {e}")
        return

    previous_line = None
    for line in map(lambda x: x.rstrip(), filter(None, contents.splitlines())):
        if line[0:6] == "REPEAT":
            if not previous_line:
                continue
            for _ in range(int(line[7:])):
                # repeat the last command
                runScriptLine(previous_line)
        else:
            runScriptLine(line)
            previous_line = line
        time.sleep(float(defaultDelay) / 1000)
