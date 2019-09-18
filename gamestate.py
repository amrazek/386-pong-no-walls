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
            self._left_wins, self._right_wins = previous_state.points
        else:
            self._left_score, self._right_score = 0, 0
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

        # determine if right threshold is high enough for a player to win a rally
        if self._left_score >= config.MIN_POINTS_TO_WIN_RALLY or  self._right_score >= config.MIN_POINTS_TO_WIN_RALLY:
            # to win a rally, one player's score must also be at least
            # two greater than the other's
            if math.abs(self._left_score - self._right_score) >= config.MIN_POINT_DIFFERENCE_TO_WIN:
                # one of the players has one a set
                winner = Board.LEFT_PLAYER if self._left_score > self._right_score else Board.RIGHT_PLAYER

                if winner == Board.LEFT_PLAYER:
                    self._left_wins += 1
                else:
                    self._right_wins += 1

                self._left_score = self._right_score = 0  # reset for next rally

        # if the set does not have a winner yet, continue
        if self._left_wins < config.NUMBER_RALLIES_TO_WIN and self._right_wins < config.NUMBER_RALLIES_TO_WIN:
            # move to next game in the rally
            next = BeginGame(input_state=self._input_state, previous_state=self)

            return next
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

        countdown_messages = ["Game starts in " + str(x) + "..." for x in reversed(range(1, config.COUNTDOWN_BEGIN + 1))]
        countdown_messages.append("Begin!")

        self.countdown_messages = [entities.TextSprite(text=x, color=config.SCORE_COLOR) for x in countdown_messages]

        for msg in self._messages:
            center = pygame.Vector2(config.WINDOW_SIZE.width * 0.5 - msg.rect.width * 0.5,
                                    config.WINDOW_SIZE.height * 0.5 - msg.rect.height * 0.5)

            msg.set_position(center)

        # determine which player has the most points, and how many more points they need to win
        # if neither have 11 points:
        #  if at least 2 points away:
        #       need 11 points to win
        #  else
        #       need
        min_points_required = config.MIN_POINTS_TO_WIN_RALLY
        delta_score = abs(self.points[0] - self.points[1])

        if max(self.points) < config.MIN_POINTS_TO_WIN_RALLY:  # neither player has 11 points
            # if both players are within DIFF points, and are within DIFF points needed to win rally,
            # then min points = base points needed + delta score diff

            if delta_score < config.MIN_POINT_DIFFERENCE_TO_WIN:
                min_points_required += delta_score

        else:  # one or both players exceeds the min points, now the greater must only win by diff
            # note: by definition, the players must be within the point diff or else this state
            # would not have been created
            min_points_required += min(delta_score, config.MIN_POINT_DIFFERENCE_TO_WIN)

        player_with_most = self._game.board.left_player if


    @property
    def next_state(self):
        return self._game

    @property
    def finished(self):
        return len(self._messages) == 0

    def update(self, elapsed):
        self._display_time += elapsed

        if self._display_time >= config.DURATION_PER_MESSAGE and len(self.countdown_messages) > 0:
            self.countdown_messages = self.countdown_messages[1:]
            self._display_time -= config.DURATION_PER_MESSAGE

        # allow game to start once we're on last message (which should be "begin")
        if len(self.countdown_messages) <= 1:
            self._game.update(elapsed)

    def draw(self, screen):
        self._game.draw(screen)  # draw board

        if len(self.countdown_messages) > 0:
            current = self.countdown_messages[0]
            screen.blit(source=current.image, dest=current.rect)
