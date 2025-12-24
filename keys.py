import subprocess
import time
import os
import settings
from evdev import UInput, ecodes as e


# set cocket path
os.environ['YDOTOOL_SOCKET'] = '/tmp/.ydotool_socket'

baseMoveSpeed = 31

#key codes
KEYS = {
    'a': '30', 'b': '48', 'c': '46', 'd': '32', 'e': '18',
    'f': '33', 'g': '34', 'h': '35', 'i': '23', 'j': '36',
    'k': '37', 'l': '38', 'm': '50', 'n': '49', 'o': '24',
    'p': '25', 'q': '16', 'r': '19', 's': '31', 't': '20',
    'u': '22', 'v': '47', 'w': '17', 'x': '45', 'y': '21',
    'z': '44',
    '0': '11', '1': '2', '2': '3', '3': '4', '4': '5',
    '5': '6', '6': '7', '7': '8', '8': '9', '9': '10',
    '<': '51', '>' : '52',
    'space': '57', 'shift': '42', 'esc': '1', 'enter': '28',
    'backspace': '14', 'tab': '15', 'ctrl': '29', 'alt': '56',
    'capslock': '58', 'up': '103', 'down': '108', 'left': '105',
    'right': '106',
    'f1': '59', 'f2': '60', 'f3': '61', 'f4': '62',
    'f5': '63', 'f6': '64', 'f7': '65', 'f8': '66',
    'f9': '67', 'f10': '68', 'f11': '87', 'f12': '88',
}


capabilities = {
    e.EV_KEY: [
        e.BTN_LEFT,
        e.BTN_RIGHT,
        e.BTN_MIDDLE,
    ],
    e.EV_REL: [
        e.REL_X,
        e.REL_Y,
        e.REL_WHEEL,
    ],
}

ui = UInput(capabilities, name="virtual-mouse")

def lmb_down():
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)
    ui.syn()

def lmb_up():
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)
    ui.syn()

def move(dx, dy):
    ui.write(e.EV_REL, e.REL_X, dx)
    ui.write(e.EV_REL, e.REL_Y, dy)
    ui.syn()

def scroll(amount):
    ui.write(e.EV_REL, e.REL_WHEEL, amount)
    ui.syn()



def press(key_name):
    key = key_name.lower()
    if key in KEYS:
        code = KEYS[key]
        subprocess.run(['ydotool', 'key', f'{code}:1', f'{code}:0'])
    else:
        print(f"Unknown key: {key_name}")


def hold(key_name, duration=0.1):
    key = key_name.lower()
    speed_multiplier = baseMoveSpeed / settings.moveSpeed
    if key in KEYS:
        code = KEYS[key]
        subprocess.run(['ydotool', 'key', f'{code}:1'])
        time.sleep(duration * speed_multiplier)
        subprocess.run(['ydotool', 'key', f'{code}:0'])
    else:
        print(f"Unknown key: {key_name}")


def key_down(key_name):
    key = key_name.lower()
    if key in KEYS:
        code = KEYS[key]
        subprocess.run(['ydotool', 'key', f'{code}:1'])
    else:
        print(f"Unknown key: {key_name}")


def key_up(key_name):
    key = key_name.lower()
    if key in KEYS:
        code = KEYS[key]
        subprocess.run(['ydotool', 'key', f'{code}:0'])
    else:
        print(f"Unknown key: {key_name}")


def combo(*keys_list):
    codes = []
    for key in keys_list:
        k = key.lower()
        if k in KEYS:
            codes.append(KEYS[k])
        else:
            print(f"Unknown key: {key}")
            return
    for code in codes:
        subprocess.run(['ydotool', 'key', f'{code}:1'])
    time.sleep(0.05)
    for code in reversed(codes):
        subprocess.run(['ydotool', 'key', f'{code}:0'])


def type_text(text):
    subprocess.run(['ydotool', 'type', text])


def wait(seconds):
    time.sleep(seconds)
