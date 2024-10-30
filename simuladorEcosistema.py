import pygame
import random

# Configuración básica de pantalla
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema")

# Configuración de organismos
NUM_ORGANISMS = 30
organisms = []

# Inicializar organismos con posiciones y colores aleatorios
for _ in range(NUM_ORGANISMS):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    organisms.append({"pos": [x, y], "color": color})

# Bucle principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Actualizar y dibujar organismos
    for organism in organisms:
        # Movimiento aleatorio
        organism["pos"][0] += random.randint(-2, 2)
        organism["pos"][1] += random.randint(-2, 2)

        # Mantener organismos dentro de la pantalla
        organism["pos"][0] = max(0, min(WIDTH, organism["pos"][0]))
        organism["pos"][1] = max(0, min(HEIGHT, organism["pos"][1]))

        # Dibujar organismo
        pygame.draw.circle(screen, organism["color"], (int(organism["pos"][0]), int(organism["pos"][1])), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
