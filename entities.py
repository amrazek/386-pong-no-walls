import pygame
from pygame.locals import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, ball_color):
        super(Ball, self).__init__()

        # this will be an image later, so might as well save some time and
        # make it a surface to begin with
        self.image = pygame.Surface((radius * 2, radius * 2), HWSURFACE)
        self.image = self.image.convert()

        mask_color = (0, 0, 0)
        self.image.set_colorkey(mask_color)
        self.image.fill(mask_color)

        pygame.draw.circle(self.image, ball_color, (radius, radius), radius)

        self.rect = pygame.Rect(200, 200, radius, radius)
