import cv2
import numpy as np
import subprocess
from pathlib import Path

class MultiBuffScanner:
    def __init__(self, buff_images_folder, region=None, threshold=0.5):
        self.buff_templates = {}
        self.threshold = threshold
        # ALWAYS define a small region for maximum speed!
        self.region = region if region else {'top': 0, 'left': 0, 'width': 400, 'height': 200}

        folder = Path(buff_images_folder)
        for img_path in folder.glob('*.png'):
            # Load as COLOR since we use color capture
            template = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
            if template is not None:
                self.buff_templates[img_path.stem] = template

    def Scan(self):
        # Format geometry: "x,y widthxheight"
        geom = f"{self.region['left']},{self.region['top']} {self.region['width']}x{self.region['height']}"
        
        try:
            # FASTEST WAY: Capture region only, output raw PPM to stdout
            result = subprocess.run(['grim', '-t', 'ppm', '-g', geom, '-'], 
                                   capture_output=True, check=True)
            
            # DECODE directly from stdout buffer (skipping BytesIO)
            image = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)
            
            if image is None: return []

            best_haste = None
            best_bear = None

            for name, template in self.buff_templates.items():
                # Matching on COLOR image is more accurate for icons
                res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)

                if max_val >= self.threshold:
                    det = {'name': name, 'confidence': max_val, 'position': max_loc}
                    
                    if 'haste' in name.lower():
                        if best_haste is None or max_val > best_haste['confidence']:
                            best_haste = det
                    elif 'bear_morph' in name.lower():
                        if best_bear is None or max_val > best_bear['confidence']:
                            best_bear = det

            final = []
            if best_haste: final.append(best_haste)
            if best_bear: final.append(best_bear)
            return final

        except Exception as e:
            print(f"Scan Error: {e}")
            return []