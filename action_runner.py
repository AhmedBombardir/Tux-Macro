import pygame
import keys

class ActionRunner:

    def __init__(self):
        self.queue = []
        self.pattern = []
        self.current = None
        self.start_time = 0
        self.loop = False



    def start(self, actions, loop=False):
        self.pattern = actions.copy()
        self.queue = self.pattern.copy()
        self.current = None
        self.loop = loop



    def update(self):

        if not self.current and self.queue:
            self.current = self.queue.pop(0)
            self.start_time = pygame.time.get_ticks()
            self._start(self.current)

        if self.current and self._done(self.current):
            self._end(self.current)
            self.current = None
        
        if not self.current and not self.queue:
            if self.loop:
                self.queue = self.pattern.copy()

    def _start(self, action):
        t, key, _ = action
        if t == "down":
            keys.key_down(key)
        elif t == "up":
            keys.key_up(key)
        elif t == "hold":
            keys.key_down(key)
        elif t == "wait":
            pass  

    def _end(self, action):
        t, key, _ = action
        if t == "hold":
            keys.key_up(key)
        elif t == "wait":
            pass 

    def _done(self, action):
        t, _, dur = action
        if t in ("down", "up"):
            return True
        if t in ("hold", "wait"): 
            return pygame.time.get_ticks() - self.start_time >= dur * 1000
        return pygame.time.get_ticks() - self.start_time >= dur * 1000


    def stop(self):

        if self.current:
            t, key, _ = self.current
            if t in ("hold", "down"):
                keys.key_up(key)
        

        for action in self.queue:
            t, key, _ = action
            if t in ("hold", "down"):
                keys.key_up(key)
        

        for action in self.pattern:
            t, key, _ = action
            keys.key_up(key)
        

        self.current = None
        self.queue = []
        self.loop = False