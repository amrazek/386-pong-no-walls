import pygame
from pygame.locals import *
import math
import helper
from enum import Enum


class Ball(pygame.sprite.Sprite):
    def __init__(self, bounds, radius, ball_color, velocity_vector):
        super().__init__()

        self.velocity = velocity_vector
        self.radius = radius
        self.bounds = bounds
        self.position = pygame.Vector2(self.bounds.centerx, self.bounds.centery)

        # this will be an image later, so might as well save some time and
        # make it a surface to begin with
        self.image = pygame.Surface((radius * 2, radius * 2), HWSURFACE)
        self.image = self.image.convert()

        mask_color = (0, 0, 0)
        self.image.set_colorkey(mask_color)
        self.image.fill(mask_color)

        pygame.draw.circle(self.image, ball_color, (radius, radius), radius)

        self.rect = pygame.Rect(200, 200, radius * 2, radius * 2)

    def update(self, paddles, elapsed_seconds):
        delta_position = self.velocity * elapsed_seconds

        # attempt to move in x direction
        next_rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)
        next_rect.centerx += delta_position.x

        for paddle in paddles:
            if next_rect.colliderect(paddle.rect):
                delta_position.x = 0
                self.velocity.x *= -1
                next_rect = self.rect
                break

        self.rect = next_rect  # accept delta x change
        self.position.x += delta_position.x

        # attempt to move in y direction
        next_rect = next_rect.copy()
        next_rect.centery += delta_position.y

        for paddle in paddles:
            if next_rect.colliderect(paddle.rect):
                delta_position.y = 0
                self.velocity.y *= -1
                next_rect = self.rect
                break

        self.rect = next_rect
        self.position.y += delta_position.y

    def get_position(self):
        return self.position


class MovementDirection(Enum):
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)
    STOP = pygame.Vector2()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, size, speed, bounds, color=(255, 242, 0)):
        super().__init__()

        self.speed = speed
        self.size = size
        self.bounds = bounds.copy()
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2()

        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(0, 0, size[0], size[1])

        self.position.x = self.bounds.centerx
        self.position.y = self.bounds.centery

        self.image.fill(color)
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

    def get_position(self):
        return self.position


class Net(pygame.sprite.Sprite):
    def __init__(self, board_bounds, net_width, dash_length, dash_color=(255, 255, 255)):
        super().__init__()

        # generate an appropriate net surface - no sense in doing this
        # every single frame
        self.rect = pygame.Rect(0, 0, net_width, board_bounds.height)
        self.rect.center = board_bounds.center

        self.image = pygame.Surface((net_width, board_bounds.height))

        self.image.fill(color=(0, 0, 0))  # fill with black

        # generate dashes
        dash_rect = pygame.Rect(0, 0, net_width, dash_length)
        dash_rect.centery = 0

        # calculate offset such that the first and last dash will have the
        # same amount of space between their edge and the edge of the board
        num_dashes = self.image.get_height() / (dash_length * 2);
        offset = int((num_dashes - math.floor(num_dashes)) * dash_length)

        for y in range(offset, self.image.get_height() + dash_length + offset, dash_length * 2):
            fill_rect = dash_rect.copy()
            fill_rect.centery = y
            fill_rect.clip(self.image.get_rect())

            self.image.fill(color=dash_color, rect=fill_rect)


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text="", font="consolas", size=16, color=(255,255,255)):
        super().__init__()
        self.text = text
        self.font = pygame.sysfont.SysFont(font, size)
        self.color = color
        self.rect = pygame.Rect(0, 0, size, size)
        self.__update_image()

    def __update_image(self):
        self.image = self.font.render(self.text, False, self.color)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

    def set_position(self, position):
        self.rect.left = position.x
        self.rect.top = position.y
