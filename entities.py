import pygame
from pygame.locals import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, radius, ball_color, velocity_vector):
        super(Ball, self).__init__()


        self.velocity = velocity_vector
        self.radius = radius
        self.bounds = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.position = pygame.Vector2((self.bounds.centerx, self.bounds.centery))

        # this will be an image later, so might as well save some time and
        # make it a surface to begin with
        self.image = pygame.Surface((radius * 2, radius * 2), HWSURFACE)
        self.image = self.image.convert()

        mask_color = (0, 0, 0)
        self.image.set_colorkey(mask_color)
        self.image.fill(mask_color)

        pygame.draw.circle(self.image, ball_color, (radius, radius), radius)

        self.rect = pygame.Rect(200, 200, radius, radius)

    def update(self, elapsed_seconds):
        self.position += self.velocity * elapsed_seconds
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)