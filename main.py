import gui, patterns, threading, time, subprocess, os, settings, paths, queue
from buff_detection import UltraFastBuffScanner

# Wayland socket configuration
socket_path = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = socket_path

# Shared state between threads
buff_state = {
    'current_buffs': {},
    'speed_multiplier': 1.0,
    'lock': threading.Lock()
}

# Simple path queue
path_queue = queue.Queue()

# Make buff_state accessible to keys module
import keys
keys.buff_state = buff_state



PATH_FUNCTIONS = {
    "Hives": paths.Hives,
    "Pepper": paths.Pepper,
    "Cannon": paths.Cannon,
    "Cannon_dandelion": paths.Cannon_dandelion,
    "Cannon_pine": paths.Cannon_pine,
    "Cannon_mushroom": paths.Cannon_mushroom,
    "Cannon_blueflower": paths.Cannon_blueflower,
    "Cannon_sunflower": paths.Cannon_sunflower,
    "Cannon_clover": paths.Cannon_clover,
    "Cannon_strawberry": paths.Cannon_strawberry,
    "Cannon_spider": paths.Cannon_spider,
    "Cannon_bamboo": paths.Cannon_bamboo,
    "Cannon_pineapple": paths.Cannon_pineapple,
    "Cannon_stump": paths.Cannon_stump,
    "Cannon_mountain": paths.Cannon_mountain,
}



STARTUP_BY_FIELD = {
    "Dandelion": ["Cannon", "Cannon_dandelion"],
    "Clover": ["Cannon", "Cannon_clover"],
    "Sunflower": ["Cannon", "Cannon_sunflower"],
    "Mushroom": ["Cannon", "Cannon_mushroom"],
    "Blue Flower": ["Cannon", "Cannon_blueflower"],
    "Strawberry": ["Cannon", "Cannon_strawberry"],
    "Spider": ["Cannon", "Cannon_spider"],
    "Bamboo": ["Cannon", "Cannon_bamboo"],
    "Pineapple": ["Cannon", "Cannon_pineapple"],
    "Stump": ["Cannon", "Cannon_stump"],
    "Mountain": ["Cannon", "Cannon_mountain"],

    # Fields without cannon
    "Pepper": ["Pepper"],
}



