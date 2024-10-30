import pygame
import random
import math
import time

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema con Cazador")

NUM_PLANTS = 50
NUM_HERBIVORES = 20
NUM_CARNIVORES = 10
HERBIVORE_MAX_ENERGY = 100
CARNIVORE_MAX_ENERGY = 150
REFUGE_RADIUS = 50
REFUGE_POSITION = (WIDTH - 100, HEIGHT // 2)
REFUGE_DURATION = 4000
CARNIVORE_RECHARGE_TIME = 3000
HUNTER_SHOOT_RANGE = 100
HUNTER_RELOAD_TIME = 2000
HUNTER_SPEED = 1.1

plants = []
herbivores = []
carnivores = []

# Plantas
for _ in range(NUM_PLANTS):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    plants.append({"pos": [x, y], "color": (150, 150, 150)})

# Herbívoros de dos tipos
for _ in range(NUM_HERBIVORES // 2):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    herbivores.append({
        "pos": [x, y],
        "color": (0, 255, 0), # Verde para el primer tipo
        "energy": HERBIVORE_MAX_ENERGY,
        "eaten_plants": 0,
        "in_refuge": False,
        "refuge_start_time": None,
        "type": "herbivore_type_1"
    })

for _ in range(NUM_HERBIVORES // 2):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    herbivores.append({
        "pos": [x, y],
        "color": (173, 255, 47), # Verde claro para el segundo tipo
        "energy": HERBIVORE_MAX_ENERGY,
        "eaten_plants": 0,
        "in_refuge": False,
        "refuge_start_time": None,
        "type": "herbivore_type_2"
    })

# Carnívoros de dos tipos
for _ in range(NUM_CARNIVORES // 2):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    carnivores.append({
        "pos": [x, y],
        "color": (255, 0, 0), # Rojo para el primer tipo
        "energy": CARNIVORE_MAX_ENERGY,
        "recharging": False,
        "recharge_start_time": None,
        "type": "carnivore_type_1"
    })

for _ in range(NUM_CARNIVORES // 2):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    carnivores.append({
        "pos": [x, y],
        "color": (255, 165, 0), # Naranja para el segundo tipo
        "energy": CARNIVORE_MAX_ENERGY,
        "recharging": False,
        "recharge_start_time": None,
        "type": "carnivore_type_2"
    })

hunter = {
    "pos": [WIDTH // 2, HEIGHT // 2],
    "color": (0, 0, 255),
    "last_shot_time": None,
    "target": None
}

def move_towards(organism, target, speed=1):
    dx, dy = target[0] - organism["pos"][0], target[1] - organism["pos"][1]
    dist = math.hypot(dx, dy)
    if dist != 0:
        organism["pos"][0] += (dx / dist) * speed
        organism["pos"][1] += (dy / dist) * speed

def move_away(organism, target, speed=1):
    dx, dy = organism["pos"][0] - target[0], organism["pos"][1] - target[1]
    dist = math.hypot(dx, dy)
    if dist != 0:
        organism["pos"][0] += (dx / dist) * speed
        organism["pos"][1] += (dy / dist) * speed

def is_in_refuge(pos):
    return math.hypot(pos[0] - REFUGE_POSITION[0], pos[1] - REFUGE_POSITION[1]) < REFUGE_RADIUS

def draw_dotted_line(screen, start_pos, end_pos, color, width=1, dot_length=5):
    distance = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    dots = int(distance // (dot_length * 2))
    for i in range(dots):
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * (i * dot_length * 2) / distance
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * (i * dot_length * 2) / distance
        pygame.draw.circle(screen, color, (int(x), int(y)), width)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 0, 255), REFUGE_POSITION, REFUGE_RADIUS, 1)

    # Plantas
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

    # Carnívoros
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

        for other_carnivore in carnivores:
            if carnivore["type"] != other_carnivore["type"]:
                dist = math.hypot(carnivore["pos"][0] - other_carnivore["pos"][0], carnivore["pos"][1] - other_carnivore["pos"][1])
                if dist < 20:
                    move_away(carnivore, other_carnivore["pos"], speed=1.2)
                    break

    hunter["target"] = None
    highest_threat_herbivore = None
    closest_threatening_carnivore = None

    for herbivore in herbivores:
        threatening_carnivore = min(
            carnivores,
            key=lambda c: math.hypot(herbivore["pos"][0] - c["pos"][0], herbivore["pos"][1] - c["pos"][1]),
            default=None
        )
        if threatening_carnivore and (
            highest_threat_herbivore is None or 
            math.hypot(threatening_carnivore["pos"][0] - herbivore["pos"][0], threatening_carnivore["pos"][1] - herbivore["pos"][1]) <
            math.hypot(closest_threatening_carnivore["pos"][0] - highest_threat_herbivore["pos"][0], closest_threatening_carnivore["pos"][1] - highest_threat_herbivore["pos"][1])
        ):
            highest_threat_herbivore = herbivore
            closest_threatening_carnivore = threatening_carnivore

    if highest_threat_herbivore and closest_threatening_carnivore:
        move_towards(hunter, highest_threat_herbivore["pos"], HUNTER_SPEED)

        if math.hypot(hunter["pos"][0] - closest_threatening_carnivore["pos"][0], hunter["pos"][1] - closest_threatening_carnivore["pos"][1]) <= HUNTER_SHOOT_RANGE:
            hunter["target"] = closest_threatening_carnivore
            if hunter["last_shot_time"] is None or pygame.time.get_ticks() - hunter["last_shot_time"] >= HUNTER_RELOAD_TIME:
                hunter["last_shot_time"] = pygame.time.get_ticks()
                carnivores.remove(closest_threatening_carnivore)

    pygame.draw.circle(screen, hunter["color"], (int(hunter["pos"][0]), int(hunter["pos"][1])), 8)

    if hunter["target"]:
        draw_dotted_line(screen, hunter["pos"], hunter["target"]["pos"], (255, 255, 255))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()