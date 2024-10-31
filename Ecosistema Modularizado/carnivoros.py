import pygame
import math

CARNIVORE_MAX_ENERGY = 150
CARNIVORE_RECHARGE_TIME = 3000

class Carnivore:
    def __init__(self, x, y, color, carnivore_type):
        self.pos = [x, y]
        self.color = color
        self.energy = CARNIVORE_MAX_ENERGY
        self.recharging = False
        self.recharge_start_time = None
        self.type = carnivore_type

    def move_towards(self, target, speed=1):
        dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.pos[0] += (dx / dist) * speed
            self.pos[1] += (dy / dist) * speed

    def attack_herbivore(self, herbivores):
        closest_herbivore = min(herbivores, key=lambda h: self.distance_to(h.pos), default=None)
        if closest_herbivore and self.distance_to(closest_herbivore.pos) < 5:
            self.energy += 40
            herbivores.remove(closest_herbivore)

    def distance_to(self, target):
        return math.hypot(self.pos[0] - target[0], self.pos[1] - target[1])

    def update(self, herbivores):
        if self.recharging:
            if pygame.time.get_ticks() - self.recharge_start_time >= CARNIVORE_RECHARGE_TIME:
                self.energy = CARNIVORE_MAX_ENERGY
                self.recharging = False
            return

        self.energy -= 0.3
        if self.energy <= 0:
            self.recharging = True
            self.recharge_start_time = pygame.time.get_ticks()
        else:
            self.attack_herbivore(herbivores)
