import pygame
from pygame.locals import *
import math
import helper
from enum import Enum


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, radius, ball_color, velocity_vector):
        super().__init__()

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

    def update(self, paddles, elapsed_seconds):
        delta_position = self.velocity * elapsed_seconds

        next_rect = pygame.Rect(self.rect.centerx - self.radius, self.rect.centery - self.radius, self.radius, self.radius)
        next_rect.centerx += delta_position.x

        for paddle in paddles:
            if next_rect.colliderect(paddle.rect):
                delta_position.x = 0
                self.velocity.x *= -1
                break

        self.rect.centerx += delta_position.x

        next_rect.centery += delta_position.y

        for paddle in paddles:
            if next_rect.colliderect(paddle.rect):
                delta_position.y = 0
                self.velocity.y *= -1
                break

        self.rect.centery += delta_position.y



class MovementDirection(Enum):
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)
    STOP = pygame.Vector2()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, size, speed, bounds):
        super().__init__()

        self.speed = speed
        self.size = size
        self.bounds = bounds
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2()

        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(0, 0, size[0], size[1])

        self.position.x = self.rect.centerx
        self.position.y = self.rect.centery

        yellow = (255, 242, 0)
        self.image.fill(yellow)
        self.image = self.image.convert()

    def update(self, elapsed):
        move_amount = self.velocity * self.speed * elapsed

        self.position += move_amount

        helper.rect_clamp_point_ip(self.bounds, self.position)

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

        self.rect.clamp_ip(self.bounds)

    def move(self, direction=MovementDirection.STOP):
        self.velocity = direction.value
