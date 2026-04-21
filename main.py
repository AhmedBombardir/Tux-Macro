import threading
import time
import subprocess
import os
import re
import traceback

import gui
import keys
import paths
import patterns
import settings
import timers
from buff_detection import UltraFastBuffScanner


# ---------------------------------------------------------------------------
# Ydotool
# ---------------------------------------------------------------------------

SOCKET_PATH = "/run/user/1000/.ydotool_socket"
os.environ["YDOTOOL_SOCKET"] = SOCKET_PATH


def start_ydotool():
    print("[YDOTOOL] Restarting ydotoold...")
    subprocess.run(["pkill", "-f", "ydotoold"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)

    if os.path.exists(SOCKET_PATH):
        try:
            os.remove(SOCKET_PATH)
        except OSError:
            pass

    try:
        proc = subprocess.Popen(
            ["ydotoold", "--socket-path", SOCKET_PATH, "--socket-perm", "0666"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(25):
            if os.path.exists(SOCKET_PATH):
                print(f"[YDOTOOL] Ready at {SOCKET_PATH}")
                return proc
            time.sleep(0.2)

        print("[YDOTOOL] Timed out waiting for socket")
        return None
    except Exception as e:
        print(f"[YDOTOOL] Failed to start: {e}")
        return None


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

buff_state = {
    "current_buffs": {},
    "speed_multiplier": 1.0,
    "bear_morph_active": False,
    "lock": threading.Lock(),
}

bug_run_state = {
    "active": False,
    "current_bug": None,
    "lock": threading.Lock(),
}

collect_state = {
    "active": False,
    "lock": threading.Lock(),
}

keys.buff_state = buff_state


# ---------------------------------------------------------------------------
# Path mappings
# ---------------------------------------------------------------------------

FIELD_PATHS = {
    "Clover":       paths.Cannon_clover,
    "Mushroom":     paths.Cannon_mushroom,
    "Spider":       paths.Cannon_spider,
    "Bamboo":       paths.Cannon_bamboo,
    "Strawberry":   paths.Cannon_strawberry,
    "Blue Flower":  paths.Cannon_blueflower,
    "Pine Tree":    paths.Cannon_pine,
    "Pineapple":    paths.Cannon_pineapple,
    "Pumpkin":      paths.Cannon_pumpkin,
    "Cactus":       paths.Cannon_cactus,
    "Stump":        paths.Cannon_stump,
    "Rose":         paths.Cannon_rose,
    "Dandelion":    paths.Cannon_dandelion,
    "Sunflower":    paths.Cannon_sunflower,
    "Mountain":     paths.Cannon_mountain,
    "Pepper":       paths.Pepper,
}

BUG_PATHS = {
    "werewolf": paths.Cannon_pumpkin,
    "mantis":   paths.Cannon_pine,
    "scorpion": paths.Cannon_rose,
    "spider":   paths.Cannon_spider,
    "beetle":   [paths.Cannon_clover, paths.Cannon_blueflower, paths.Cannon_bamboo, paths.Cannon_pineapple],
    "ladybug":  [paths.Cannon_strawberry, paths.Cannon_mushroom, paths.Cannon_clover],
}


# ---------------------------------------------------------------------------
# Timers
# ---------------------------------------------------------------------------

gather_timer  = timers.Timer()
collect_timer = timers.Timer()
bug_timer     = timers.Timer()


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

scanner = UltraFastBuffScanner(
    templates_folder="images",
    region={"x": 0, "y": 0, "width": 1920, "height": 1080},
    threshold=0.9,
    use_grayscale=False,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def release_all_keys():
    try:
        keys.lmb_up()
        keys.key_up("w")
        keys.key_up("a")
        keys.key_up("s")
        keys.key_up("d")
    except Exception:
        pass


def goto_field():
    """Reset position and navigate to cannon."""
    time.sleep(1)
    paths.Reset()
    time.sleep(1)
    paths.Reset_p2()
    time.sleep(2)
    paths.Cannon()
    time.sleep(0.5)


def place_sprinkler():
    sp = settings.sprinkler
    keys.press("1")
    if sp == "Basic" or sp == "Supreme":
        return
    keys.hold("a", 0.5)
    keys.hold("w", 0.5)
    keys.press("space")
    time.sleep(0.5)
    keys.press("1")
    time.sleep(1)
    keys.hold("d", 0.5)
    if sp == "Silver":
        keys.hold("s", 0.5)
        return
    keys.press("space")
    time.sleep(0.5)
    keys.press("1")
    time.sleep(1)
    keys.hold("s", 0.5)
    if sp == "Golden":
        return
    keys.hold("a", 0.5)
    keys.press("space")
    time.sleep(0.5)
    keys.press("1")
    time.sleep(1)
    keys.hold("d", 0.5)


# ---------------------------------------------------------------------------
# Collect
# ---------------------------------------------------------------------------

def _collect(name):
    print(f"[COLLECT] Starting: {name}")
    release_all_keys()
    time.sleep(0.5)

    paths.Reset()
    time.sleep(1)
    paths.Reset_p2()
    time.sleep(2)
    paths.Cannon()
    time.sleep(0.5)

    collect_path = settings.collect_paths.get(name)
    if collect_path:
        collect_path()
        time.sleep(0.5)
        paths.Reset()
        time.sleep(1)
        paths.Reset_p2()
        time.sleep(2)
    else:
        print(f"[COLLECT] No path found for: {name}")

    print(f"[COLLECT] Done: {name}")

def do_collect(name):
    with collect_state["lock"]:
        collect_state["active"] = True

    time.sleep(1)


    try:
        _collect(name)
    except Exception as e:
        print(f"[COLLECT] Error during {name}: {e}")
        traceback.print_exc()
    finally:
        release_all_keys()
        with collect_state["lock"]:
            collect_state["active"] = False


# ---------------------------------------------------------------------------
# Bug kill
# ---------------------------------------------------------------------------

def _kill_bug(bug_name):
    print(f"[KILL] Starting: {bug_name}")
    release_all_keys()
    time.sleep(0.5)

    goto_field()

    bug_path = BUG_PATHS.get(bug_name)
    if not bug_path:
        print(f"[KILL] No path found for: {bug_name}")
        return

    path_list = bug_path if isinstance(bug_path, list) else [bug_path]

    for idx, path_func in enumerate(path_list, 1):
        print(f"[KILL] {bug_name} location {idx}/{len(path_list)}")
        path_func()
        time.sleep(0.5)
        if idx < len(path_list):
            goto_field()

    paths.Reset()
    time.sleep(1)
    print(f"[KILL] Done: {bug_name}")


def kill_bug(bug_name):
    with bug_run_state["lock"]:
        bug_run_state["active"] = True
        bug_run_state["current_bug"] = bug_name
    try:
        _kill_bug(bug_name)
    except Exception as e:
        print(f"[KILL] Error during {bug_name}: {e}")
        traceback.print_exc()
    finally:
        release_all_keys()
        with bug_run_state["lock"]:
            bug_run_state["active"] = False
            bug_run_state["current_bug"] = None


# ---------------------------------------------------------------------------
# Threads
# ---------------------------------------------------------------------------

def buff_scanner_thread():
    print("[SCANNER] Thread started")

    local_scanner = UltraFastBuffScanner(
        templates_folder="images",
        region={"x": 50, "y": 0, "width": 400, "height": 200},
        threshold=0.95,
        use_grayscale=True,
    )
    print(f"[SCANNER] Templates: {list(local_scanner.templates.keys())}")

    frame_times = []
    scan_count = 0

    try:
        while gui.running:
            if not gui.playing:
                time.sleep(0.2)
                continue

            try:
                t0 = time.perf_counter()
                found_buffs = local_scanner.scan()

                # Deduplicate buffs (keep highest confidence per type)
                best_buffs = {}
                for buff_name, data in found_buffs.items():
                    buff_type = "".join(c for c in buff_name if not c.isdigit())
                    if buff_type not in best_buffs or data["confidence"] > best_buffs[buff_type]["confidence"]:
                        best_buffs[buff_type] = {"name": buff_name, **data}

                bear_morph = any("bear_morph" in d["name"].lower() for d in best_buffs.values())
                speed_mult = 1.0

                for data in best_buffs.values():
                    name = data["name"].lower()
                    if "haste" in name:
                        m = re.search(r"haste(\d+)", name)
                        speed_mult = 1.0 + (int(m.group(1)) * 0.1) if m else 1.1
                        break
                    elif "expedition" in name:
                        speed_mult = 1.25
                        break

                with buff_state["lock"]:
                    buff_state["current_buffs"] = best_buffs
                    buff_state["speed_multiplier"] = speed_mult
                    buff_state["bear_morph_active"] = bear_morph

                if best_buffs:
                    buff_str = " | ".join(f"{d['name']} ({d['confidence']:.0%})" for d in best_buffs.values())
                    morph_str = " + Bear Morph" if bear_morph else ""
                    #print(f"[SCAN] {buff_str}{morph_str} → {speed_mult:.2f}x")

                elapsed = time.perf_counter() - t0
                frame_times.append(elapsed)
                scan_count += 1

                if len(frame_times) > 30:
                    frame_times.pop(0)
                if scan_count % 30 == 0:
                    avg = sum(frame_times) / len(frame_times)
                    #print(f"[SCANNER] {1/avg:.1f} FPS | {avg*1000:.1f}ms/scan")

                time.sleep(max(0.001, 0.1 - elapsed))

            except Exception as e:
                print(f"[SCANNER] Error: {e}")
                traceback.print_exc()
                time.sleep(0.5)
    finally:
        local_scanner.cleanup()
        print("[SCANNER] Thread stopped")


def timer_thread():
    print("[TIMER] Thread started")

    gather_timer.start("gather", settings.gatherTime)

    bug_times = getattr(settings, "bug_respawn_times", {
        "ladybug":  120,
        "beetle":   120,
        "werewolf": 3600,
        "mantis":   1200,
        "scorpion": 1200,
        "spider":   1800,
    })

    if getattr(settings, "bugs_ready_on_start", False):
        print("[TIMER] Bugs ready on start")
        for bug_name, duration in bug_times.items():
            bug_timer.start_ready(bug_name, duration)
    else:
        for bug_name, duration in bug_times.items():
            bug_timer.start(bug_name, duration)

    print("[TIMER] Waiting for macro to stabilize...")
    time.sleep(1)

    while gui.running:
        time.sleep(1)

        if not gui.playing:
            continue

        with bug_run_state["lock"]:
            in_bug_run = bug_run_state["active"]
        if in_bug_run:
            continue

        gather_interrupt = getattr(settings, "gather_interrupt", False)
        is_gathering = not gather_timer.is_ready("gather")

        if not gather_interrupt and is_gathering:
            continue

        # Bug kills
        if settings.bug_run_enabled:
            for bug_name in bug_times:
                if not gui.playing:
                    break
                if bug_timer.is_ready(bug_name):
                    print(f"[TIMER] {bug_name.upper()} ready")
                    kill_bug(bug_name)
                    bug_timer.start(bug_name, bug_times[bug_name])

        # Collects
        for name, (is_enabled, duration) in settings.collect_dict.items():
            if not is_enabled:
                continue
            if name not in collect_timer.timers:
                collect_timer.start_ready(name, duration)
            if collect_timer.is_ready(name):
                print(f"[TIMER] {name} ready, collecting...")
                do_collect(name)
                collect_timer.start(name, duration)

    print("[TIMER] Thread stopped")


def macro_loop():
    print("[MACRO] Thread started, waiting for ydotoold...")
    time.sleep(2)
    print("[MACRO] Ready")

    current_pattern = None
    paths_executed = False
    initial_bug_clear_done = False

    while gui.running:
        if not gui.playing:
            if current_pattern is not None or paths_executed:
                print("[MACRO] Stopped — releasing keys")
                release_all_keys()
            current_pattern = None
            paths_executed = False
            initial_bug_clear_done = False
            gather_timer.reset("gather")
            time.sleep(0.2)
            continue

        # Pause during bug run or collect
        with bug_run_state["lock"]:
            in_bug_run = bug_run_state["active"]
        with collect_state["lock"]:
            in_collect = collect_state["active"]

        if in_bug_run or in_collect:
            current_pattern = None
            paths_executed = False
            time.sleep(0.1)
            continue

        # Initial bug clear on start
        if not initial_bug_clear_done:
            initial_bug_clear_done = True
            if settings.bug_run_enabled and getattr(settings, "bugs_ready_on_start", False):
                print("[MACRO] Initial bug clear...")
                bug_times = getattr(settings, "bug_respawn_times", {})
                for bug_name in ["ladybug", "beetle", "spider", "werewolf", "mantis", "scorpion"]:
                    if not gui.playing:
                        break
                    kill_bug(bug_name)
                    if bug_name in bug_times:
                        bug_timer.start(bug_name, bug_times[bug_name])
                print("[MACRO] Initial bug clear done")

        # Gather timer expired
        if gather_timer.is_ready("gather") and paths_executed:
            print("[MACRO] Gather time finished")
            paths_executed = False
            current_pattern = None
            gather_timer.reset("gather")
            paths.Reset()
            continue




        # Navigate to field
        if current_pattern is None and not paths_executed:
            with collect_state["lock"]:
                if collect_state["active"]:
                    continue
            with bug_run_state["lock"]:
                if bug_run_state["active"]:
                    continue

            at_hive, conf1, _ = scanner.check_image("at_hive", 0.95)
            at_cannon, conf2, _ = scanner.check_image("E", 0.95)
            print(f"[MACRO] at_hive: {at_hive} ({conf1:.0%}) | E: {at_cannon} ({conf2:.0%})")

            if not at_hive and not at_cannon:
                print("[MACRO] Hive not found, resetting...")
                with collect_state["lock"]:
                    in_collect = collect_state["active"]
                with bug_run_state["lock"]:
                    in_bug = bug_run_state["active"]
                if not in_collect and not in_bug:
                    paths.Reset()
                    time.sleep(1)
                continue

            paths.Reset_p2()
            paths.Cannon()
            time.sleep(1)

            found, confidence, _ = scanner.check_image("E", 0.9)
            if not found:
                print("[MACRO] Cannon not found, resetting...")
                paths.Reset()
                continue

            field_func = FIELD_PATHS.get(settings.field)
            if field_func:
                print(f"[MACRO] Field: {settings.field}")
                field_func()
            else:
                print(f"[MACRO] Unknown field: {settings.field}")

            place_sprinkler()
            gather_timer.start("gather", settings.gatherTime)
            paths_executed = True

        # Start pattern
        elif current_pattern is None and paths_executed:
            current_pattern = settings.pattern
            pattern_func = getattr(patterns, current_pattern, patterns.CornerXSnake)
            print(f"[MACRO] Pattern: {current_pattern}")

        # Run pattern
        if current_pattern is not None:
            with buff_state["lock"]:
                speed_mult = buff_state["speed_multiplier"]
                active_buffs = list(buff_state["current_buffs"].keys())

            if speed_mult > 1.0:
                print(f"[MACRO] Speed {speed_mult:.1f}x ({active_buffs})")

            try:
                pattern_func()
            except Exception as e:
                if gui.playing:
                    print(f"[MACRO] Pattern error: {e}")
                release_all_keys()

        time.sleep(0.01)

    print("[MACRO] Thread stopped")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

ydotool_proc = start_ydotool()

if not ydotool_proc:
    print("[FATAL] ydotoold failed to start")
else:
    time.sleep(2)

    threads = [
        threading.Thread(target=buff_scanner_thread, daemon=True, name="Scanner"),
        threading.Thread(target=macro_loop,          daemon=True, name="Macro"),
        threading.Thread(target=timer_thread,        daemon=True, name="Timer"),
    ]
    for t in threads:
        t.start()

    try:
        while gui.running:
            gui.Render()
            time.sleep(0.01)
    except KeyboardInterrupt:
        gui.running = False
    finally:
        print("[MAIN] Shutting down...")
        gui.playing = False
        time.sleep(0.3)
        release_all_keys()
        ydotool_proc.terminate()
        print("[MAIN] Done")
