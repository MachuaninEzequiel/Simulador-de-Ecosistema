import random

def initialize_plants(num_plants):
    plants = []
    for _ in range(num_plants):
        x = random.randint(0, 1024)
        y = random.randint(0, 768)
        plants.append({"pos": [x, y], "color": (150, 150, 150)})
    return plants