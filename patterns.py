import keys
import time

'''CORNER_X_SNAKE = [
    ("hold", "w", 2.0),
    ("wait", None, 0.05),
    
    ("hold", "a", 2.0),
    ("wait", None, 0.05),
    
    ("hold", "d", 1.5),
    ("wait", None, 0.05),
    
    ("hold", "s", 0.2),
    ("wait", None, 0.05),
    
    ("hold", "a", 1.6),
    ("wait", None, 0.05),
    
    ("hold", "s", 0.2),
    ("wait", None, 0.05),
    
    ("hold", "d", 1.5),
    ("wait", None, 0.05),
    
    ("hold", "s", 0.2),
    ("wait", None, 0.05),
    
    ("hold", "a", 1.6),
    ("wait", None, 0.05),
    
    ("hold", "s", 0.2),
    ("wait", None, 0.05),
    
    ("hold", "d", 1.5),
]'''

patternFinished = True

def CornerXSnake():
    global patternFinished
    patternFinished = False

    keys.lmb_down()
    keys.key_down('w')
    keys.key_down('a')
    time.sleep(1.75)
    keys.key_up('w')
    keys.key_up('a')
    keys.hold('d', 1.5)
    keys.hold('s', 0.2)
    keys.hold('a', 1.6)
    keys.hold('s', 0.2)
    keys.hold('d', 1.5)
    keys.hold('s', 0.2)
    keys.hold('a', 1.6)
    keys.hold('s', 0.2)
    keys.hold('d', 1.5)
    keys.key_down('w')
    keys.key_down('a')
    time.sleep(1)
    keys.key_up('w')
    keys.key_up('a')

    
    patternFinished = True
    keys.lmb_up()
    
def Stationary():
    global patternFinished

    patternFinished = False
    keys.lmb_down()
    patternFinished = True


def E_lol(spacing=30, reps=1, size=0.125):
    """
    Customizable version
    Usage: SnakePatternCustom(spacing=183, reps=4, size=1.2)
    """
    global patternFinished
    patternFinished = False
    
    facing_corner = 1
    
    keys.lmb_down()
    
    keys.hold('a', 0.25)
    # First half
    keys.key_down('a')
    keys.wait(spacing * 9 / 2000 * (reps * 2 + 1))
    keys.key_up('a')
    
    keys.hold('s', 5 * size)
    
    for _ in range(reps):
        keys.hold('d', spacing * 9 / 2000)
        keys.hold('w', 5 * size)
        keys.hold('d', spacing * 9 / 2000)
        keys.hold('s', (1094 + 25 * facing_corner) * 9 / 2000 * size)
    
    # Second half
    keys.key_down('a')
    keys.wait(spacing * 9 / 2000 * (reps * 2 + 0.5))
    keys.key_up('a')
    
    keys.hold('w', 5 * size)
    
    for _ in range(reps):
        keys.hold('d', spacing * 9 / 2000)
        keys.hold('s', (1094 + 25 * facing_corner) * 9 / 2000 * size)
        keys.hold('d', spacing * 9 / 2000 * 1.5)
        keys.hold('w', 5 * size)
    
    patternFinished = True
    time.sleep(0.2)
    keys.lmb_up()