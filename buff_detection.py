import cv2
import numpy as np
import mmap
import subprocess
import time
from pathlib import Path

class FastScreenCapture:
    """
    Ultra-fast capture using shared memory.
    Uses /dev/shm (RAM disk) instead of stdout.
    """
    def __init__(self, region=None):
        self.region = region
        # File in RAM (not on disk!)
        self.shm_path = "/dev/shm/screenshot.ppm"
    
    def capture(self):
        """Capture screen to shared memory and load it"""
        if self.region:
            geom = f"{self.region['x']},{self.region['y']} {self.region['width']}x{self.region['height']}"
            subprocess.run(['grim', '-g', geom, '-t', 'ppm', self.shm_path], 
                         check=True, capture_output=True)
        else:
            subprocess.run(['grim', '-t', 'ppm', self.shm_path], 
                         check=True, capture_output=True)
        
        # Load from RAM (super fast)
        return cv2.imread(self.shm_path, cv2.IMREAD_COLOR)
    
    def cleanup(self):
        """Delete file from RAM"""
        Path(self.shm_path).unlink(missing_ok=True)


def find_image_fast(template_path, region=None, threshold=0.8, capture=None):
    """
    Fastest version - uses shared memory capture.
    
    Args:
        template_path: path to image file
        region: {'x', 'y', 'width', 'height'} or None
        threshold: 0.0-1.0
        capture: FastScreenCapture object (optional, for reuse)
    
    Returns:
        dict with results or None
    """
    # Use existing capture or create new one
    if capture is None:
        capture = FastScreenCapture(region)
    
    # Capture from RAM
    screen = capture.capture()
    
    # Load template (cache this outside function for max speed!)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    
    if screen is None or template is None:
        return None
    
    # Match
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= threshold:
        x, y = max_loc
        if region:
            x += region['x']
            y += region['y']
        
        return {
            'found': True,
            'confidence': float(max_val),
            'x': x, 'y': y
        }
    
    return {'found': False, 'confidence': float(max_val)}


class UltraFastBuffScanner:
    """
    Fastest possible implementation - everything in RAM + cache.
    """
    def __init__(self, templates_folder, region, threshold=0.75):
        self.region = region
        self.threshold = threshold
        self.capture = FastScreenCapture(region)
        
        # Pre-load all templates into RAM
        self.templates = {}
        for img_path in Path(templates_folder).glob('*.png'):
            img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
            if img is not None:
                self.templates[img_path.stem] = img
        
        print(f"Loaded {len(self.templates)} templates into RAM")
    
    def scan(self):
        """Ultra-fast scan - everything in RAM"""
        screen = self.capture.capture()
        if screen is None:
            return {}
        
        results = {}
        for name, template in self.templates.items():
            res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= self.threshold:
                results[name] = {
                    'confidence': float(max_val),
                    'position': max_loc
                }
        
        return results
    
    def cleanup(self):
        self.capture.cleanup()






# === BENCHMARK - comparison of methods ===
def benchmark():
    region = {'x': 0, 'y': 0, 'width': 400, 'height': 200}
    template = "buff.png"
    
    print("=== BENCHMARK ===\n")
    
    # Method 1: stdout (your current method)
    print("1. STDOUT Method (your current):")
    times = []
    for _ in range(10):
        start = time.perf_counter()
        result = subprocess.run(['grim', '-g', f"{region['x']},{region['y']} {region['width']}x{region['height']}", 
                                '-t', 'ppm', '-'], capture_output=True)
        screen = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg1 = sum(times) / len(times)
    print(f"   Average: {avg1*1000:.1f}ms, FPS: {1/avg1:.1f}\n")
    
    # Method 2: shared memory
    print("2. SHARED MEMORY Method (/dev/shm):")
    capture = FastScreenCapture(region)
    times = []
    for _ in range(10):
        start = time.perf_counter()
        screen = capture.capture()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg2 = sum(times) / len(times)
    print(f"   Average: {avg2*1000:.1f}ms, FPS: {1/avg2:.1f}\n")
    capture.cleanup()
    
    speedup = avg1 / avg2
    print(f" Shared memory is {speedup:.1f}x FASTER!")