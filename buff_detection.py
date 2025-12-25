import cv2
import numpy as np
import subprocess
from pathlib import Path

class MultiBuffScanner:
    def __init__(self, buff_images_folder, region=None, threshold=0.8):
        """
        Optimized Wayland scanner (Arch Linux) using grim + PPM.
        """
        self.buff_templates = {}
        self.threshold = threshold

        # Load templates
        folder = Path(buff_images_folder)
        if not folder.exists():
            print(f"Error: Folder does not exist: {buff_images_folder}")
            return

        for img_path in folder.glob('*.png'):
            template = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if template is not None:
                buff_name = img_path.stem
                self.buff_templates[buff_name] = template
                print(f"✓ Loaded buff: {buff_name}")

        # Scan region (x, y, width, height)
        self.region = region if region else {
            'top': 0,
            'left': 0,
            'width': 1920,
            'height': 1080
        }

        print(f"Loaded {len(self.buff_templates)} buffs. Scanner ready (Wayland/Grim mode).")

    def Scan(self):
        """Capture screenshot using grim and detect buffs"""
        # Geometry format for grim: "x,y widthxheight"
        geometry = f"{self.region['left']},{self.region['top']} {self.region['width']}x{self.region['height']}"

        try:
            # -t ppm is much faster than png (no CPU compression)
            result = subprocess.run(
                ['grim', '-t', 'ppm', '-g', geometry, '-'],
                capture_output=True,
                check=True
            )

            # Decode image directly from RAM (stdout buffer)
            nparr = np.frombuffer(result.stdout, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                return []

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detected_buffs = []

            for buff_name, template in self.buff_templates.items():
                result_map = cv2.matchTemplate(
                    gray_image,
                    template,
                    cv2.TM_CCOEFF_NORMED
                )

                # Get best match only
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_map)

                if max_val >= self.threshold:
                    detected_buffs.append({
                        'name': buff_name,
                        'position': max_loc,
                        'confidence': max_val
                    })

            return detected_buffs

        except FileNotFoundError:
            print("Error: 'grim' is not installed! Install it with: sudo pacman -S grim")
            return []
        except Exception as e:
            print(f"Scan error: {e}")
            return []


def on_buffs_found(buffs):
    """Helper function to display detected buffs"""
    if not buffs:
        return

    print("\n[!] BUFFS DETECTED:")
    for buff in buffs:
        print(f"  • {buff['name']} ({buff['confidence']:.2%})")
