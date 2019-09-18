import math
import pygame
from pygame.locals import *
import config
from board import Board
import players
import entities


class InputState:
    def __init__(self):
        self.quit = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def event_loop(self):
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.quit = True
            elif evt.type == KEYDOWN or evt.type == KEYUP:
                state: bool = True if evt.type == KEYDOWN else False

                if evt.key == K_LEFT:
                    self.left = state
                elif evt.key == K_RIGHT:
                    self.right = state
                elif evt.key == K_UP:
                    self.up = state
                elif evt.key == K_DOWN:
                    self.down = state
                elif evt.key == K_ESCAPE:
                    self.quit = True


# base state which other "states" (playing a game, menu, victory, etc) derive
# this hides all the ugly logic and makes for a clean game loop
class GameState:
    def __init__(self, input_state, previous_state=None):
        if previous_state is not None:
            self._left_score, self._right_score = previous_state.points
            self._left_wins, self._right_wins = previous_state.games_won
        else:
            self._left_score, self._right_score = 11, 12
            self._left_wins, self._right_wins = 0, 0

        self._input_state = input_state

    @staticmethod
    def create_initial(input_state):
        return BeginGame(input_state)

    @property
    def next_state(self):
        raise RuntimeError

    @property
    def finished(self):
        raise RuntimeError

    def update(self, elapsed):
        raise RuntimeError

    def draw(self, screen):
        raise RuntimeError

    @property
    def points(self):
        return self._left_score, self._right_score

    @property
    def games_won(self):
        return self._left_wins, self._right_wins


# this is actual "in game" play and runs until the ball goes out of bounds
class PlayGame(GameState):
    def __init__(self, input_state, previous_state=None):
        super().__init__(input_state, previous_state)

        self.board = Board(input_state=input_state,
                           state=self,
                           size=config.WINDOW_SIZE,
                           left_player_generator=players.Player,
                           right_player_generator=players.ComputerPlayer)

    @property
    def next_state(self):
        if not self.finished:
            raise RuntimeError

        # score will determine next state
        if self.board.get_status() == Board.LEFT_PLAYER:
            self._left_score += 1
        else:
            self._right_score += 1

        # determine if a player has won a game
        if self._left_score >= config.MIN_POINTS_TO_WIN_GAME or self._right_score >= config.MIN_POINTS_TO_WIN_GAME:
            # to win a rally, one player's score must also be at least two greater than the other's
            if abs(self._left_score - self._right_score) >= config.MIN_POINT_DIFFERENCE_TO_WIN:
                # one of the players has won a set
                winner = Board.LEFT_PLAYER if self._left_score > self._right_score else Board.RIGHT_PLAYER

                if winner == Board.LEFT_PLAYER:
                    self._left_wins += 1
                else:
                    self._right_wins += 1

                self._left_score = self._right_score = 0  # reset for next game

                return GameVictory(input_state=self._input_state, previous_state=self)

        # determine if a player has won the set
        if self._left_wins < config.NUMBER_GAMES_REQUIRED_VICTORY and \
                self._left_wins < config.NUMBER_GAMES_REQUIRED_VICTORY:
            # move to next game
            return BeginGame(input_state=self._input_state, previous_state=self)
        else:
            raise NotImplementedError  # TODO: victory screen

    @property
    def finished(self):
        return self.board.get_status() != Board.IN_PROGRESS

    def update(self, elapsed):
        self.board.update(elapsed)

    def draw(self, screen):
        self.board.draw(screen)


