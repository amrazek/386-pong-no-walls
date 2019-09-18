import pygame
import math
import random
import entities
import config


class PaddleType:
    VERTICAL = 0
    TOP = 1
    BOTTOM = 2


class Board:
    IN_PROGRESS = 0
    LEFT_PLAYER = 1
    RIGHT_PLAYER = 2

    def __init__(self, input_state, state, size, left_player_generator, right_player_generator):
        assert size.width > 0 and size.height > 0

        self.bounds = pygame.Rect(0, 0, size.width, size.height)
        self._background = config.BACKGROUND_COLOR

        net = Board._create_net(self.bounds)

        self._ball = Board._create_ball(self.bounds, initial_velocity=Board._create_initial_velocity())

        left_center = self._create_paddle(paddle_type=PaddleType.VERTICAL)
        left_top = self._create_paddle(paddle_type=PaddleType.TOP)
        left_bottom = self._create_paddle(paddle_type=PaddleType.BOTTOM)

        right_center = self._create_paddle(player=Board.RIGHT_PLAYER)
        right_top = self._create_paddle(player=Board.RIGHT_PLAYER, paddle_type=PaddleType.TOP)
        right_bottom = self._create_paddle(player=Board.RIGHT_PLAYER, paddle_type=PaddleType.BOTTOM)

        self._paddles = pygame.sprite.Group(left_center, left_top, left_bottom, right_center, right_top, right_bottom)
        self._passives = pygame.sprite.Group(net)

        self._status = Board.IN_PROGRESS

        self._left_player = left_player_generator(input_state, left_center, left_top, left_bottom)
        self._right_player = right_player_generator(input_state, right_center, right_top, right_bottom)

        left_score_pos = pygame.Vector2(left_top.rect.centerx, left_top.rect.bottom)
        right_score_pos = pygame.Vector2(right_top.rect.centerx, right_top.rect.bottom)

        self._left_score = self._create_text(left_score_pos, self._left_player.name + ": " + str(state.points[0]))
        self._right_score = self._create_text(right_score_pos, self._right_player.name + ": " + str(state.points[1]))

        # text is centered at given pos, but this means it will overlap the top paddles somewhat
        delta_pos = pygame.Vector2(0, max(0.5 * self._left_score.rect.height, 0.5 * self._right_score.rect.height))

        self._left_score.set_position(self._left_score.get_position() + delta_pos)
        self._right_score.set_position(self._right_score.get_position() + delta_pos)

        self._passives.add(self._left_score, self._right_score)

    def update(self, elapsed):
        self._ball.update(elapsed, self._paddles)
        self._paddles.update(elapsed)

        self._left_player.update(elapsed, self._ball)
        self._right_player.update(elapsed, self._ball)

        # if the ball isn't anywhere on the field, it's out of bounds
        if not self._ball.rect.colliderect(self.bounds):
            # determine which player lost the ball: the other player scores a point
            if self._ball.get_position().x < self.bounds.centerx:
                # ball went off of left player's side -> right player wins
                self._status = Board.RIGHT_PLAYER
            else:
                self._status = Board.LEFT_PLAYER

    def update_scores(self, state):
        self._left_score.set_text(self._left_player.get_name() + ": " + str(state.points[0]))
        self._right_score.set_text(self._right_player.get_name() + ": " + str(state.points[1]))

    def draw(self, screen, draw_ball=True):
        screen.fill(self._background)
        self._passives.draw(screen)
        self._paddles.draw(screen)

        if draw_ball:
            screen.blit(dest=self._ball.rect, source=self._ball.image)

    def get_status(self):
        return self._status

    @property
    def left_player(self):
        return self._left_player

    @property
    def right_player(self):
        return self._right_player

    @classmethod
    def _create_net(cls, board_bounds):
        net = entities.Net(
            board_bounds=board_bounds,
            dash_length=config.NET_DASH_LENGTH,
            net_width=config.NET_WIDTH)

        return net

    @classmethod
    def _create_ball(cls, bounds, initial_velocity):
        ball = entities.Ball(
            radius=config.BALL_RADIUS,
            velocity_vector=initial_velocity,
            bounds=bounds)

        return ball

    def _create_paddle(self, player=LEFT_PLAYER, paddle_type=PaddleType.VERTICAL):
        is_vertical = paddle_type == PaddleType.VERTICAL

        width = config.PADDLE_THICKNESS if is_vertical else config.PADDLE_LENGTH
        height = config.PADDLE_THICKNESS if not is_vertical else config.PADDLE_LENGTH

        # define movement area
        movement_bounds = pygame.Rect(0, 0, self.bounds.width, self.bounds.height)

        # adjust bounds based on player side
        if player == Board.LEFT_PLAYER:
            if is_vertical:
                movement_bounds.width = 1
            else:
                movement_bounds.height = 1
                movement_bounds.width = self.bounds.width * 0.5  # can only move on its half of board

                if paddle_type == PaddleType.BOTTOM:
                    movement_bounds.top = self.bounds.height - height

                # also, do not let the paddle move so far to the left that it intersects
                # the vertical paddle
                movement_bounds.width -= config.PADDLE_THICKNESS
                movement_bounds.left += config.PADDLE_THICKNESS

        else:  # right player
            # everything must be on right-hand side, so start by moving the whole rect
            movement_bounds.left = self.bounds.width * 0.5
            movement_bounds.width = self.bounds.width * 0.5

            if is_vertical:  # adjust paddle so it sits on right hand side of screen
                movement_bounds.width = 1
                movement_bounds.left = self.bounds.width - width
            else:
                movement_bounds.height = 1

                if paddle_type == PaddleType.BOTTOM:  # adjust paddle so it lies at bottom of screen
                    movement_bounds.top = self.bounds.height - height

                # also, do not let the paddle move so far to the left that it intersects
                # the vertical paddle
                movement_bounds.width -= config.PADDLE_THICKNESS

        # define actual paddle size
        paddle_bounds = pygame.Rect(0, 0, width, height)

        paddle = entities.Paddle(paddle_bounds=paddle_bounds, movement_bounds=movement_bounds, speed=config.PADDLE_SPEED)

        return paddle

    @classmethod
    def _create_initial_velocity(cls):
        # determine a 60 degree arc
        arc_angle = random.uniform(0, 60.0 * 3.14159 / 180.0)

        # determine which player heading will receive ball initially
        x_velocity_multiplier = [-1.0, 1.0][random.randint(0, 1)]

        velocity = pygame.Vector2(math.cos(arc_angle - 3.14159 / 6.0), math.sin(arc_angle - 3.14159 / 6.0))
        velocity.x *= x_velocity_multiplier

        # todo: random velocity (angle AND speed)
        #return velocity * config.BALL_SPEED

        return pygame.Vector2(1, 0) * config.BALL_SPEED

    @classmethod
    def _create_text(cls, position, text=""):
        sprite = entities.TextSprite(text, color=config.SCORE_COLOR)

        # calculate corrected position such that the text is centered
        # at given position
        position.x -= sprite.rect.width * 0.5
        position.y -= sprite.rect.height * 0.5

        sprite.set_position(position)

        return sprite
