import random
import math
import pygame

HERBIVORE_MAX_ENERGY = 100
REFUGE_DURATION = 4000

def initialize_herbivores(num_herbivores):
    herbivores = []
    for _ in range(num_herbivores // 2):
        x = random.randint(0, 1024)
        y = random.randint(0, 768)
        herbivores.append({
            "pos": [x, y],
            "color": (0, 255, 0),
            "energy": HERBIVORE_MAX_ENERGY,
            "eaten_plants": 0,
            "in_refuge": False,
            "refuge_start_time": None,
            "type": "herbivore_type_1"
        })
        
        x = random.randint(0, 1024)
        y = random.randint(0, 768)
        herbivores.append({
            "pos": [x, y],
            "color": (173, 255, 47),
            "energy": HERBIVORE_MAX_ENERGY,
            "eaten_plants": 0,
            "in_refuge": False,
            "refuge_start_time": None,
            "type": "herbivore_type_2"
        })
    
    return herbivores

def update_herbivores(herbivores, plants):
        for herbivore in herbivores[:]:
            # Disminuir energía
            herbivore["energy"] -= 0.1

            # Verificar si está en refugio
            if herbivore["in_refuge"]:
                if pygame.time.get_ticks() - herbivore["refuge_start_time"] > REFUGE_DURATION:
                    herbivore["in_refuge"] = False
                else:
                    herbivore["energy"] = HERBIVORE_MAX_ENERGY
                    continue

            # Lógica para entrar al refugio
            if herbivore["eaten_plants"] >= 2 and is_in_refuge(herbivore["pos"]):
                herbivore["in_refuge"] = True
                herbivore["refuge_start_time"] = pygame.time.get_ticks()
                herbivore["eaten_plants"] = 0
                continue

            # Buscar la planta más cercana
            closest_plant = min(plants, key=lambda p: math.hypot(herbivore["pos"][0] - p["pos"][0], 
                                                            herbivore["pos"][1] - p["pos"][1]), 
                                default=None)

            # Consumir planta si está cerca
            if closest_plant and math.hypot(herbivore["pos"][0] - closest_plant["pos"][0], 
                                        herbivore["pos"][1] - closest_plant["pos"][1]) < 5:
                herbivore["energy"] += 20
                herbivore["eaten_plants"] += 1
                plants.remove(closest_plant)

            # Verificar si la energía llega a cero
            if herbivore["energy"] <= 0:
                herbivores.remove(herbivore)
            else:
                move_towards(herbivore, closest_plant["pos"] if closest_plant else herbivore["pos"])
