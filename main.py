import gui, patterns, threading, time, subprocess, os, buff_detection, settings

# Wayland socket configuration
socket_path = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = socket_path

def StartYdotool():
    """ 
    Ensures ydotoold is running and the socket is accessible.
    """
    print("Log: Re-starting ydotoold...")
    subprocess.run(["pkill", "-f", "ydotoold"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    
    if os.path.exists(socket_path):
        try: os.remove(socket_path)
        except: pass

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

def MacroLoop():
    """
    Main logic loop: Scans screen and executes movement patterns.
    """
    # Optimized scan region for better FPS
    region = {'top': 0, 'left': 0, 'width': 450, 'height': 200}
    
    scanner = buff_detection.MultiBuffScanner(
        buff_images_folder='Tux-Macro/images',
        region=region,
        threshold=0.8 
    )

    pattern_functions = {
        "CornerXSnake": patterns.CornerXSnake,
        "E_lol": patterns.E_lol,
        "Stationary": patterns.Stationary
    }

    current_pattern = None
    
    while gui.running:
        if gui.playing:
            if current_pattern is None:
                current_pattern = settings.pattern
                pattern_func = pattern_functions.get(current_pattern, patterns.CornerXSnake)
                print(f"--- MACRO STARTED ({current_pattern}) ---")
            
            loop_start = time.time()
            
            # 1. Screen Scan
            found_buffs = scanner.Scan()
            if found_buffs:
                output = " | ".join([f"{b['name']} ({b['confidence']:.0%})" for b in found_buffs])
                print(f"[SCAN] {output}")

            # 2. Movement (Wrapped in try-except to prevent socket crashes)
            try:
                pattern_func()
            except Exception as e:
                # Silently catch socket errors during shutdown
                if gui.playing:
                    print(f"Movement Warning: {e}")

            # 3. Frequency Control (Aiming for ~10Hz)
            elapsed = time.time() - loop_start
            time.sleep(max(0.001, 1 - elapsed)) 
        else:
            current_pattern = None
            time.sleep(0.2)

# --- Main Entry Point ---
ydotool_proc = StartYdotool()

if ydotool_proc:
    # Start the macro thread
    macro_thread = threading.Thread(target=MacroLoop, daemon=True)
    macro_thread.start()

    try:
        # Keep the main thread alive for the GUI
        while gui.running:
            gui.Render()
            time.sleep(0.01)
    except KeyboardInterrupt:
        gui.running = False
    finally:
        print("Cleaning up...")
        gui.playing = False # Stop the macro loop first
        time.sleep(0.2)     # Give the loop time to finish its last move
        ydotool_proc.terminate()
        print("Done.")
else:
    print("FATAL: ydotoold failed to start.")