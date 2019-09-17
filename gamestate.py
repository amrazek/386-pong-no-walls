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
    def __init__(self, input_state):
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


# this is actual "in game" play and runs until the ball goes out of bounds
class PlayGame(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)

        self.board = Board(input_state=input_state,
                           state=self,
                           size=config.WINDOW_SIZE,
                           left_player_generator=players.ComputerPlayer,
                           right_player_generator=players.ComputerPlayer)

    def next_state(self):
        pass

    @property
    def finished(self):
        return self.board.get_status() != Board.IN_PROGRESS

    def update(self, elapsed):
        self.board.update(elapsed)

    def draw(self, screen):
        self.board.draw(screen)

    @property
    def points(self):
        return self._left_score, self._right_score


# this state displays a countdown before game begins
class BeginGame(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)
        self._game = PlayGame(input_state)
        self._display_time = 0

        messages = ["Game starts in " + str(x) + "..." for x in reversed(range(1, config.COUNTDOWN_BEGIN + 1))]
        messages.append("Begin!")

        self._messages = [entities.TextSprite(text=x, color=config.SCORE_COLOR) for x in messages]

        for msg in self._messages:
            center = pygame.Vector2(config.WINDOW_SIZE.width * 0.5 - msg.rect.width * 0.5,
                                    config.WINDOW_SIZE.height * 0.5 - msg.rect.height * 0.5)

            msg.set_position(center)

    @property
    def next_state(self):
        return self._game

    @property
    def finished(self):
        return len(self._messages) == 0

    def update(self, elapsed):
        self._display_time += elapsed

        if self._display_time >= config.DURATION_PER_MESSAGE and len(self._messages) > 0:
            self._messages = self._messages[1:]
            self._display_time -= config.DURATION_PER_MESSAGE

        # allow game to start once we're on last message (which should be "begin")
        if len(self._messages) <= 1:
            self._game.update(elapsed)

    def draw(self, screen):
        self._game.draw(screen)  # draw board

        if len(self._messages) > 0:
            current = self._messages[0]
            screen.blit(source=current.image, dest=current.rect)
