import settings
import time

class GatherTimer:
    def __init__(self):
        self.start_time = None
        self.duration = settings.gatherTime
    
    def start(self):
        self.start_time = time.time()
    
    def is_expired(self):
        if self.start_time is None:
            return False
        elapsed = time.time() - self.start_time
        return elapsed >= self.duration
    
    def reset(self):
        self.start_time = None