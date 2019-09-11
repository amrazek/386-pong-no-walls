import pygame
from pygame.locals import *
import math
from enum import Enum


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, radius, ball_color, velocity_vector):
        super(Ball, self).__init__()

        self.velocity = velocity_vector
        self.radius = radius
        self.bounds = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.position = pygame.Vector2(self.bounds.centerx, self.bounds.centery)

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


class MovementStyle(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class Paddle(pygame.sprite.Sprite):
    def __init__(self, size, speed, bounds, style=MovementStyle.VERTICAL):
        super().__init__()

        self.speed = speed
        self.bounds = bounds
        self.size = size
        self.style = style
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(0, 0, size[0], size[1])

        if style == MovementStyle.VERTICAL:
            self.min_position = self.bounds.top + size[1] * 0.5
            self.max_position = self.bounds.bottom - size[1] * 0.5
        else:
            self.min_position = self.bounds.left + size[0] * 0.5
            self.max_position = self.bounds.right - size[0] * 0.5

        yellow = (255, 242, 0)
        self.image.fill(yellow)
        self.image = self.image.convert()

        self.position = bounds.centery if style == MovementStyle.VERTICAL else bounds.centerx
        self.target_position = self.position

    def __calculate_movement(self, elapsed):
        distance_to_target = self.target_position - self.position
        return self.speed * elapsed, distance_to_target

    def update(self, elapsed_seconds):
        movement, dist_left = self.__calculate_movement(elapsed_seconds)
        direction = 1.0 if dist_left > 0 else -1.0

        if movement > math.fabs(dist_left):
            self.position = self.target_position
        else:
            self.position += movement * direction
            self.position = self.min_position if self.position < self.min_position else self.position
            self.position = self.max_position if self.position > self.max_position else self.position

        self.__update_rect()

    def __update_rect(self):
        if self.style == MovementStyle.VERTICAL:
            self.rect.centery = self.position
        else:
            self.rect.centerx = self.position

        self.rect.clamp_ip(self.bounds)

    def move_to(self, position):
        self.target_position = position

    def get_position(self):
        return self.position

    def get_bounds(self):
        return self.bounds
