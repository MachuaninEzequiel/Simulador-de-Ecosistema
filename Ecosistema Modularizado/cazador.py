import pygame
import math
from herbivoros import Herbivore

HUNTER_SHOOT_RANGE = 100
HUNTER_RELOAD_TIME = 2000

class Hunter:
    def __init__(self, x, y, color=(0, 0, 255)):
        self.pos = [x, y]
        self.color = color
        self.last_shot_time = None
        self.target = None

    def distance_to(self, target):
        return math.hypot(self.pos[0] - target[0], self.pos[1] - target[1])

    def hunt(self, herbivores):
        if self.target and self.distance_to(self.target.pos) < HUNTER_SHOOT_RANGE:
            herbivores.remove(self.target)
