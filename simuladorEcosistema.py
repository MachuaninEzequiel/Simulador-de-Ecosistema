import pygame
import random
import math
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema con Cazador")

NUM_PLANTS = 50
NUM_HERBIVORES = 20
NUM_CARNIVORES = 10
HERBIVORE_MAX_ENERGY = 100
CARNIVORE_MAX_ENERGY = 100
REFUGE_RADIUS = 50
REFUGE_POSITION = (WIDTH - 100, HEIGHT // 2)
REFUGE_DURATION = 4000
CARNIVORE_RECHARGE_TIME = 3000
HUNTER_SHOOT_RANGE = 100
HUNTER_RELOAD_TIME = 2000

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
    herbivores.append({
        "pos": [x, y], 
        "color": (0, 255, 0), 
        "energy": HERBIVORE_MAX_ENERGY, 
        "eaten_plants": 0, 
        "in_refuge": False,
        "refuge_start_time": None
    })

for _ in range(NUM_CARNIVORES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    carnivores.append({
        "pos": [x, y], 
        "color": (255, 0, 0), 
        "energy": CARNIVORE_MAX_ENERGY,
        "recharging": False,
        "recharge_start_time": None
    })

hunter = {
    "pos": [WIDTH // 2, HEIGHT // 2],
    "color": (0, 0, 255),
    "last_shot_time": None
}

def move_towards(organism, target, speed=1):
    dx, dy = target[0] - organism["pos"][0], target[1] - organism["pos"][1]
    dist = math.hypot(dx, dy)
    if dist != 0:
        organism["pos"][0] += (dx / dist) * speed
        organism["pos"][1] += (dy / dist) * speed

def is_in_refuge(pos):
    return math.hypot(pos[0] - REFUGE_POSITION[0], pos[1] - REFUGE_POSITION[1]) < REFUGE_RADIUS

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (0, 0, 255), REFUGE_POSITION, REFUGE_RADIUS, 1)

    for plant in plants:
        pygame.draw.circle(screen, plant["color"], (int(plant["pos"][0]), int(plant["pos"][1])), 3)

    for herbivore in herbivores[:]:
        herbivore["energy"] -= 0.1

        if herbivore["in_refuge"]:
            if pygame.time.get_ticks() - herbivore["refuge_start_time"] > REFUGE_DURATION:
                herbivore["in_refuge"] = False
            else:
                herbivore["energy"] = HERBIVORE_MAX_ENERGY
                continue

        if herbivore["eaten_plants"] >= 2:
            if is_in_refuge(herbivore["pos"]):
                herbivore["in_refuge"] = True
                herbivore["refuge_start_time"] = pygame.time.get_ticks()
                herbivore["eaten_plants"] = 0
            else:
                move_towards(herbivore, REFUGE_POSITION)
                pygame.draw.circle(screen, herbivore["color"], (int(herbivore["pos"][0]), int(herbivore["pos"][1])), 5)
                continue

        closest_plant = min(plants, key=lambda p: math.hypot(herbivore["pos"][0] - p["pos"][0], herbivore["pos"][1] - p["pos"][1]), default=None)
        if closest_plant and math.hypot(herbivore["pos"][0] - closest_plant["pos"][0], herbivore["pos"][1] - closest_plant["pos"][1]) < 5:
            herbivore["energy"] += 20
            herbivore["eaten_plants"] += 1
            plants.remove(closest_plant)

        if herbivore["energy"] <= 0:
            herbivores.remove(herbivore)
        else:
            pygame.draw.circle(screen, herbivore["color"], (int(herbivore["pos"][0]), int(herbivore["pos"][1])), 5)
            move_towards(herbivore, closest_plant["pos"] if closest_plant else herbivore["pos"])

    for carnivore in carnivores[:]:
        if carnivore["recharging"]:
            if pygame.time.get_ticks() - carnivore["recharge_start_time"] >= CARNIVORE_RECHARGE_TIME:
                carnivore["energy"] = CARNIVORE_MAX_ENERGY
                carnivore["recharging"] = False
            pygame.draw.circle(screen, carnivore["color"], (int(carnivore["pos"][0]), int(carnivore["pos"][1])), 6)
            continue

        carnivore["energy"] -= 0.3

        closest_herbivore = min(
            [h for h in herbivores if not is_in_refuge(h["pos"])],
            key=lambda h: math.hypot(carnivore["pos"][0] - h["pos"][0], carnivore["pos"][1] - h["pos"][1]),
            default=None
        )
        if closest_herbivore and math.hypot(carnivore["pos"][0] - closest_herbivore["pos"][0], carnivore["pos"][1] - closest_herbivore["pos"][1]) < 5:
            carnivore["energy"] += 40
            herbivores.remove(closest_herbivore)

        if carnivore["energy"] <= 0:
            carnivore["recharging"] = True
            carnivore["recharge_start_time"] = pygame.time.get_ticks()
        else:
            pygame.draw.circle(screen, carnivore["color"], (int(carnivore["pos"][0]), int(carnivore["pos"][1])), 6)
            if closest_herbivore:
                move_towards(carnivore, closest_herbivore["pos"])

    if hunter["last_shot_time"] is None or pygame.time.get_ticks() - hunter["last_shot_time"] >= HUNTER_RELOAD_TIME:
        closest_carnivore = min(
            carnivores,
            key=lambda c: math.hypot(hunter["pos"][0] - c["pos"][0], hunter["pos"][1] - c["pos"][1]),
            default=None
        )
        if closest_carnivore and math.hypot(hunter["pos"][0] - closest_carnivore["pos"][0], hunter["pos"][1] - closest_carnivore["pos"][1]) <= HUNTER_SHOOT_RANGE:
            hunter["last_shot_time"] = pygame.time.get_ticks()
            carnivores.remove(closest_carnivore)

    pygame.draw.circle(screen, hunter["color"], (int(hunter["pos"][0]), int(hunter["pos"][1])), 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
