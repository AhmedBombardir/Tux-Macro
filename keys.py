import subprocess
import time
import os
import settings
from evdev import UInput, ecodes as e

os.environ['YDOTOOL_SOCKET'] = '/tmp/.ydotool_socket'

baseMoveSpeed = 31

buff_state = None

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
        e.KEY_A, e.KEY_B, e.KEY_C, e.KEY_D, e.KEY_E,
        e.KEY_F, e.KEY_G, e.KEY_H, e.KEY_I, e.KEY_J,
        e.KEY_W, e.KEY_S, e.KEY_SPACE,
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
    ui.write(e.EV_REL, e.REL_X, int(dx))
    ui.write(e.EV_REL, e.REL_Y, int(dy))
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


def hold(key_name, duration=0.1, adjusted=True):
    """
    Hold a key for specified duration.
    Automatically compensates for speed buffs and moveSpeed settings.
    """
    key = key_name.lower()
    
    # CHANGED: Get effective movespeed (base + bear morph bonus)
    effective_movespeed = settings.moveSpeed
    if buff_state is not None:
        try:
            with buff_state['lock']:
                if buff_state.get('bear_morph_active', False):
                    effective_movespeed = settings.moveSpeed + 6
        except:
            pass
    
    # Calculate speed multiplier based on effective movespeed
    speed_multiplier = baseMoveSpeed / effective_movespeed
    
    # Get haste buff multiplier
    buff_speed = 1.0
    if buff_state is not None:
        try:
            with buff_state['lock']:
                buff_speed = buff_state['speed_multiplier']
        except:
            pass
    
    # Combine both multipliers
    total_multiplier = speed_multiplier / buff_speed
    
    adjusted_duration = duration * total_multiplier
    
    if key in KEYS:
        code = KEYS[key]
        subprocess.run(['ydotool', 'key', f'{code}:1'])
        time.sleep(adjusted_duration)
        subprocess.run(['ydotool', 'key', f'{code}:0'])
    else:
        print(f"Unknown key: {key_name}")


def key_down(key_name):
    key = key_name.lower()
    if key in KEYS:
        key_code = getattr(e, f'KEY_{key.upper()}', None)
        if key_code:
            ui.write(e.EV_KEY, key_code, 1)
            ui.syn()
    else:
        print(f"Unknown key: {key_name}")


def key_up(key_name):
    key = key_name.lower()
    if key in KEYS:
        key_code = getattr(e, f'KEY_{key.upper()}', None)
        if key_code:
            ui.write(e.EV_KEY, key_code, 0)
            ui.syn()
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
    """
    Wait for specified duration.
    Also compensates for speed buffs.
    """
    # CHANGED: Get effective movespeed (base + bear morph bonus)
    effective_movespeed = settings.moveSpeed
    if buff_state is not None:
        try:
            with buff_state['lock']:
                if buff_state.get('bear_morph_active', False):
                    effective_movespeed = settings.moveSpeed + 6
        except:
            pass
    
    # Calculate speed multiplier based on effective movespeed
    speed_multiplier = baseMoveSpeed / effective_movespeed
    
    # Get haste buff multiplier
    buff_speed = 1.0
    if buff_state is not None:
        try:
            with buff_state['lock']:
                buff_speed = buff_state['speed_multiplier']
        except:
            pass
    
    # Combine both multipliers
    total_multiplier = speed_multiplier / buff_speed
    
    adjusted_wait = seconds * total_multiplier
    time.sleep(adjusted_wait)