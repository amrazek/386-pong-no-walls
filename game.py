import pygame
import sys
from pygame.locals import *
from entities import *
from input import *
import controllers
from helper import *
from board import Board
import collections

window_size = Dimensions(800, 400)
bkg_color = (0, 0, 0)
pdl_long = 100
pdl_short = 10
player_color = (255, 242, 0)
computer_color = (255, 0, 0)

screen = pygame.display.set_mode(size=window_size, flags=HWSURFACE)
pygame.display.set_caption("Pong No Walls")
pygame.font.init()
clock = pygame.time.Clock()
input = Input()

board_bounds = pygame.Rect(0, 0, window_size.width, window_size.height)


class GameState:
    def __init__(self):
        self._left_score = 0
        self._right_score = 0

        self.board = Board(input=input,
                           state=self,
                           size=window_size,
                           left_player_generator=controllers.ComputerController,
                           right_player_generator=controllers.ComputerController)

    @classmethod
    def create(cls):
        return GameState()  # todo: create next state based on current state

    @property
    def next_state(self):
        return None

    def is_finished(self):
        return self.board.get_status() != Board.IN_PROGRESS

    def update(self, elapsed):
        self.board.update(elapsed)

    def draw(self, screen):
        self.board.draw(screen)

    @property
    def points(self):
        return self._left_score, self._right_score


elapsed_time = 0.0

state = GameState.create()

while not input.quit and not state.is_finished():
    input.event_loop()
    state.update(elapsed_time)
    state.draw(screen)
    pygame.display.flip()

    # limit FPS to 60, but otherwise execute as quickly as possible
    elapsed_time = clock.tick_busy_loop(60) / 1000.0

pygame.quit()
sys.exit(0)
