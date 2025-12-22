'''import threading
import time
import cv2 as cv
import subprocess
from pathlib import Path

class BuffMonitor:
    def __init__(self, base_speed=18, gear_bonus=10, calibrated_speed=28):
        """
        Monitor buffów używając gotowych template'ów
        
        Wymaga folderów:
        images/haste1.png, haste2.png, ..., haste10.png
        images/bear_morph.png
        """
        self.BASE_SPEED = base_speed
        self.GEAR_BONUS = gear_bonus
        self.CALIBRATED_SPEED = calibrated_speed
        
        # Stany buffów
        self.bear_morph_active = False
        self.haste_stacks = 0
        
        # Ścieżki do template'ów
        self.images_dir = Path('images')
        
        # Threading
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
    
    def _monitor_loop(self):
        """Monitoruj buffy w osobnym wątku"""
        while self.running:
            try:
                self._detect_buffs()
                time.sleep(0.3)  # Sprawdzaj co 300ms
            except Exception as e:
                print(f"Błąd monitora buffów: {e}")
                time.sleep(1)
    
    def _detect_buffs(self):
        """Wykryj aktywne buffy przez template matching"""
        # Screenshot obszaru buffów (dostosuj współrzędne!)
        subprocess.run(['grim', '-g', '1700,10,220,100', '/tmp/buffs.png'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        screenshot = cv.imread('/tmp/buffs.png')
        if screenshot is None:
            return
        
        # Wykryj Bear Morph
        self.bear_morph_active = self._check_template(
            screenshot, 
            'bear_morph1.png', 'bear_morph2.png', 'bear_morph3.png', 'bear_morph4.png', 'bear_morph5.png', 'bear_morph6.png',
            threshold=0.8
        )
        
        # Wykryj Haste (sprawdzaj od najwyższego do najniższego)
        self.haste_stacks = 0
        for stacks in range(10, 0, -1):
            if self._check_template(screenshot, f'haste{stacks}.png', threshold=0.85):
                self.haste_stacks = stacks
                break
    
    def _check_template(self, screenshot, template_name, threshold=0.8):
        """
        Sprawdź czy template występuje na screenshocie
        
        Args:
            screenshot: obraz ze screenshota
            template_name: nazwa pliku (np. 'haste5.png')
            threshold: próg dopasowania
        
        Returns:
            bool: True jeśli znaleziono
        """
        template_path = self.images_dir / template_name
        
        if not template_path.exists():
            return False
        
        template = cv.imread(str(template_path))
        if template is None:
            return False
        
        # Template matching
        result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(result)
        
        return max_val >= threshold
    
    def get_current_speed(self):
        """Oblicz aktualną prędkość gracza"""
        # Bazowa prędkość
        if self.bear_morph_active:
            base = 24  # Bear Morph base
        else:
            base = self.BASE_SPEED
        
        # Dodaj bonus z ekwipunku
        total_base = base + self.GEAR_BONUS
        
        # Zastosuj haste (multiplikatywny)
        haste_multiplier = 1.0 + (self.haste_stacks * 0.1)  # 10% per stack
        final_speed = total_base * haste_multiplier
        
        return final_speed
    
    def get_time_multiplier(self):
        """
        Oblicz współczynnik czasu dla aktualnych buffów
        
        Returns:
            float: Jak długo gracz powinien iść (względem calibrated speed)
        """
        current_speed = self.get_current_speed()
        return self.CALIBRATED_SPEED / current_speed
    
    def get_status(self):
        """Zwróć status buffów (do debugowania)"""
        speed = self.get_current_speed()
        multiplier = self.get_time_multiplier()
        
        buffs = []
        if self.bear_morph_active:
            buffs.append("Bear")
        if self.haste_stacks > 0:
            buffs.append(f"Haste x{self.haste_stacks}")
        
        buff_str = " + ".join(buffs) if buffs else "No buffs"
        
        return f"{buff_str} | Speed: {speed:.1f} | Time mult: {multiplier:.3f}x"
    
    def stop(self):
        self.running = False


# === UŻYCIE ===

# Inicjalizuj monitor (dostosuj do swoich wartości!)
buff_monitor = BuffMonitor(
    base_speed=18,
    gear_bonus=10,       # Zmień na swój bonus
    calibrated_speed=28  # Zmień na swoją normalną prędkość
)
'''