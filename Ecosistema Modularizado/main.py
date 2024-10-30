import pygame
from plantas import initialize_plants
from herbivoros import initialize_herbivores, update_herbivores
from carnivoros import initialize_carnivores, update_carnivores
from cazador import initialize_hunter, update_hunter
from refugio import REFUGE_POSITION, REFUGE_RADIUS

# Inicialización de Pygame
pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema con Cazador")

# Inicializar entidades del ecosistema
plants = initialize_plants(50)
herbivores = initialize_herbivores(20)
carnivores = initialize_carnivores(10)
hunter = initialize_hunter()

# Bucle principal del juego
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 0, 255), REFUGE_POSITION, REFUGE_RADIUS)

    # Actualizar y dibujar plantas
    for plant in plants:
        pygame.draw.circle(screen, plant["color"], (int(plant["pos"][0]), int(plant["pos"][1])), 3)

    # Actualizar y dibujar herbívoros
    update_herbivores(herbivores, plants)

    # Actualizar y dibujar carnívoros
    update_carnivores(carnivores)

    # Actualizar y dibujar cazador
    update_hunter(hunter, herbivores, carnivores)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()