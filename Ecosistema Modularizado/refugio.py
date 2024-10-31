import math

REFUGE_POSITION = (924, 384)  
REFUGE_RADIUS = 50
REFUGE_DURATION = 4000

def is_in_refuge(pos):
    return math.hypot(pos[0] - REFUGE_POSITION[0], pos[1] - REFUGE_POSITION[1]) < REFUGE_RADIUS
