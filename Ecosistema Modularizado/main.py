import pygame
import random
from herbivoros import Herbivore
from carnivoros import Carnivore
from plantas import Plant
from cazador import Hunter
from refugio import REFUGE_POSITION, REFUGE_RADIUS, is_in_refuge

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))

NUM_PLANTS = 50
NUM_HERBIVORES = 20
NUM_CARNIVORES = 10

plants = [Plant(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_PLANTS)]
herbivores = [Herbivore(random.randint(0, WIDTH), random.randint(0, HEIGHT), (0, 255, 0), "herbivore_type_1") for _ in range(NUM_HERBIVORES)]
carnivores = [Carnivore(random.randint(0, WIDTH), random.randint(0, HEIGHT), (255, 0, 0), "carnivore_type_1") for _ in range(NUM_CARNIVORES)]
hunter = Hunter(WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 0, 255), REFUGE_POSITION, REFUGE_RADIUS, 1)
    for plant in plants:
        pygame.draw.circle(screen, plant.color, (int(plant.pos[0]), int(plant.pos[1])), 3)
    for herbivore in herbivores[:]:
        if not herbivore.update(plants, REFUGE_POSITION):
            herbivores.remove(herbivore)
    for carnivore in carnivores[:]:
        carnivore.update(herbivores)
    hunter.hunt(herbivores)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
