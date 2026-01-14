import cv2
import numpy as np
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


class UltraFastBuffScanner:
    """
    Optimized scanner - 3-5x faster than original.
    Optimizations:
    1. Grayscale matching (3x faster)
    2. Optional downscaling (2x faster)
    3. Early exit on first match (optional)
    """
    def __init__(self, templates_folder, region, threshold=0.75, 
                 use_grayscale=True, downscale=False, early_exit=False):
        self.region = region
        self.threshold = threshold
        self.capture = FastScreenCapture(region)
        self.use_grayscale = use_grayscale
        self.downscale = downscale
        self.early_exit = early_exit
        
        # Pre-load all templates into RAM
        self.templates = {}
        for img_path in Path(templates_folder).glob('*.png'):
            img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
            if img is not None:
                # Convert to grayscale if using grayscale matching
                if use_grayscale:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Optionally downscale templates
                if downscale:
                    img = cv2.resize(img, None, fx=0.5, fy=0.5, 
                                   interpolation=cv2.INTER_AREA)
                
                self.templates[img_path.stem] = img
        
        print(f"Loaded {len(self.templates)} templates into RAM")
        if use_grayscale:
            print("  - Using grayscale matching (~3x faster)")
        if downscale:
            print("  - Using 50% downscaling (~2x faster)")
    
    def scan(self):
        """Ultra-fast scan with optimizations"""
        screen = self.capture.capture()
        if screen is None:
            return {}
        
        # Convert to grayscale if needed
        if self.use_grayscale:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        # Optionally downscale
        if self.downscale:
            screen = cv2.resize(screen, None, fx=0.5, fy=0.5,
                              interpolation=cv2.INTER_AREA)
        
        results = {}
        for name, template in self.templates.items():
            res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= self.threshold:
                # Scale position back if downscaled
                if self.downscale:
                    max_loc = (max_loc[0] * 2, max_loc[1] * 2)
                
                results[name] = {
                    'confidence': float(max_val),
                    'position': max_loc
                }
                
                # Early exit if only need to know if ANY buff exists
                if self.early_exit:
                    break
        
        return results
    
    def cleanup(self):
        self.capture.cleanup()


class MultiScaleBuffScanner(UltraFastBuffScanner):
    """
    Advanced: handles different display scaling automatically.
    Use if buffs appear at different sizes on different monitors.
    """
    def __init__(self, templates_folder, region, threshold=0.75,
                 scales=[0.8, 0.9, 1.0, 1.1, 1.2]):
        self.scales = scales
        super().__init__(templates_folder, region, threshold, 
                        use_grayscale=True, downscale=False)
    
    def scan(self):
        """Scan at multiple scales"""
        screen = self.capture.capture()
        if screen is None:
            return {}
        
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        results = {}
        for name, template in self.templates.items():
            best_match = None
            
            # Try each scale
            for scale in self.scales:
                if scale != 1.0:
                    w = int(template.shape[1] * scale)
                    h = int(template.shape[0] * scale)
                    if w < 5 or h < 5:
                        continue
                    scaled_template = cv2.resize(template, (w, h))
                else:
                    scaled_template = template
                
                res = cv2.matchTemplate(screen, scaled_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                
                if max_val >= self.threshold:
                    if best_match is None or max_val > best_match['confidence']:
                        best_match = {
                            'confidence': float(max_val),
                            'position': max_loc,
                            'scale': scale
                        }
            
            if best_match:
                results[name] = best_match
        
        return results