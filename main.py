import gui
import patterns
import threading
import time
import subprocess
import os
import paths



#set ydotool socket path
socket_path = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = socket_path



def start_ydotool():

    #kill old processes
    subprocess.run(["pkill", "-f", "ydotoold"], stderr=subprocess.DEVNULL)
    
    #fix ambigous issuse
    #also add socket perm to allow python to read it freely
    try:
        proc = subprocess.Popen(
            ['ydotoold', '--socket-path', socket_path, '--socket-perm', '0666'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Log: Launched ydotoold (Socket: {socket_path})")
    except Exception as e:
        print(f"Start error: {e}")
        return None
    
    #wait for start
    time.sleep(1.5)
    return proc


def macro_loop():
    paths_done = False

    time.sleep(1)
    while True:
        if gui.playing:
            if not paths_done:
                paths.Cannon()
                paths.Cannon_pine()
                paths_done = True
            else:
                patterns.CornerXSnake()  # gather non stop
        else:
            paths_done = False
            time.sleep(0.1)

ydotool_proc = start_ydotool()

macro_thread = threading.Thread(target=macro_loop, daemon=True)
macro_thread.start()


try:
    while gui.running:
        gui.Render()
finally:
    print("Cleaning up...")
    if ydotool_proc:
        ydotool_proc.terminate()