import random
import math

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
        # Lógica para actualizar energía y movimiento de los herbívoros...