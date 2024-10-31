import random
import math

class Herbivore:
    def __init__(self, pos, color, energy=100, eaten_plants=0, in_refuge=False, refuge_start_time=None):
        self.pos = pos
        self.color = color
        self.energy = energy
        self.eaten_plants = eaten_plants
        self.in_refuge = in_refuge
        self.refuge_start_time = refuge_start_time

    def move_towards(self, target, speed=1):
        dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.pos[0] += (dx / dist) * speed
            self.pos[1] += (dy / dist) * speed

    def is_alive(self):
        return self.energy > 0

    def update_energy(self, amount):
        self.energy += amount