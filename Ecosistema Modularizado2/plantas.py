import random

class Plant:
    def __init__(self, pos):
        self.pos = pos
        self.color = (150, 150, 150)  # Default color for plants

    @staticmethod
    def create_random_plant(width, height):
        x = random.randint(0, width)
        y = random.randint(0, height)
        return Plant([x, y])