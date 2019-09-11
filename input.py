import pygame
from pygame.locals import *

class Input:
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
                state = True if evt.type == KEYDOWN else False

                if evt.key == K_LEFT:
                    self.left = state
                elif evt.key == K_RIGHT:
                    self.right = state
                elif evt.key == K_UP:
                    self.up = state
                elif evt.key == K_DOWN:
                    self.down = state


def handle_player_input(input, board_bounds, vertical, top, bottom):
    if (input.left and input.right) or not input.left and not input.right:
        top.move_to(top.get_position())
        bottom.move_to(bottom.get_position())
    elif input.left:
        top.move_to(board_bounds.left)
        bottom.move_to(board_bounds.left)
    else:
        top.move_to(board_bounds.right)
        bottom.move_to(board_bounds.right)

    if (input.up and input.down) or (not input.up and not input.down):
        vertical.move_to(vertical.get_position())
    elif input.up:
        vertical.move_to(board_bounds.top)
    else:
        vertical.move_to(board_bounds.bottom)