import pygame
import math
import random
import helper
import config


class Ball(pygame.sprite.Sprite):
    def __init__(self, bounds, radius, velocity_vector):
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

        ball_start = self.position
        ball_end = ball_start + delta_position

        # ball is on field, determine whether it has collided with any paddles
        for paddle in pygame.sprite.spritecollide(sprite=self, group=paddles, dokill=False):
            for segment in paddle.get_line_segments():
                intersections = helper.line_circle_intersection(ball_end, config.BALL_RADIUS, segment[0], segment[1])

                if len(intersections) > 0:
                    # this move has resulted in a collision!
                    segment_dir = (segment[1] - segment[0]).normalize()
                    vertical_line = pygame.Vector2(0, 1)

                    is_vertical = True if abs(segment_dir.dot(vertical_line)) >= 0.99 else False

                    if is_vertical:
                        self.velocity.x = -self.velocity.x
                    else:
                        self.velocity.y = -self.velocity.y

                    Ball.play_sound()

                    return

        self.position += delta_position
        self.rect.center = self.position

    def get_position(self):
        return self.position

    @staticmethod
    def play_sound():
        num_sounds = len(config.PADDLE_BOUNCE_SOUNDS)

        if num_sounds == 0:
            return

        which = config.PADDLE_BOUNCE_SOUNDS[random.randint(0, len(config.PADDLE_BOUNCE_SOUNDS) - 1)]
        which.play()


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

    def get_line_segments(self):
        top_left = pygame.Vector2(self.rect.left, self.rect.top)
        top_right = pygame.Vector2(self.rect.right, self.rect.top)
        bottom_right = pygame.Vector2(self.rect.right, self.rect.bottom)
        bottom_left = pygame.Vector2(self.rect.left, self.rect.bottom)

        return [(top_left, top_right),
                (top_right, bottom_right),
                (bottom_right, bottom_left), (bottom_left, top_right)]


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

    def set_center(self, center_position):
        self.rect.center = center_position

    def get_position(self):
        return pygame.Vector2(self.rect.left, self.rect.top)

    def set_text(self, text):
        self.text = text
        self.__update_image()
