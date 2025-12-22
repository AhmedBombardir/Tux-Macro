import gui
import patterns
import threading
import time
import subprocess
import os

# Ustawiamy ścieżkę do socketu tam, gdzie ydotool sam go sobie stworzył
socket_path = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = socket_path

def start_ydotool():
    # 1. Zabijamy stare procesy
    subprocess.run(["pkill", "-f", "ydotoold"], stderr=subprocess.DEVNULL)
    
    # 2. Uruchamiamy z jawnym parametrem --socket-path (naprawia błąd 'ambiguous')
    # Dodajemy też --socket-perm 0666, żeby Python mógł swobodnie czytać socket
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
    
    # 3. Czekamy na READY
    time.sleep(1.5)
    return proc

def macro_loop():
    while True:
        if gui.playing:
            patterns.CornerXSnake()
        else:
            time.sleep(0.1)

# --- START ---
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