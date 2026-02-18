import gui, patterns, threading, time, subprocess, os, settings, re, paths
from buff_detection import UltraFastBuffScanner
import timers

# Wayland socket configuration
socket_path = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = socket_path

# Shared state between threads
buff_state = {
    'current_buffs': {},
    'speed_multiplier': 1.0,
    'bear_morph_active': False,
    'lock': threading.Lock()
}

# Bug run state
bug_run_state = {
    'active': False,
    'current_bug': None,
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
    "Pepper": paths.Pepper,
}

# Bug kill paths mapping
bug_paths = {
    "werewolf": paths.Cannon_pumpkin,
    "mantis": paths.Cannon_pine,
    "scorpion": paths.Cannon_rose,
    "beetle": [paths.Cannon_clover, paths.Cannon_blueflower, paths.Cannon_bamboo, paths.Cannon_pineapple],
    "ladybug": [paths.Cannon_strawberry, paths.Cannon_mushroom, paths.Cannon_clover],
    "spider": paths.Cannon_spider,
}

gatherTimer = timers.GatherTimer()
bugTimer = timers.BugTimer()

region = {'x': 0, 'y': 0, 'width': 1920, 'height': 1080}
scanner = UltraFastBuffScanner(
    templates_folder='images',
    region=region,
    threshold=0.9,
    use_grayscale=False
)



def StartYdotool():
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
    print("[SCANNER] Thread started, loading templates...")
    
    region = {'x': 50, 'y': 0, 'width': 400, 'height': 200}
    
    scanner = UltraFastBuffScanner(
        templates_folder='images',
        region=region,
        threshold=0.95,
        use_grayscale=True
    )
    
    print("[SCANNER] Templates loaded, starting scan loop...")
    print(f"[SCANNER] Loaded templates: {list(scanner.templates.keys())}")

    frame_times = []
    scan_count = 0
    
    try:
        while gui.running:
            if gui.playing:
                try:  
                    scan_start = time.perf_counter()
                    
                    found_buffs = scanner.scan()
                    
                    best_buffs = {}
                    for buff_name, data in found_buffs.items():
                        buff_type = ''.join([c for c in buff_name if not c.isdigit()])
                        
                        if buff_type not in best_buffs or data['confidence'] > best_buffs[buff_type]['confidence']:
                            best_buffs[buff_type] = {
                                'name': buff_name,
                                'confidence': data['confidence'],
                                'position': data['position']
                            }
                    
                    # Check for bear morph first
                    bear_morph_active = False
                    for buff_type, data in best_buffs.items():
                        buff_name = data['name'].lower()
                        if 'bear_morph' in buff_name:
                            bear_morph_active = True
                            break
                    
                    # Calculate speed multiplier based on haste
                    speed_multiplier = 1.0
                    
                    for buff_type, data in best_buffs.items():
                        buff_name = data['name'].lower()
                        
                        if 'haste' in buff_name:
                            match = re.search(r'haste(\d+)', buff_name)
                            if match:
                                haste_level = int(match.group(1))
                                speed_multiplier = 1.0 + (haste_level * 0.1)
                            else:
                                speed_multiplier = 1.1
                            break
                        elif 'expedition' in buff_name:
                            speed_multiplier = 1.25
                            break
                    
                    # Update shared state with bear morph
                    with buff_state['lock']:
                        buff_state['current_buffs'] = best_buffs
                        buff_state['speed_multiplier'] = speed_multiplier
                        buff_state['bear_morph_active'] = bear_morph_active
                    
                    # Print buff info
                    if best_buffs:
                        output = " | ".join([f"{data['name']} ({data['confidence']:.0%})" 
                                           for data in best_buffs.values()])
                        morph_str = " + Bear Morph (+6 MS)" if bear_morph_active else ""
                        print(f"[SCAN] {output}{morph_str} → Speed: {speed_multiplier:.2f}x")
                    
                    scan_time = time.perf_counter() - scan_start
                    frame_times.append(scan_time)
                    scan_count += 1
                    
                    if len(frame_times) > 30:
                        frame_times.pop(0)
                    
                    if scan_count % 30 == 0:
                        avg_time = sum(frame_times) / len(frame_times)
                        avg_fps = 1.0 / avg_time if avg_time > 0 else 0
                        print(f"[SCANNER] FPS: {avg_fps:.1f} | Scan time: {avg_time*1000:.1f}ms")
                    
                    time.sleep(max(0.001, 0.1 - scan_time))
                
                except Exception as e:
                    print(f"[SCANNER] Error in scan loop: {e}")
                    import traceback
                    traceback.print_exc()
                    time.sleep(0.5)
            else:
                time.sleep(0.2)
    
    finally:
        scanner.cleanup()
        print("[SCANNER] Thread stopped")


