import random
import pygame
import math

CARNIVORE_MAX_ENERGY = 150

def initialize_carnivores(num_carnivores):
    carnivores = []
    for _ in range(num_carnivores // 2):
        x = random.randint(0, 1024)
        y = random.randint(0, 768)
        carnivores.append({
            "pos": [x, y],
            "color": (255, 0, 0),
            "energy": CARNIVORE_MAX_ENERGY,
            "recharging": False,
            "recharge_start_time": None,
            "type": "carnivore_type_1"
        })
        
        x = random.randint(0, 1024)
        y = random.randint(0, 768)
        carnivores.append({
            "pos": [x, y],
            "color": (255, 165, 0),
            "energy": CARNIVORE_MAX_ENERGY,
            "recharging": False,
            "recharge_start_time": None,
            "type": "carnivore_type_2"
        })
    
    return carnivores

def update_carnivores(carnivores, herbivores):
    for carnivore in carnivores[:]:
        if carnivore["recharging"]:
            if pygame.time.get_ticks() - carnivore["recharge_start_time"] >= CARNIVORE_RECHARGE_TIME:
                carnivore["energy"] = CARNIVORE_MAX_ENERGY
                carnivore["recharging"] = False
            continue

        # Disminuir energía
        carnivore["energy"] -= 0.3

        # Buscar el herbívoro más cercano
        closest_herbivore = min(
            [h for h in herbivores if not is_in_refuge(h["pos"])],
            key=lambda h: math.hypot(carnivore["pos"][0] - h["pos"][0], carnivore["pos"][1] - h["pos"][1]),
            default=None
        )

        # Consumir el herbívoro si está cerca
        if closest_herbivore and math.hypot(carnivore["pos"][0] - closest_herbivore["pos"][0], 
                                            carnivore["pos"][1] - closest_herbivore["pos"][1]) < 5:
            carnivore["energy"] += 40
            herbivores.remove(closest_herbivore)

        # Verificar si la energía llega a cero
        if carnivore["energy"] <= 0:
            carnivore["recharging"] = True
            carnivore["recharge_start_time"] = pygame.time.get_ticks()
        else:
            if closest_herbivore:
                move_towards(carnivore, closest_herbivore["pos"])