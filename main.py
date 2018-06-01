import numpy as np

import pygame
import sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

screen_size = (640, 480)
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pygame cheat sheet")

redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)

mouse_x, mouse_y = 0, 0

font = pygame.font.Font(None, 32)
msg = "Hello world"

fps = 30

while True:
    window.fill(whiteColor)

    pygame.draw.circle(window, blueColor, (300, 50), 20, 0)

    msg_surface = font.render(msg, False, blueColor)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (mouse_x, mouse_y)
    window.blit(msg_surface, msg_rect)

    # get numpy surface
    np_arr = pygame.surfarray.array3d(window)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                fps += 10
                fps = min(fps, 120)
            elif event.key == K_DOWN:
                fps-= 10
                fps = max(fps, 10)
            elif event.key == K_SPACE:
                fps = 60

            print(fps)

    pygame.display.update()
    fpsClock.tick(120)