import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema con Cazador y Divisiones")

NUM_PLANTS = 50
NUM_HERBIVORE_TYPE1 = 7
NUM_HERBIVORE_TYPE2 = 7
NUM_HERBIVORE_TYPE3 = 6
NUM_CARNIVORES_RED = 8
NUM_CARNIVORES_ORANGE = 4
HERBIVORE_MAX_ENERGY = 100
CARNIVORE_MAX_ENERGY = 150
REFUGE_RADIUS = 50
REFUGE_DURATION = 4000
CARNIVORE_RECHARGE_TIME = 3000
HUNTER_SHOOT_RANGE = 100
HUNTER_RELOAD_TIME = 2000
HUNTER_SPEED = 1.1

# Refugios para cada sección
REFUGE_POSITIONS = [(WIDTH // 6, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2), (5 * WIDTH // 6, HEIGHT // 2)]
HERBIVORE_COLORS = [(0, 255, 0), (34, 139, 34), (0, 128, 0)]
CARNIVORE_RED_COLOR = (255, 0, 0)
CARNIVORE_ORANGE_COLOR = (255, 140, 0)
HUNTER_COLOR = (0, 0, 255)

plants = [{"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "color": (150, 150, 150)} for _ in range(NUM_PLANTS)]
herbivores = []
carnivores = []

# Creación de herbívoros y carnívoros en distintas secciones
def create_herbivores(num, color, section_idx):
    x_start = (section_idx * WIDTH) // 3
    x_end = ((section_idx + 1) * WIDTH) // 3
    for _ in range(num):
        x, y = random.randint(x_start, x_end), random.randint(0, HEIGHT)
        herbivores.append({"pos": [x, y], "color": color, "energy": HERBIVORE_MAX_ENERGY, "eaten_plants": 0,
                           "in_refuge": False, "refuge_start_time": None, "section": section_idx})

create_herbivores(NUM_HERBIVORE_TYPE1, HERBIVORE_COLORS[0], 0)
create_herbivores(NUM_HERBIVORE_TYPE2, HERBIVORE_COLORS[1], 1)
create_herbivores(NUM_HERBIVORE_TYPE3, HERBIVORE_COLORS[2], 2)

for _ in range(NUM_CARNIVORES_RED):
    carnivores.append({"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "color": CARNIVORE_RED_COLOR,
                       "energy": CARNIVORE_MAX_ENERGY, "recharging": False, "recharge_start_time": None, "type": "red"})
for _ in range(NUM_CARNIVORES_ORANGE):
    carnivores.append({"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "color": CARNIVORE_ORANGE_COLOR,
                       "energy": CARNIVORE_MAX_ENERGY, "recharging": False, "recharge_start_time": None, "type": "orange"})

hunter = {"pos": [WIDTH // 2, HEIGHT // 2], "color": HUNTER_COLOR, "last_shot_time": None, "target": None}

def move_towards(organism, target, speed=1):
    dx, dy = target[0] - organism["pos"][0], target[1] - organism["pos"][1]
    dist = math.hypot(dx, dy)
    if dist != 0:
        organism["pos"][0] += (dx / dist) * speed
        organism["pos"][1] += (dy / dist) * speed

def is_in_refuge(pos, section):
    return math.hypot(pos[0] - REFUGE_POSITIONS[section][0], pos[1] - REFUGE_POSITIONS[section][1]) < REFUGE_RADIUS

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (100, 100, 100), (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 1)
    pygame.draw.line(screen, (100, 100, 100), (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 1)
    for pos in REFUGE_POSITIONS:
        pygame.draw.circle(screen, (0, 0, 255), pos, REFUGE_RADIUS, 1)

    for plant in plants:
        pygame.draw.circle(screen, plant["color"], (int(plant["pos"][0]), int(plant["pos"][1])), 3)

    for herbivore in herbivores[:]:
        herbivore["energy"] -= 0.1
        if herbivore["energy"] <= 0:
            herbivores.remove(herbivore)
            continue
        if herbivore["in_refuge"]:
            if pygame.time.get_ticks() - herbivore["refuge_start_time"] > REFUGE_DURATION:
                herbivore["in_refuge"] = False
            else:
                herbivore["energy"] = HERBIVORE_MAX_ENERGY
                continue
        if herbivore["eaten_plants"] >= 2:
            if is_in_refuge(herbivore["pos"], herbivore["section"]):
                herbivore["in_refuge"] = True
                herbivore["refuge_start_time"] = pygame.time.get_ticks()
                herbivore["eaten_plants"] = 0
            else:
                move_towards(herbivore, REFUGE_POSITIONS[herbivore["section"]])
            continue
        closest_plant = min(plants, key=lambda p: math.hypot(herbivore["pos"][0] - p["pos"][0], herbivore["pos"][1] - p["pos"][1]), default=None)
        if closest_plant and math.hypot(herbivore["pos"][0] - closest_plant["pos"][0], herbivore["pos"][1] - closest_plant["pos"][1]) < 5:
            herbivore["energy"] += 20
            herbivore["eaten_plants"] += 1
            plants.remove(closest_plant)
        else:
            move_towards(herbivore, closest_plant["pos"] if closest_plant else herbivore["pos"])
        pygame.draw.circle(screen, herbivore["color"], (int(herbivore["pos"][0]), int(herbivore["pos"][1])), 5)

    # Carnivores y cazador
    for carnivore in carnivores[:]:
        if carnivore["recharging"]:
            if pygame.time.get_ticks() - carnivore["recharge_start_time"] >= CARNIVORE_RECHARGE_TIME:
                carnivore["energy"] = CARNIVORE_MAX_ENERGY
                carnivore["recharging"] = False
            pygame.draw.circle(screen, carnivore["color"], (int(carnivore["pos"][0]), int(carnivore["pos"][1])), 6)
            continue

        carnivore["energy"] -= 0.3

        closest_herbivore = min(
            [h for h in herbivores if not is_in_refuge(h["pos"], h["section"])],
            key=lambda h: math.hypot(carnivore["pos"][0] - h["pos"][0], carnivore["pos"][1] - h["pos"][1]),
            default=None
        )
        if closest_herbivore and math.hypot(carnivore["pos"][0] - closest_herbivore["pos"][0], carnivore["pos"][1] - closest_herbivore["pos"][1]) < 10:
            carnivore["energy"] += 40
            herbivores.remove(closest_herbivore)
            if carnivore["energy"] > CARNIVORE_MAX_ENERGY:
                carnivore["recharging"] = True
                carnivore["recharge_start_time"] = pygame.time.get_ticks()

        if carnivore["energy"] <= 0:
            carnivores.remove(carnivore)
        else:
            pygame.draw.circle(screen, carnivore["color"], (int(carnivore["pos"][0]), int(carnivore["pos"][1])), 6)
            if carnivore["type"] == "orange" and closest_herbivore:
                nearest_red_carnivore = min(
                    [c for c in carnivores if c["type"] == "red"],
                    key=lambda c: math.hypot(c["pos"][0] - carnivore["pos"][0], c["pos"][1] - carnivore["pos"][1]),
                    default=None
                )
                if nearest_red_carnivore and math.hypot(nearest_red_carnivore["pos"][0] - carnivore["pos"][0], nearest_red_carnivore["pos"][1] - carnivore["pos"][1]) < 50:
                    continue
                # En caso de no haber un carnívoro rojo cerca, los carnívoros naranjas se acercan al herbívoro más cercano
                move_towards(carnivore, closest_herbivore["pos"])
            elif carnivore["type"] == "red" and closest_herbivore:
                move_towards(carnivore, closest_herbivore["pos"])

    # Dibujar el cazador y permitirle disparar si el objetivo está a rango
    if hunter["target"] and math.hypot(hunter["target"]["pos"][0] - hunter["pos"][0], hunter["target"]["pos"][1] - hunter["pos"][1]) < HUNTER_SHOOT_RANGE:
        hunter["target"]["energy"] -= 50  # Disparar reduce la energía del objetivo
        if hunter["target"]["energy"] <= 0:
            carnivores.remove(hunter["target"])  # Elimina el carnívoro si su energía es cero
        hunter["target"] = None  # Restablece el objetivo tras el disparo
        hunter["last_shot_time"] = pygame.time.get_ticks()
    else:
        # Buscar el carnívoro más cercano si el cazador no tiene un objetivo o si el objetivo se aleja demasiado
        nearest_carnivore = min(carnivores, key=lambda c: math.hypot(hunter["pos"][0] - c["pos"][0], hunter["pos"][1] - c["pos"][1]), default=None)
        if nearest_carnivore and math.hypot(hunter["pos"][0] - nearest_carnivore["pos"][0], hunter["pos"][1] - nearest_carnivore["pos"][1]) < HUNTER_SHOOT_RANGE:
            hunter["target"] = nearest_carnivore
        elif nearest_carnivore:
            # Moverse hacia el carnívoro más cercano si está fuera de rango
            move_towards(hunter, nearest_carnivore["pos"], HUNTER_SPEED)

    pygame.draw.circle(screen, hunter["color"], (int(hunter["pos"][0]), int(hunter["pos"][1])), 8)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
