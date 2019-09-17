import pygame
from pygame.locals import *
import math
import helper
import config


class Ball(pygame.sprite.Sprite):
    def __init__(self, bounds, radius, ball_color, velocity_vector):
        super().__init__()

        self.velocity = velocity_vector
        self.radius = radius
        self.bounds = bounds
        self.position = pygame.Vector2(self.bounds.centerx, self.bounds.centery)

        self.image = config.BALL_SURFACE

        self.rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        self.rect.center = self.position

    def update(self, elapsed_seconds, paddles):
        delta_position = self.velocity * elapsed_seconds

        #next_position = self.position + delta_position
        #intersections = helper.line_line_intersection(self.position, next_position, pygame.Vector2(600, 0), pygame.Vector2(600, 600))

        next_rect = self.rect.copy()
        next_rect.center = self.position + delta_position

        for paddle in paddles:
            if next_rect.colliderect(paddle.rect):
                is_vertical = True if paddle.rect.height > paddle.rect.width else False

                if is_vertical:
                    self.velocity.x = -self.velocity.x
                else:
                    self.velocity.y = -self.velocity.y

                break

        self.position += delta_position
        self.rect = next_rect
        self.rect.center = self.position

    def get_position(self):
        return self.position


class MovementDirection:
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)
    STOP = pygame.Vector2()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddle_bounds, movement_bounds, speed):
        super().__init__()
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2()
        self.speed = speed

        self.paddle_bounds = paddle_bounds.copy()
        self.movement_bounds = movement_bounds.copy()

        self.movement_bounds.width -= paddle_bounds.width
        self.movement_bounds.height -= paddle_bounds.height

        self.movement_bounds.width = self.movement_bounds.width if self.movement_bounds.width > 0 else 1
        self.movement_bounds.height = self.movement_bounds.height if self.movement_bounds.height > 0 else 1

        self.movement_bounds.left += paddle_bounds.width * 0.5
        self.movement_bounds.top += paddle_bounds.height * 0.5

        self.image = config.HORIZONTAL_PADDLE_SURFACE \
            if paddle_bounds.width > paddle_bounds.height else config.VERTICAL_PADDLE_SURFACE

        self.rect = paddle_bounds.copy()

        self.position.x = self.movement_bounds.centerx
        self.position.y = self.movement_bounds.centery
        self.update(0.0)  # set up rect to match position

    def update(self, elapsed):
        move_amount = self.velocity * elapsed

        self.position += move_amount

        helper.rect_clamp_point_ip(self.movement_bounds, self.position)

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def move(self, direction=MovementDirection.STOP):
        self.velocity = direction * self.speed

    def get_position(self):
        return self.position

    def get_dimensions(self):
        return helper.Dimensions(self.rect.width, self.rect.height)


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
        num_dashes = self.image.get_height() / (dash_length * 2)
        offset = int((num_dashes - math.floor(num_dashes)) * dash_length)

        for y in range(offset, self.image.get_height() + dash_length + offset, dash_length * 2):
            fill_rect = dash_rect.copy()
            fill_rect.centery = y
            fill_rect.clip(self.image.get_rect())

            self.image.fill(color=dash_color, rect=fill_rect)


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text="", font="consolas", size=16, color=(255, 255, 255)):
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
