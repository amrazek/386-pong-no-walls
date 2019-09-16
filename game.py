import pygame
import sys
from pygame.locals import *
from entities import *
from input import *
import controllers
from helper import *
from board import Board
import collections

# import random

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
        self.board = Board(input=input,
                           size=window_size,
                           left_player_generator=controllers.ComputerController,
                           right_player_generator=controllers.DefaultPlayer)

    @classmethod
    def create(cls):
        return GameState()

    def next_state(self):
        return None

    def is_finished(self):
        return self.board.get_status() != Board.IN_PROGRESS

    def update(self, elapsed):
        self.board.update(elapsed)

    def draw(self, screen):
        self.board.draw(screen)


elapsed_time = 0.0

state = GameState.create()

while not input.quit and not state.is_finished():
    input.event_loop()
    state.update(elapsed_time)

    state.draw(screen)
    pygame.display.flip()

    # player.update()
    # computer.update(ball)
    # computer_right.update(ball)  # temp: have computer play itself

    # update all sprites
    # paddles.update(elapsed_time)
    # balls.update(paddles, elapsed_time)
    # decoration.update(elapsed_time)

    # render all sprites
    # screen.fill(bkg_color)
    # decoration.draw(screen)
    # paddles.draw(screen)
    # balls.draw(screen)
    # scores.draw(screen)
    # pygame.display.flip()

    # limit FPS to 60, but otherwise execute as quickly as possible
    elapsed_time = clock.tick_busy_loop(60) / 1000.0

pygame.quit()
sys.exit(0)
