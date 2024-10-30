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
CARNIVORE_MAX_ENERGY = 150
REFUGE_RADIUS = 50
REFUGE_POSITION = (WIDTH - 100, HEIGHT // 2)
REFUGE_DURATION = 4000
CARNIVORE_RECHARGE_TIME = 3000
HUNTER_SHOOT_RANGE = 100
HUNTER_RELOAD_TIME = 2000
HUNTER_SPEED = 1.5


total_plants_consumed = 0
total_carnivores_hunted = 0
start_time = time.time()
end_time = None


plants = []
herbivores = []
carnivores = []
hunter = {"pos": [WIDTH // 2, HEIGHT // 2], "color": (0, 0, 255), "last_shot_time": None, "target": None}


for _ in range(NUM_PLANTS):
    plants.append({"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "color": (150, 150, 150)})
for _ in range(NUM_HERBIVORES):
    herbivores.append({"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "color": (0, 255, 0), 
                       "energy": HERBIVORE_MAX_ENERGY, "eaten_plants": 0, "in_refuge": False, "refuge_start_time": None})
for _ in range(NUM_CARNIVORES):
    carnivores.append({"pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)], "color": (255, 0, 0), 
                       "energy": CARNIVORE_MAX_ENERGY, "recharging": False, "recharge_start_time": None})

def move_towards(organism, target, speed=1):
    dx, dy = target[0] - organism["pos"][0], target[1] - organism["pos"][1]
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

def show_end_game_screen():
    global end_time
    end_time = time.time() - start_time
    font = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))

    
    texts = [
        f"Simulación terminada",
        f"Plantas consumidas: {total_plants_consumed}",
        f"Tiempo total: {int(end_time)} segundos",
        f"Carnívoros cazados por el cazador: {total_carnivores_hunted}",
        f"Herbívoros sobrevivientes: 0",
    ]
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100 + i * 30))

    # Botón de Salir
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 40)
    pygame.draw.rect(screen, (200, 0, 0), button_rect)
    button_text = font.render("Salir", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, 
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    pygame.display.flip()
    waiting_for_exit(button_rect)

def waiting_for_exit(button_rect):
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

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
        if herbivore["eaten_plants"] >= 2 and is_in_refuge(herbivore["pos"]):
            herbivore["in_refuge"] = True
            herbivore["refuge_start_time"] = pygame.time.get_ticks()
            herbivore["eaten_plants"] = 0
        closest_plant = min(plants, key=lambda p: math.hypot(herbivore["pos"][0] - p["pos"][0], herbivore["pos"][1] - p["pos"][1]), default=None)
        if closest_plant and math.hypot(herbivore["pos"][0] - closest_plant["pos"][0], herbivore["pos"][1] - closest_plant["pos"][1]) < 5:
            herbivore["energy"] += 20
            herbivore["eaten_plants"] += 1
            total_plants_consumed += 1
            plants.remove(closest_plant)
        if herbivore["energy"] <= 0:
            herbivores.remove(herbivore)
        else:
            pygame.draw.circle(screen, herbivore["color"], (int(herbivore["pos"][0]), int(herbivore["pos"][1])), 5)
            move_towards(herbivore, closest_plant["pos"] if closest_plant else herbivore["pos"])

    
    for carnivore in carnivores[:]:
        carnivore["energy"] -= 0.3
        closest_herbivore = min([h for h in herbivores if not is_in_refuge(h["pos"])], 
                                key=lambda h: math.hypot(carnivore["pos"][0] - h["pos"][0], carnivore["pos"][1] - h["pos"][1]), 
                                default=None)
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

    
    if not herbivores:
        show_end_game_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