def KillBug(bug_name):
    """Execute bug kill sequence"""
    print(f"[KILL] Starting {bug_name} kill sequence...")
    
    # CRITICAL: Stop all movement before bug run
    print(f"[KILL] Stopping all movement...")
    try:
        keys.lmb_up()
        keys.key_up('w')
        keys.key_up('a')
        keys.key_up('s')
        keys.key_up('d')
    except:
        pass
    
    time.sleep(0.5)  # Let keys release properly
    
    with bug_run_state['lock']:
        bug_run_state['active'] = True
        bug_run_state['current_bug'] = bug_name
    
    try:
        print(f"[KILL] Resetting position...")
        paths.Reset()
        time.sleep(1)
        paths.Reset_p2()
        time.sleep(2)
        print(f"[KILL] Cannon sequence...")
        paths.Cannon()
        time.sleep(0.5)
        
        
        bug_path = bug_paths.get(bug_name)
        
        if bug_path:
            if isinstance(bug_path, list):
                # Multiple locations (beetle, ladybug)
                print(f"[KILL] {bug_name} has {len(bug_path)} locations")
                for idx, path_func in enumerate(bug_path, 1):
                    print(f"[KILL] Location {idx}/{len(bug_path)}...")
                    path_func()
                    time.sleep(0.5)
                    if idx < len(bug_path):  # Don't reset after last one
                        paths.Reset()
                        time.sleep(1)
                        paths.Reset_p2()
                        time.sleep(2)
                        paths.Cannon()
                        time.sleep(0.5)
            else:
                # Single location
                print(f"[KILL] Executing {bug_name} path...")
                bug_path()
                time.sleep(0.5)
            
            print(f"[KILL] Final reset...")
            paths.Reset()
            time.sleep(1)
            print(f"[KILL] {bug_name} kill sequence completed!")
        else:
            print(f"[KILL] ERROR: No path found for {bug_name}")
    
    except Exception as e:
        print(f"[KILL] ERROR during {bug_name} kill: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Release all keys again just to be safe
        try:
            keys.lmb_up()
            keys.key_up('w')
            keys.key_up('a')
            keys.key_up('s')
            keys.key_up('d')
        except:
            pass
        
        with bug_run_state['lock']:
            bug_run_state['active'] = False
            bug_run_state['current_bug'] = None


def TimerThread():
    """Monitor bug timers and trigger kills"""
    print("[TIMER] Thread started")
    
    gatherTimer.start()

    # Check if bugs should be ready immediately or need to wait
    bugs_ready_on_start = getattr(settings, 'bugs_ready_on_start', False)
    
    # Get respawn times from settings
    bug_times = getattr(settings, 'bug_respawn_times', {
        "ladybug": 120,
        "beetle": 120,
        "werewolf": 3600,
        "mantis": 1200,
        "scorpion": 1200,
        "spider": 1800,
    })
    
    if bugs_ready_on_start:
        # Bugs are ready immediately - set timers as already expired
        print("[TIMER] Bugs are READY on start - initial clear will happen in MacroLoop")
        
        # Initialize timers but with start_time set to way in the past so is_ready() returns True
        for bug_name, duration in bug_times.items():
            bugTimer.timers[bug_name] = {
                'start_time': time.time() - (duration + 1),  # Already expired
                'duration': duration
            }
    else:
        # Initialize bug timers - start with full duration (NOT ready immediately)
        print("[TIMER] Bug timers initialized - bugs will be ready after their respawn times:")
        print(f"  - Ladybug & Beetle: 2 minutes")
        print(f"  - Mantis & Scorpion: 20 minutes")
        print(f"  - Spider: 30 minutes")
        print(f"  - Werewolf: 1 hour")
        
        for bug_name, duration in bug_times.items():
            bugTimer.start(bug_name, duration)

    while gui.running:
        time.sleep(1)
        
        if not gui.playing:
            continue
        
        # Check if currently in bug run
        with bug_run_state['lock']:
            in_bug_run = bug_run_state['active']
        
        if in_bug_run:
            continue
        
        # Check gather interrupt setting
        gather_interrupt = getattr(settings, 'gather_interrupt', True)
        
        # Check if we're currently gathering
        is_gathering = not gatherTimer.is_expired()
        
        # If gather interrupt is OFF and we're gathering, skip bug checks
        if not gather_interrupt and is_gathering:
            continue
        
        # Check each bug timer
        bugs_to_kill = []
        
        if bugTimer.is_ready("werewolf"):
            bugs_to_kill.append("werewolf")
        
        if bugTimer.is_ready("mantis"):
            bugs_to_kill.append("mantis")
        
        if bugTimer.is_ready("scorpion"):
            bugs_to_kill.append("scorpion")
        
        if bugTimer.is_ready("beetle"):
            bugs_to_kill.append("beetle")
        
        if bugTimer.is_ready("ladybug"):
            bugs_to_kill.append("ladybug")
        
        if bugTimer.is_ready("spider"):
            bugs_to_kill.append("spider")
        
        # Execute kills for ready bugs
        for bug_name in bugs_to_kill:
            if not gui.playing:
                break
            
            print(f"[TIMER] {bug_name.upper()} is ready!")
            
            # If gather interrupt is ON, interrupt gathering
            if gather_interrupt and is_gathering:
                print("[TIMER] Interrupting gather for bug run...")
            
            KillBug(bug_name)
            
            # Reset the bug timer
            bugTimer.start(bug_name, bugTimer.timers[bug_name]['duration'])
    
    print("[TIMER] Thread stopped")


def MacroLoop():
    pattern_functions = {
        "CornerXSnake": patterns.CornerXSnake,
        "E_lol": patterns.E_lol,
        "Stationary": patterns.Stationary
    }
    
    current_pattern = None
    paths_executed = False
    initial_bug_clear_done = False  # NEW: Track if we did initial bug clear
    
    print("[MACRO] Thread started")
    
    print("[MACRO] Waiting for ydotoold to stabilize...")
    time.sleep(2)
    print("[MACRO] Ready!")
    
    while gui.running:
        if gui.playing:
            # Check if bug run is active
            with bug_run_state['lock']:
                in_bug_run = bug_run_state['active']
            
            if in_bug_run:
                # Pause macro during bug runs
                current_pattern = None
                paths_executed = False
                time.sleep(0.1)
                continue
            
            # NEW: Check if we need to do initial bug clear
            if not initial_bug_clear_done:
                bugs_ready_on_start = getattr(settings, 'bugs_ready_on_start', False)
                
                if bugs_ready_on_start:
                    print("[MACRO] bugs_ready_on_start = True, clearing all bugs before first gather...")
                    time.sleep(2)
                    
                    # Kill all bugs that are marked as ready
                    bugs_to_clear = ["ladybug", "beetle", "spider", "werewolf", "mantis", "scorpion"]
                    
                    for bug_name in bugs_to_clear:
                        if not gui.playing:
                            break
                        
                        print(f"[MACRO] Initial clear: {bug_name.upper()}")
                        KillBug(bug_name)
                        
                        # Restart timer after killing (timers already exist from TimerThread)
                        if bug_name in bugTimer.timers:
                            bugTimer.start(bug_name, bugTimer.timers[bug_name]['duration'])
                    
                    print("[MACRO] Initial bug clear complete! Starting normal macro...")
                
                initial_bug_clear_done = True
            
            if current_pattern is None and not paths_executed:
                time.sleep(5)

                # Check for hive
                found = False
                confidence = 0.0
                pos = None

                for template in ['hive_respawn_day', 'hive_respawn_night']:
                    found, confidence, pos = scanner.check_image(template, 0.9)
                    
                    print(f"[DEBUG] Checking {template}: found={found}, confidence={confidence:.2%}")
                    
                    if found:
                        print(f"Hive found ({template}) at {pos} with {confidence:.0%} confidence")
                        break

                paths.Reset_p2()

                if found:
                    paths.Cannon()
                else:
                    print("Hive not found, resetting...")
                    paths.Reset()
                    continue

                # Execute field path
                selected_field = settings.field
                field_func = field_paths.get(selected_field)

                if field_func:
                    print(f"[MACRO] Executing: {selected_field} path")
                    field_func()
                else:
                    print(f"[ERROR] No path found for field: {selected_field}")

                paths_executed = True

                # Sprinkler logic
                if settings.sprinkler == "Basic" or settings.sprinkler == "Supreme":
                    keys.press('1')
                elif settings.sprinkler == "Silver":
                    keys.press('1')
                    keys.hold('a', 0.5)
                    keys.hold('w', 0.5)
                    keys.press('space')
                    time.sleep(0.5)
                    keys.press('1')
                    time.sleep(1)
                    keys.hold('d', 0.5)
                    keys.hold('s', 0.5)
                elif settings.sprinkler == "Golden":
                    keys.press('1')
                    keys.hold('a', 0.5)
                    keys.hold('w', 0.5)
                    keys.press('space')
                    time.sleep(0.5)
                    keys.press('1')
                    time.sleep(1)
                    keys.hold('d', 0.5)
                    keys.press('space')
                    time.sleep(0.5)
                    keys.press('1')
                    time.sleep(1)
                    keys.hold('s', 0.5)
                elif settings.sprinkler == "Diamond":
                    keys.press('1')
                    keys.hold('a', 0.5)
                    keys.hold('w', 0.5)
                    keys.press('space')
                    time.sleep(0.5)
                    keys.press('1')
                    time.sleep(1)
                    keys.hold('d', 0.5)
                    keys.press('space')
                    time.sleep(0.5)
                    keys.press('1')
                    time.sleep(1)
                    keys.hold('s', 0.5)
                    keys.hold('a', 0.5)
                    keys.press('space')
                    time.sleep(0.5)
                    keys.press('1')
                    time.sleep(1)
                    keys.hold('d', 0.5)

                gatherTimer.start()

            elif current_pattern is None and paths_executed:
                current_pattern = settings.pattern
                pattern_func = pattern_functions.get(current_pattern, patterns.CornerXSnake)
                print(f"--- MACRO STARTED ({current_pattern}) ---")

            if gatherTimer.is_expired():
                print("[MACRO] Gather time finished!")
                paths_executed = False
                current_pattern = None
                gatherTimer.reset()
                paths.Reset()
                continue

            # Only execute pattern if we have one AND not in bug run
            if current_pattern is not None:
                with bug_run_state['lock']:
                    in_bug_run = bug_run_state['active']
                
                if not in_bug_run:
                    with buff_state['lock']:
                        speed_mult = buff_state['speed_multiplier']
                        active_buffs = list(buff_state['current_buffs'].keys())
                    
                    if speed_mult > 1.0 and active_buffs:
                        print(f"[MACRO] Speed boost active: {speed_mult:.1f}x (Buffs: {active_buffs})")
                    
                    try:
                        pattern_func()
                    except Exception as e:
                        if gui.playing:
                            print(f"Movement Warning: {e}")
                        try:
                            keys.lmb_up()
                        except:
                            pass
            
            time.sleep(0.01)
        else:
            if current_pattern is not None or paths_executed:
                print("[MACRO] Stopping - releasing all keys...")
                try:
                    keys.lmb_up()
                    keys.key_up('w')
                    keys.key_up('a')
                    keys.key_up('s')
                    keys.key_up('d')
                except:
                    pass
            
            current_pattern = None
            paths_executed = False
            initial_bug_clear_done = False  # Reset on stop
            gatherTimer.reset()
            time.sleep(0.2)
    
    print("[MACRO] Thread stopped")

# --- Main Entry Point ---
ydotool_proc = StartYdotool()

if ydotool_proc:
    print("Waiting for ydotoold to stabilize...")
    time.sleep(2)
    
    scanner_thread = threading.Thread(target=BuffScannerThread, daemon=True)
    macro_thread = threading.Thread(target=MacroLoop, daemon=True)
    timer_thread = threading.Thread(target=TimerThread, daemon=True)
    
    scanner_thread.start()
    macro_thread.start()
    timer_thread.start()
    
    try:
        while gui.running:
            gui.Render()
            time.sleep(0.01)
    except KeyboardInterrupt:
        gui.running = False
    finally:
        print("Cleaning up...")
        gui.playing = False
        time.sleep(0.3)
        
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