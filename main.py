import gui
import patterns
import threading
import time
import subprocess
import os
import paths
import buff_detection
import numpy as np

# Set ydotool socket path for Wayland compatibility
socket_path = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = socket_path

def start_ydotool():
    """Starts the ydotoold daemon to allow virtual input on Wayland"""
    subprocess.run(["pkill", "-f", "ydotoold"], stderr=subprocess.DEVNULL)
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
    time.sleep(1.5)
    return proc

def macro_loop():
    """Main logic loop for the macro"""
    paths_done = False
    
    # IMPORTANT: Adjust these to your screen resolution!
    # Smaller width/height = less CPU usage.
    region = {
        'top': 10,
        'left': 1700,
        'width': 960,  # Reduced from 720 to be more specific
        'height': 320  # Reduced from 480
    }
    
    scanner = buff_detection.MultiBuffScanner(
        buff_images_folder='Tux-Macro/images',
        region=region,
        threshold=0.5
    )

    while gui.running: # Loop only as long as GUI is running
        if gui.playing:
            start_time = time.time()
            
            # Execute scan
            found_buffs = scanner.Scan()
            
            if found_buffs:
                # Group by position to avoid detecting multiple morphs in the same spot
                best_matches = {}
                for buff in found_buffs:
                    pos = buff['position']
                    # Use a small range (e.g., 10px) to treat close coordinates as the same spot
                    pos_key = (pos[0] // 10, pos[1] // 10)
                    
                    if pos_key not in best_matches or buff['confidence'] > best_matches[pos_key]['confidence']:
                        best_matches[pos_key] = buff
                
                print("\n BUFFS FOUND:")
                for buff in best_matches.values():
                    print(f"  • {buff['name']}: {buff['confidence']:.2%}")


            if not paths_done:
                paths_done = True
            else:
                patterns.CornerXSnake()  

            # CAP THE FPS: This prevents system lag.
            # 0.2 seconds = ~5 scans per second.
            elapsed = time.time() - start_time
            wait_time = max(0.01, 0.2 - elapsed) 
            time.sleep(wait_time)
        else:
            paths_done = False
            time.sleep(0.5) # Sleep more when paused to save CPU

# --- Entry Point ---
ydotool_proc = start_ydotool()
macro_thread = threading.Thread(target=macro_loop, daemon=True)
macro_thread.start()

try:
    while gui.running:
        gui.Render()
        time.sleep(0.01) # Small sleep to prevent GUI from eating 100% CPU
finally:
    print("Cleaning up...")
    if ydotool_proc:
        ydotool_proc.terminate()