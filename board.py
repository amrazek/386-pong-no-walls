import pygame
import collections
import entities
import math
import random


class Board:
    BACKGROUND_COLOR = pygame.Color('#000000')
    BALL_COLOR = pygame.Color('#FF0000')

    NET_DASH_LENGTH = 30
    NET_WIDTH = 10

    BALL_RADIUS = 10
    BALL_SPEED = 400.0

    IN_PROGRESS = 0
    LEFT_WON = 1
    RIGHT_WON = 2

    def __init__(self, size, left_player_generator, right_player_generator):
        assert size.width > 0 and size.height > 0

        self._bounds = pygame.Rect(0, 0, size.width, size.height)
        self._background = Board.BACKGROUND_COLOR

        net = Board._create_net(self._bounds)
        ball = Board._create_ball(self._bounds, initial_pos=self._bounds.center, initial_velocity=Board._create_initial_velocity())

        self.decorations = pygame.sprite.Group(net)
        self.balls = pygame.sprite.Group(ball)

        self._status = Board.IN_PROGRESS

        self._left_player = left_player_generator()
        self._right_player = right_player_generator()

    def update(self, elapsed):
        self.decorations.update(elapsed)
        self.balls.update(elapsed)  # todo: ball needs paddles, elapsed time to update

        self._left_player.update(elapsed)
        self._right_player.update(elapsed)

        # check if ball out of bounds
        outside_balls = [ball for ball in self.balls if not ball.rect.colliderect(self._bounds)]

        for ball in outside_balls:
            if ball.get_position().x < self._bounds.left:
                self._status = Board.LEFT_WON
            else:
                self._status = Board.RIGHT_WON

    def draw(self, screen):
        screen.fill(self._background)
        self.decorations.draw(screen)
        self.balls.draw(screen)

    def get_status(self):
        return self._status

    @classmethod
    def _create_net(cls, board_bounds):
        net = entities.Net(
            board_bounds=board_bounds,
            dash_length=cls.NET_DASH_LENGTH,
            net_width=cls.NET_WIDTH)

        return net

    @classmethod
    def _create_ball(cls, bounds, initial_pos, initial_velocity):
        ball = entities.Ball(
            ball_color=Board.BALL_COLOR,
            radius=Board.BALL_RADIUS,
            velocity_vector=initial_velocity,
            bounds=bounds)

        return ball

    @classmethod
    def _create_initial_velocity(cls):
        # determine a 60 degree arc
        # arc_angle = random.uniform(0, 60.0 * 3.14159 / 180.0)
        #
        # # determine which player heading will receive ball initially
        # x_velocity_multiplayer = [-1.0, 1.0][random.randint(0, 1)]
        #
        # velocity = pygame.Vector2(math.cos(arc_angle - 30), math.sin(arc_angle - 30))
        # velocity.x *= x_velocity_multiplayer
        #
        # return velocity * Board.BALL_SPEED
        return pygame.Vector2(1.0, 0.0) * Board.BALL_SPEED
