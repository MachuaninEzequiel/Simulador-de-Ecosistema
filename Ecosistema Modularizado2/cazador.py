import math
import pygame

HUNTER_SHOOT_RANGE = 100  
HUNTER_RELOAD_TIME = 2000 

class Hunter:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.last_shot_time = None

    def move_towards(self, target, speed=1):
        dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.pos[0] += (dx / dist) * speed
            self.pos[1] += (dy / dist) * speed

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if (self.last_shot_time is None or current_time - self.last_shot_time >= HUNTER_RELOAD_TIME):
            return True  # Indicates a successful shot
        return False  # Indicates no shot was taken