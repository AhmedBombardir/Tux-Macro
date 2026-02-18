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


class BugTimer:
    def __init__(self):
        self.timers = {}  # {'bug_name': {'start_time': timestamp, 'duration': seconds}}
    
    def start(self, bug_name, duration):
        """Start timer for specific bug"""
        self.timers[bug_name] = {
            'start_time': time.time(),
            'duration': duration
        }
    
    def is_ready(self, bug_name):
        """Check if bug timer expired (bug respawned)"""
        if bug_name not in self.timers:
            return True  # No timer = bug is ready
        
        timer = self.timers[bug_name]
        if timer['start_time'] is None:
            return True
        
        elapsed = time.time() - timer['start_time']
        return elapsed >= timer['duration']
    
    def reset(self, bug_name):
        """Reset specific bug timer"""
        if bug_name in self.timers:
            self.timers[bug_name]['start_time'] = None
    
    def reset_all(self):
        """Reset all bug timers"""
        self.timers.clear()
    
    def get_time_remaining(self, bug_name):
        """Get seconds until bug respawns (for UI/logging)"""
        if bug_name not in self.timers:
            return 0
        
        timer = self.timers[bug_name]
        if timer['start_time'] is None:
            return 0
        
        elapsed = time.time() - timer['start_time']
        remaining = timer['duration'] - elapsed
        return max(0, remaining)