# this state displays a countdown before game begins
# and informs players how many more points are needed
# to win (as per project requirements)
class BeginGame(GameState):
    def __init__(self, input_state, previous_state=None):
        super().__init__(input_state, previous_state)
        self._game = PlayGame(input_state, previous_state)
        self._display_time = 0

        _countdown_messages = ["Game starts in " + str(x) + "..." for x in reversed(range(1, config.COUNTDOWN_BEGIN + 1))]
        _countdown_messages.append("Begin!")

        self._countdown_messages = [entities.TextSprite(text=x, color=config.SCORE_COLOR) for x in _countdown_messages]

        board_center = pygame.Vector2(config.WINDOW_SIZE.width * 0.5, config.WINDOW_SIZE.height * 0.5)

        for msg in self._countdown_messages:
            center = board_center - pygame.Vector2(msg.rect.width * 0.5, msg.rect.height * 0.5)
            msg.set_position(center)

        # determine how many more points each player needs to win
        left_points_needed = BeginGame.calc_points_needed(self.points[0], self.points[1])
        right_points_needed = BeginGame.calc_points_needed(self.points[1], self.points[0])

        self._left_spr = entities.TextSprite(text=str(left_points_needed) + " points to go!", color=config.SCORE_COLOR)
        self._right_spr = entities.TextSprite(text=str(right_points_needed) + " points to go!", color=config.SCORE_COLOR)

        def center_text(text_sprite, board_location):
            text_sprite.rect.center = board_location

        quarter_offset = pygame.Vector2(config.WINDOW_SIZE.width * 0.25, 0)

        center_text(self._left_spr, board_center - quarter_offset)
        center_text(self._right_spr, board_center + quarter_offset)

    @property
    def next_state(self):
        return self._game

    @property
    def finished(self):
        return len(self._countdown_messages) == 0

    def update(self, elapsed):
        self._display_time += elapsed

        if self._display_time >= config.DURATION_PER_MESSAGE and len(self._countdown_messages) > 0:
            self._countdown_messages = self._countdown_messages[1:]
            self._display_time -= config.DURATION_PER_MESSAGE

        # allow game to start once we're on last message (which should be "begin")
        if len(self._countdown_messages) <= 1:
            self._game.update(elapsed)

    def draw(self, screen):
        self._game.draw(screen)  # draw board

        if len(self._countdown_messages) > 0:
            current = self._countdown_messages[0]
            screen.blit(source=current.image, dest=current.rect)

        screen.blit(source=self._left_spr.image, dest=self._left_spr.rect)
        screen.blit(source=self._right_spr.image, dest=self._right_spr.rect)

    @staticmethod
    def calc_points_needed(target_player_points, other_player_points):
        delta_score = abs(target_player_points - other_player_points)
        target_winning = True if target_player_points > other_player_points else False

        # calculate how many points target player needs to win
        if target_player_points < config.MIN_POINTS_TO_WIN_GAME:
            # two cases possible: if the spread is greater than required diff, only need remaining points to 11
            # otherwise, we need 11 points AND at least two more than other player
            if delta_score > config.MIN_POINT_DIFFERENCE_TO_WIN and target_winning:
                return config.MIN_POINTS_TO_WIN_GAME - target_player_points
            else:
                return max(config.MIN_POINTS_TO_WIN_GAME - target_player_points, other_player_points + config.MIN_POINT_DIFFERENCE_TO_WIN - target_player_points)

        else:  # target player has at least the minimum points
            # they need other player's + 2
            return other_player_points + 2 - target_player_points


# when a game is completed (one player has reached 11 points and at least 2 points higher than opponent)
# this is a brief screen to mention why scores are resetting
class GameVictory(GameState):
    def __init__(self, input_state, previous_state=None):
        super().__init__(input_state, previous_state)

        # borrow the board from previous state
        self.board = previous_state.board

        # create "X won game" message
        winner, score = (self.board.left_player, self.games_won[0]) if self.points[0] > self.points[1] else (self.board.right_player, self.games_won[1])

        self._game_won = entities.TextSprite(
            text=winner.name + " has won " + str(score) + " of " + str(config.NUMBER_GAMES_REQUIRED_VICTORY * 2 - 1),
            color=config.SCORE_COLOR)

        self._game_won.set_center(self.board.bounds.center)

        # track display time
        self._elapsed = 0.0

    @property
    def next_state(self):
        if not self.finished:
            raise RuntimeError

        return BeginGame(input_state=self._input_state, previous_state=self)

    @property
    def finished(self):
        return self._elapsed > config.DURATION_PER_GAME_VICTORY_MESSAGE

    def update(self, elapsed):
        self._elapsed += elapsed

    def draw(self, screen):
        self.board.draw(screen)
        screen.blit(source=self._game_won.image, dest=self._game_won.rect)