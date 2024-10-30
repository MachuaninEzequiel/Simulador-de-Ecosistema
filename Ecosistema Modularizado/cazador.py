import math
import pygame

HUNTER_SPEED = 1.1

def initialize_hunter():
    return {
        "pos": [512, 384],
        "color": (0, 0, 255),
        "last_shot_time": None,
        "target": None
    }

def update_hunter(hunter, herbivores, carnivores):
    hunter["target"] = None

    for herbivore in herbivores:
        threatening_carnivore = min(
            carnivores,
            key=lambda c: math.hypot(herbivore["pos"][0] - c["pos"][0], 
                                    herbivore["pos"][1] - c["pos"][1]),
            default=None
        )

        if threatening_carnivore:
            move_towards(hunter, highest_threat_herbivore["pos"], HUNTER_SPEED)

            # Disparar al carnívoro si está dentro del rango de tiro
            if math.hypot(hunter["pos"][0] - threatening_carnivore["pos"][0], 
                        hunter["pos"][1] - threatening_carnivore["pos"][1]) <= HUNTER_SHOOT_RANGE:
                hunter["target"] = threatening_carnivore
                if hunter['last_shot_time'] is None or pygame.time.get_ticks() - hunter['last_shot_time'] >= HUNTER_RELOAD_TIME:
                    hunter['last_shot_time'] = pygame.time.get_ticks()
                    carnivores.remove(threatening_carnivore)