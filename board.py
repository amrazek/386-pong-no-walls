import pygame
import collections
import entities
import math
import random


class PaddleType:
    VERTICAL = 0
    TOP = 1
    BOTTOM = 2


class Board:
    BACKGROUND_COLOR = pygame.Color('#000000')
    BALL_COLOR = pygame.Color('#FF0000')

    NET_DASH_LENGTH = 30
    NET_WIDTH = 10

    BALL_RADIUS = 10
    BALL_SPEED = 400.0

    IN_PROGRESS = 0
    LEFT_PLAYER = 1
    RIGHT_PLAYER = 2

    def __init__(self, input, size, left_player_generator, right_player_generator):
        assert size.width > 0 and size.height > 0

        self._bounds = pygame.Rect(0, 0, size.width, size.height)
        self._background = Board.BACKGROUND_COLOR

        net = Board._create_net(self._bounds)

        self._ball = Board._create_ball(self._bounds, initial_pos=self._bounds.center,
                                        initial_velocity=Board._create_initial_velocity())

        left_center = self._create_paddle(10, 100, type=PaddleType.VERTICAL)
        left_top = self._create_paddle(100, 10, type=PaddleType.TOP)
        left_bottom = self._create_paddle(100, 10, type=PaddleType.BOTTOM)

        right_center = self._create_paddle(10, 100, player=Board.RIGHT_PLAYER)
        right_top = self._create_paddle(100, 10, player=Board.RIGHT_PLAYER, type=PaddleType.TOP)
        right_bottom = self._create_paddle(100, 10, player=Board.RIGHT_PLAYER, type=PaddleType.BOTTOM)

        self._paddles = pygame.sprite.Group(left_center, left_top, left_bottom, right_center, right_top, right_bottom)
        self._passives = pygame.sprite.Group(net)

        self._status = Board.IN_PROGRESS

        self._left_player = left_player_generator(input, left_center, left_top, left_bottom)
        self._right_player = right_player_generator(input, right_center, right_top, right_bottom)

    def update(self, elapsed):
        self._ball.update(elapsed, self._paddles) 
        self._paddles.update(elapsed)

        self._left_player.update(elapsed, self._ball)
        self._right_player.update(elapsed, self._ball)

        # if the ball isn't anywhere on the field, it's out of bounds
        if not self._ball.rect.colliderect(self._bounds):
            if self._ball.get_position().x < self._bounds.left:
                self._status = Board.LEFT_PLAYER
            else:
                self._status = Board.RIGHT_PLAYER

    def draw(self, screen):
        screen.fill(self._background)
        self._passives.draw(screen)
        self._paddles.draw(screen)

        screen.blit(dest=self._ball.rect, source=self._ball.image)

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

    def _create_paddle(self, width, height, player=LEFT_PLAYER, type=PaddleType.VERTICAL):
        is_vertical = type == PaddleType.VERTICAL

        # define movement area
        movement_bounds = pygame.Rect(0, 0, self._bounds.width, self._bounds.height)

        # adjust bounds based on player side
        if player == Board.LEFT_PLAYER:
            if is_vertical:
                movement_bounds.width = 1
            else:
                movement_bounds.height = 1
                movement_bounds.width = self._bounds.width * 0.5  # can only move on its half of board

                if type == PaddleType.BOTTOM:
                    movement_bounds.top = self._bounds.height - height * 0.5

        else:  # right player
            # everything must be on right-hand side, so start by moving the whole rect
            movement_bounds.left = self._bounds.width * 0.5
            movement_bounds.width = self._bounds.width * 0.5

            if is_vertical:  # adjust paddle so it sits on right hand side of screen
                movement_bounds.width = 1
                movement_bounds.left = self._bounds.width - width
            else:
                movement_bounds.height = 1

                if type == PaddleType.BOTTOM:  # adjust paddle so it lies at bottom of screen
                    movement_bounds.top = self._bounds.height - height * 0.5

        # define actual paddle size
        paddle_bounds = pygame.Rect(0, 0, width, height)

        paddle = entities.Paddle(paddle_bounds=paddle_bounds, movement_bounds=movement_bounds, speed=100)

        return paddle

    @classmethod
    def _create_initial_velocity(cls):
        # determine a 60 degree arc
        arc_angle = random.uniform(0, 60.0 * 3.14159 / 180.0)

        # determine which player heading will receive ball initially
        x_velocity_multiplayer = [-1.0, 1.0][random.randint(0, 1)]

        velocity = pygame.Vector2(math.cos(arc_angle - 3.14159 / 6.0), math.sin(arc_angle - 3.14159 / 6.0))
        velocity.x *= x_velocity_multiplayer

        return velocity * Board.BALL_SPEED