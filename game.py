import pygame
import sys
from pygame.locals import *
from entities import *

window_size = (400, 400)
bkg_color = (0, 255, 0)

screen = pygame.display.set_mode(size=window_size, flags=HWSURFACE)
pygame.display.set_caption("Pong No Walls")
clock = pygame.time.Clock()

ball = Ball(10, pygame.color.Color('#FF0000'))
group = pygame.sprite.Group(ball)

while True:
    for evt in pygame.event.get():
        if evt.type == QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill(bkg_color)
    group.draw(screen)
    pygame.display.flip()

    clock.tick_busy_loop(60)