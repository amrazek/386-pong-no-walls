import pygame
import sys
from pygame.locals import *
from entities import *

window_size = (400, 400)
bkg_color = (0, 255, 0)

screen = pygame.display.set_mode(size=window_size, flags=HWSURFACE)
pygame.display.set_caption("Pong No Walls")
clock = pygame.time.Clock()

ball = Ball(screen, 10, pygame.color.Color('#FF0000'), pygame.Vector2(100, 0))
group = pygame.sprite.Group(ball)

elapsed_time = 0.0

while True:
    for evt in pygame.event.get():
        if evt.type == QUIT:
            pygame.quit()
            sys.exit(0)

    # update all sprites
    group.update(elapsed_time)

    # render all sprites
    screen.fill(bkg_color)
    group.draw(screen)
    pygame.display.flip()

    # limit FPS to 60, but otherwise execute as quickly as possible
    elapsed_time = clock.tick_busy_loop(60) / 1000.0