import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema")

NUM_PLANTS = 50
NUM_HERBIVORES = 20
NUM_CARNIVORES = 10

plants = []
herbivores = []
carnivores = []


for _ in range(NUM_PLANTS):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    plants.append({"pos": [x, y], "color": (150, 150, 150)})


for _ in range(NUM_HERBIVORES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    herbivores.append({"pos": [x, y], "color": (0, 255, 0), "energy": 100})


for _ in range(NUM_CARNIVORES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    carnivores.append({"pos": [x, y], "color": (255, 0, 0), "energy": 150})


def move_towards(organism, target):
    dx, dy = target[0] - organism["pos"][0], target[1] - organism["pos"][1]
    dist = math.hypot(dx, dy)
    if dist != 0:
        organism["pos"][0] += (dx / dist) * 1
        organism["pos"][1] += (dy / dist) * 1


running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    
    for plant in plants:
        pygame.draw.circle(screen, plant["color"], (int(plant["pos"][0]), int(plant["pos"][1])), 3)

    
    for herbivore in herbivores[:]:
        herbivore["energy"] -= 0.1  

        
        closest_plant = min(plants, key=lambda p: math.hypot(herbivore["pos"][0] - p["pos"][0], herbivore["pos"][1] - p["pos"][1]), default=None)
        if closest_plant and math.hypot(herbivore["pos"][0] - closest_plant["pos"][0], herbivore["pos"][1] - closest_plant["pos"][1]) < 5:
            herbivore["energy"] += 20  
            plants.remove(closest_plant)  

        if herbivore["energy"] <= 0:  
            herbivores.remove(herbivore)
        else:
            pygame.draw.circle(screen, herbivore["color"], (int(herbivore["pos"][0]), int(herbivore["pos"][1])), 5)
            move_towards(herbivore, closest_plant["pos"] if closest_plant else herbivore["pos"])

    
    for carnivore in carnivores[:]:
        carnivore["energy"] -= 0.2  

        
        closest_herbivore = min(herbivores, key=lambda h: math.hypot(carnivore["pos"][0] - h["pos"][0], carnivore["pos"][1] - h["pos"][1]), default=None)
        if closest_herbivore and math.hypot(carnivore["pos"][0] - closest_herbivore["pos"][0], carnivore["pos"][1] - closest_herbivore["pos"][1]) < 5:
            carnivore["energy"] += 40  
            herbivores.remove(closest_herbivore)  

        if carnivore["energy"] <= 0:  
            carnivores.remove(carnivore)
        else:
            pygame.draw.circle(screen, carnivore["color"], (int(carnivore["pos"][0]), int(carnivore["pos"][1])), 6)
            move_towards(carnivore, closest_herbivore["pos"] if closest_herbivore else carnivore["pos"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
