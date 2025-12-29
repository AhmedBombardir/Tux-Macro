import gui, patterns, threading, time, subprocess, os, settings
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
    Main movement loop - runs patterns continuously.
    Reads buff state from scanner thread.
    """
    pattern_functions = {
        "CornerXSnake": patterns.CornerXSnake,
        "E_lol": patterns.E_lol,
        "Stationary": patterns.Stationary
    }
    
    current_pattern = None
    
    print("[MACRO] Thread started")
    
    while gui.running:
        if gui.playing:
            if current_pattern is None:
                current_pattern = settings.pattern
                pattern_func = pattern_functions.get(current_pattern, patterns.CornerXSnake)
                print(f"--- MACRO STARTED ({current_pattern}) ---")
            
            # Get current speed multiplier from scanner thread
            with buff_state['lock']:
                speed_mult = buff_state['speed_multiplier']
                active_buffs = list(buff_state['current_buffs'].keys())
            
            # Display speed info occasionally
            if speed_mult > 1.0 and active_buffs:
                print(f"[MACRO] Speed boost active: {speed_mult:.1f}x (Buffs: {active_buffs})")
            
            # Execute movement pattern
            try:
                pattern_func()
            except Exception as e:
                if gui.playing:
                    print(f"Movement Warning: {e}")
            
            # Small delay between pattern executions
            time.sleep(0.01)
        else:
            current_pattern = None
            time.sleep(0.2)
    
    print("[MACRO] Thread stopped")

# --- Main Entry Point ---
ydotool_proc = StartYdotool()

if ydotool_proc:
    # Start BOTH threads
    scanner_thread = threading.Thread(target=BuffScannerThread, daemon=True)
    macro_thread = threading.Thread(target=MacroLoop, daemon=True)
    
    scanner_thread.start()
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
        gui.playing = False  # Stop both loops
        time.sleep(0.3)      # Give threads time to finish
        ydotool_proc.terminate()
        print("Done.")
else:
    print("FATAL: ydotoold failed to start.")