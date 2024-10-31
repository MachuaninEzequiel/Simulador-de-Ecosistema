import pygame
import random
import math
from refugio import is_in_refuge, REFUGE_POSITION, REFUGE_DURATION
from plantas import Plant

HERBIVORE_MAX_ENERGY = 100

class Herbivore:
    def __init__(self, x, y, color, herbivore_type):
        self.pos = [x, y]
        self.color = color
        self.energy = HERBIVORE_MAX_ENERGY
        self.eaten_plants = 0
        self.in_refuge = False
        self.refuge_start_time = None
        self.type = herbivore_type

    def move_towards(self, target, speed=1):
        dx, dy = target[0] - self.pos[0], target[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.pos[0] += (dx / dist) * speed
            self.pos[1] += (dy / dist) * speed

    def eat_plant(self, plant):
        if self.distance_to(plant.pos) < 5:
            self.energy += 20
            self.eaten_plants += 1
            return True
        return False

    def distance_to(self, target):
        return math.hypot(self.pos[0] - target[0], self.pos[1] - target[1])

    def update(self, plants, refuge_zone):
        self.energy -= 0.1
        if self.in_refuge:
            if pygame.time.get_ticks() - self.refuge_start_time > REFUGE_DURATION:
                self.in_refuge = False
            else:
                self.energy = HERBIVORE_MAX_ENERGY
                return

        if self.eaten_plants >= 2 and is_in_refuge(self.pos):
            self.in_refuge = True
            self.refuge_start_time = pygame.time.get_ticks()
            self.eaten_plants = 0
        else:
            closest_plant = min(plants, key=lambda p: self.distance_to(p.pos), default=None)
            if closest_plant and self.eat_plant(closest_plant):
                plants.remove(closest_plant)

        if self.energy <= 0:
            return False  
        return True  
