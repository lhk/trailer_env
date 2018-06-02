import numpy as np

import pygame
import sys
import colors
from pygame.locals import *
from utils import rotate
import params
from environment import Environment

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(params.screen_size)
pygame.display.set_caption("Pygame cheat sheet")

mouse_x, mouse_y = 0, 0

env = Environment(params.screen_size, params.car_size, params.num_obstacles)

while True:

    frame = env.render(return_numpy=False)
    window.blit(frame, (0,0))

    acceleration = 0
    steering_angle = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        acceleration = 1
    elif keys[K_DOWN]:
        acceleration = -1
    if keys[K_LEFT]:
        steering_angle=-1
    elif keys[K_RIGHT]:
        steering_angle = 1

    env.make_action(acceleration, steering_angle)
    pygame.display.update()

    clock.tick(30)