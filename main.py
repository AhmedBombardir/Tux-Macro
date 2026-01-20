import gui, patterns, threading, time, subprocess, os, settings, re, paths
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

# Make buff_state accessible to keys module
import keys
keys.buff_state = buff_state

field_paths = {
    "Clover": paths.Cannon_clover,
    "Mushroom": paths.Cannon_mushroom,
    "Spider": paths.Cannon_spider,
    "Bamboo": paths.Cannon_bamboo,
    "Strawberry": paths.Cannon_strawberry,
    "Blue Flower": paths.Cannon_blueflower,
    "Pine Tree": paths.Cannon_pine,
    "Pineapple": paths.Cannon_pineapple,
    "Pumpkin": paths.Cannon_pumpkin,
    "Cactus": paths.Cannon_cactus,
    "Stump": paths.Cannon_stump,
    "Rose": paths.Cannon_rose,
    "Dandelion": paths.Cannon_dandelion,
    "Sunflower": paths.Cannon_sunflower,
    "Mountaint": paths.Cannon_mushroom,
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
    print("[SCANNER] Thread started, loading templates...")
    
    region = {'x': 0, 'y': 0, 'width': 450, 'height': 200}
    
    # This loads templates - happens in background thread, doesn't block GUI
    scanner = UltraFastBuffScanner(
        templates_folder='Tux-Macro/images',
        region=region,
        threshold=0.75
    )
    
    print("[SCANNER] Templates loaded, starting scan loop...")
    
    frame_times = []
    scan_count = 0
    
    try:
        while gui.running:
            if gui.playing:
                try:  
                    scan_start = time.perf_counter()
                    
                    # Scan for buffs
                    found_buffs = scanner.scan()
                    
                    # Filter to best match per buff type (e.g., only one "haste" even if haste1, haste5 detected)
                    best_buffs = {}
                    for buff_name, data in found_buffs.items():
                        # Extract buff type without numbers: "haste5" -> "haste"
                        buff_type = ''.join([c for c in buff_name if not c.isdigit()])
                        
                        if buff_type not in best_buffs or data['confidence'] > best_buffs[buff_type]['confidence']:
                            best_buffs[buff_type] = {
                                'name': buff_name,
                                'confidence': data['confidence'],
                                'position': data['position']
                            }
                    
                    # Calculate speed multiplier based on haste LEVEL
                    speed_multiplier = 1.0
                    
                    for buff_type, data in best_buffs.items():
                        buff_name = data['name'].lower()
                        
                        if 'haste' in buff_name:
                            # Extract number: haste7 -> 7, haste10 -> 10
                            match = re.search(r'haste(\d+)', buff_name)
                            if match:
                                haste_level = int(match.group(1))
                                # haste1=1.1x, haste5=1.5x, haste10=2.0x
                                speed_multiplier = 1.0 + (haste_level * 0.1)
                            else:
                                # If no number found (just "haste"), assume level 1
                                speed_multiplier = 1.1
                            break
                        elif 'expedition' in buff_name:
                            # Expedition might have its own multiplier
                            speed_multiplier = 1.25  # Adjust if different
                            break
                    
                    # Update shared state (thread-safe)
                    with buff_state['lock']:
                        buff_state['current_buffs'] = best_buffs
                        buff_state['speed_multiplier'] = speed_multiplier
                    
                    # Print buff info with speed multiplier
                    if best_buffs:
                        output = " | ".join([f"{data['name']} ({data['confidence']:.0%})" 
                                           for data in best_buffs.values()])
                        print(f"[SCAN] {output} → Speed: {speed_multiplier:.2f}x")
                    
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
                
                except Exception as e:
                    print(f"[SCANNER] Error in scan loop: {e}")
                    import traceback
                    traceback.print_exc()
                    time.sleep(0.5)  # Pause before retry
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
    paths_executed = False

    
    print("[MACRO] Thread started")
    
    # Wait for ydotoold to fully stabilize (in background thread, doesn't block GUI)
    print("[MACRO] Waiting for ydotoold to stabilize...")
    time.sleep(2)
    print("[MACRO] Ready!")
    
    while gui.running:
        if gui.playing:
            if current_pattern is None and not paths_executed:

                time.sleep(5)

                paths.Cannon()
                selected_field = settings.field
                field_func = field_paths.get(selected_field)

                if field_func:
                    print(f"[MACRO] Executing: {selected_field} path")
                    field_func()
                else:
                    print(f"[ERROR No path found for field: {selected_field}")

                paths_executed = True


            elif current_pattern is None and paths_executed:

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
                # IMPORTANT: Release LMB if pattern crashes
                try:
                    keys.lmb_up()
                except:
                    pass
            
            # Small delay between pattern executions
            time.sleep(0.01)
        else:
            # Reset when macro stops
            if current_pattern is not None or paths_executed:
                print("[MACRO] Stopping - releasing all keys...")
                try:
                    keys.lmb_up()  # Release mouse
                    keys.key_up('w')  # Release all possible keys
                    keys.key_up('a')
                    keys.key_up('s')
                    keys.key_up('d')
                except:
                    pass
            
            current_pattern = None
            initial_delay_done = False
            paths_executed = False
            time.sleep(0.2)
    
    print("[MACRO] Thread stopped")

# --- Main Entry Point ---
ydotool_proc = StartYdotool()

if ydotool_proc:
    # IMPORTANT: Give ydotoold time to fully initialize
    print("Waiting for ydotoold to stabilize...")
    time.sleep(2)  # Wait 2 seconds before starting threads
    
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
        
        # Emergency cleanup - release all keys and mouse
        try:
            keys.lmb_up()
            keys.key_up('w')
            keys.key_up('a')
            keys.key_up('s')
            keys.key_up('d')
            print("Released all keys and mouse")
        except:
            pass
        
        ydotool_proc.terminate()
        print("Done.")
else:
    print("FATAL: ydotoold failed to start.")