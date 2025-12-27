import keys
import time

'''CORNER_X_SNAKE = [
    ("hold", "w", 2.0),
    ("wait", None, 0.05),  # <- krótka przerwa żeby puścić klawisz
    
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
    time.sleep(2)
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

def E_lol():
    global patternFinished

    patternFinished = False
    keys.hold('w', 0.25)
    keys.hold('d', 0.25)
    keys.hold('s', 0.25)
    keys.hold('a', 0.25)
    patternFinished = True