def StartYdotool():
    """ 
    Ensures ydotoold is running and the socket is accessible.
    """
    print("Log: Re-starting ydotoold...")
    subprocess.run(["pkill", "-f", "ydotoold"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    
    if os.path.exists(socket_path):
        try: 
            os.remove(socket_path)
        except: 
            pass
    
    try:
        proc = subprocess.Popen(
            ['ydotoold', '--socket-path', socket_path, '--socket-perm', '0666'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for socket readiness
        for _ in range(25):
            if os.path.exists(socket_path):
                print(f"Log: ydotoold is READY at {socket_path}")
                return proc
            time.sleep(0.2)
        
        return None
    except Exception as e:
        print(f"Start error: {e}")
        return None


def BuffScannerThread():
    """
    Separate thread for CONTINUOUS buff scanning.
    Runs independently from movement patterns.
    """
    region = {'x': 0, 'y': 0, 'width': 450, 'height': 200}
    
    scanner = UltraFastBuffScanner(
        templates_folder='Tux-Macro/images',
        region=region,
        threshold=0.75
    )
    
    frame_times = []
    scan_count = 0
    
    print("[SCANNER] Thread started")
    
    try:
        while gui.running:
            if gui.playing:
                scan_start = time.perf_counter()
                
                # Scan for buffs
                found_buffs = scanner.scan()
                
                # Calculate speed multiplier
                speed_multiplier = 1.0
                for buff_name in found_buffs:
                    if 'haste' in buff_name.lower() or 'expedition' in buff_name.lower():
                        speed_multiplier = 1.3  # 30% faster with haste
                        break
                
                # Update shared state (thread-safe)
                with buff_state['lock']:
                    buff_state['current_buffs'] = found_buffs
                    buff_state['speed_multiplier'] = speed_multiplier
                
                # Print buff info
                if found_buffs:
                    output = " | ".join([f"{name} ({data['confidence']:.0%})" 
                                       for name, data in found_buffs.items()])
                    print(f"[SCAN] {output}")
                
                # Performance tracking
                scan_time = time.perf_counter() - scan_start
                frame_times.append(scan_time)
                scan_count += 1
                
                if len(frame_times) > 30:
                    frame_times.pop(0)
                
                # Print FPS every 30 scans
                if scan_count % 30 == 0:
                    avg_time = sum(frame_times) / len(frame_times)
                    avg_fps = 1.0 / avg_time if avg_time > 0 else 0
                    print(f"[SCANNER] FPS: {avg_fps:.1f} | Scan time: {avg_time*1000:.1f}ms")
                
                # Target ~5-10 scans per second (adjust as needed)
                time.sleep(max(0.001, 0.1 - scan_time))  # Aim for 10 Hz
            else:
                time.sleep(0.2)
    
    finally:
        scanner.cleanup()
        print("[SCANNER] Thread stopped")



def MacroLoop():
    """
    Main loop - executes startup paths, then runs pattern.
    Check path_queue to interrupt pattern anytime.
    """
    pattern_functions = {
        "CornerXSnake": patterns.CornerXSnake,
        "E_lol": patterns.E_lol,
        "Stationary": patterns.Stationary
    }
    

    
    startup_done = False
    last_playing = False
    
    print("[MACRO] Thread started")
    
    while gui.running:
        if gui.playing and not last_playing:
            
            time.sleep(3)
            startup_done = False
            last_playing = gui.playing


        if gui.playing:
            
        # === STARTUP SEQUENCE (runs once) ===
            if not startup_done:
                print("=== STARTUP ===")

                startup_paths = STARTUP_BY_FIELD.get(
                    settings.field,
                    ["Cannon"]  # fallback
                )

                for path_name in startup_paths:
                    if path_name in PATH_FUNCTIONS:
                        print(f"[STARTUP] {path_name}")
                        PATH_FUNCTIONS[path_name]()

                startup_done = True
                print("=== PATTERN START ===")



            # === CHECK FOR MANUAL PATH ===
            if not path_queue.empty():
                path_name = path_queue.get()
                if path_name in path_functions:
                    print(f"[PATH] {path_name}")
                    try:
                        path_functions[path_name]()
                    except Exception as e:
                        print(f"[PATH] Error: {e}")
                path_queue.task_done()
                continue
            


            # === RUN PATTERN ===
            pattern_func = pattern_functions.get(settings.pattern, patterns.CornerXSnake)
            


            # Get speed multiplier
            with buff_state['lock']:
                speed_mult = buff_state['speed_multiplier']
            


            # Execute pattern
            try:
                pattern_func()
            except Exception as e:
                if gui.playing:
                    print(f"Pattern error: {e}")
            
            time.sleep(0.01)
        
        else:
            startup_done = False  # Reset on stop
            time.sleep(0.2)
    
    print("[MACRO] Thread stopped")


# === SIMPLE API ===
def DoPath(path_name):
    """
    Execute a path. That's it.
    Usage: DoPath('Cannon')
    """
    path_queue.put(path_name)


# --- Main Entry Point ---
ydotool_proc = StartYdotool()


if ydotool_proc:
    # Start threads
    scanner_thread = threading.Thread(target=BuffScannerThread, daemon=True)
    macro_thread = threading.Thread(target=MacroLoop, daemon=True)
    
    scanner_thread.start()
    macro_thread.start()
    
    try:
        # Keep main thread alive for GUI
        while gui.running:
            gui.Render()
            time.sleep(0.01)
    except KeyboardInterrupt:
        gui.running = False
    finally:
        print("Cleaning up...")
        gui.playing = False
        time.sleep(0.3)
        ydotool_proc.terminate()
        print("Done.")
else:
    print("FATAL: ydotoold failed to start.")