import time


class Timer:
    def __init__(self):
        self.timers = {}

    def start_ready(self, name, duration):
        """Start timer as already expired (ready immediately)"""
        self.timers[name] = {
            'start_time': time.time() - (duration + 1),
            'duration': duration
        }

    def start(self, name, duration):
        self.timers[name] = {
            'start_time': time.time(),
            'duration': duration
        }

    def is_ready(self, name):
        if name not in self.timers:
            return True
        timer = self.timers[name]
        if timer['start_time'] is None:
            return True
        return (time.time() - timer['start_time']) >= timer['duration']

    def reset(self, name):
        if name in self.timers:
            self.timers[name]['start_time'] = None

    def reset_all(self):
        self.timers.clear()

    def time_remaining(self, name):
        if name not in self.timers:
            return 0
        timer = self.timers[name]
        if timer['start_time'] is None:
            return 0
        return max(0, timer['duration'] - (time.time() - timer['start_time']))