import pygame
import random
import math
from herbivoros import Herbivore
from carnivoros import Carnivore
from plantas import Plant
from cazador import Hunter

pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Ecosistema con Cazador")

NUM_PLANTS = 50
NUM_HERBIVORES = 20
NUM_CARNIVORES = 10

plants = [Plant.create_random_plant(WIDTH, HEIGHT) for _ in range(NUM_PLANTS)]
herbivores = [
    Herbivore([random.randint(0, WIDTH), random.randint(0, HEIGHT)], (0, 255, 0)) for _ in range(NUM_HERBIVORES // 2)
] + [
    Herbivore([random.randint(0, WIDTH), random.randint(0, HEIGHT)], (173, 255, 47)) for _ in range(NUM_HERBIVORES // 2)
]

carnivores = [
    Carnivore([random.randint(0, WIDTH), random.randint(0, HEIGHT)], (255, 0, 0)) for _ in range(NUM_CARNIVORES // 2)
] + [
    Carnivore([random.randint(0, WIDTH), random.randint(0, HEIGHT)], (255, 165, 0)) for _ in range(NUM_CARNIVORES // 2)
]

hunter_position = [WIDTH // 2, HEIGHT // 2]
hunter_color = (0, 0, 255)
hunter_speed = 1.1

hunter = Hunter(hunter_position,hunter_color)

def move_towards(organism,target_pos,speed=1):
    dx ,dy=target_pos[0]-organism.pos[0],target_pos[1]-organism.pos[1]
    dist=math.hypot(dx ,dy)
    
    if dist!=0:
       organism.pos[0]+=(dx/dist)*speed 
       organism.pos[1]+=(dy/dist)*speed 

running=True 
clock=pygame.time.Clock()
while running:
     for event in pygame.event.get():
         if event.type==pygame.QUIT:
             running=False 

     screen.fill((0 ,0 ,0))
     
     # Draw plants.
     for plant in plants:
         pygame.draw.circle(screen , plant.color , (int(plant.pos[0]), int(plant.pos[1])), radius=3)

     # Update and draw herbivores.
     for herbivore in herbivores[:]:
         herbivore.update_energy(-.1)

         closest_plant=min(plants , key=lambda p: math.hypot(herbivore.pos[0]-p.pos[0], herbivore.pos[1]-p.pos[1]), default=None)

         if closest_plant and math.hypot(herbivore.pos[0]-closest_plant.pos[0], herbivore.pos[1]-closest_plant.pos[1]) <5 :
             herbivore.update_energy(20)
             plants.remove(closest_plant)

         if herbivore.is_alive():
             move_towards(herbivore , closest_plant.pos if closest_plant else herbivore.pos)
             pygame.draw.circle(screen , herbivore.color , (int(herbivore.pos[0]), int(herbivore.pos[1])), radius=5)

     # Update and draw carnivores.
     for carnivore in carnivores[:]:
         carnivore.update_energy(-.3)

         closest_herbivore=min(
             [h for h in herbivores if h.is_alive()],
             key=lambda h: math.hypot(carnivore .pos [0]-h .pos [0], carnivore .pos [1]-h .pos [1]),
             default=None)

         if closest_herbivore and math.hypot(carnivore .pos [0]-closest_herbivore .pos [0], carnivore .pos [1]-closest_herbivore .pos [1]) <5 :
             carnivore.update_energy(40)
             herbivores.remove(closest_herbivore)

         if carnivore.is_alive():
             move_towards(carnivore , closest_herbivore .pos if closest_herbivore else carnivore .pos)
             pygame.draw.circle(screen , carnivore.color , (int(carnivore .pos [0]), int(carnivore .pos [1])), radius=6)

     # Hunter Logic 
     highest_threat_herbivore=None 
     closest_threatening_carnivore=None 

     for herbivore in herbivores:
         threatening_carnivore=min(
             carnivores,
             key=lambda c: math.hypot(herbivore .pos [0]-c .pos [0], herbivore .pos [1]-c .pos [1]),
             default=None)

         if threatening_carnivore and (
             highest_threat_herbivore is None or 
             math.hypot(threatening_carnivore .pos [0]-herbivore .pos [0], threatening_carnivore .pos [1]-herbivore .pos [1]) <
             math.hypot(closest_threatening_carnivore .pos [0]-highest_threat_herbivore .pos [0], closest_threatening_carnivore .pos [1]-highest_threat_herbivore .pos [1])
         ):
             highest_threat_herbivore=herbivore 
             closest_threatening_carnivore=threatening_carnivore 

     if highest_threat_herbivore and closest_threatening_carnivore:
         move_towards(hunter , highest_threat_herbivore .pos , hunter_speed)

         if hunter.shoot():
             carnivores.remove(closest_threatening_carnivore)

     pygame.draw.circle(screen , hunter.color , (int(hunter .pos [0]), int(hunter .pos [1])), radius=8)

     pygame.display.flip()
     clock.tick(30)

pygame.quit()