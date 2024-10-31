import math

class Refuge:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def is_in_refuge(self, pos):
        return math.hypot(pos[0] - self.position[0], pos[1] - self.position[1]) < self.radius