import random
import math

class Carnivore:
    def __init__(self, pos, color, energy=150):
        self.pos = pos
        self.color = color
        self.energy = energy
        self.recharging = False
        self.recharge_start_time = None

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