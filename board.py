import pygame
import collections


class Board:
    BACKGROUND_COLOR = pygame.Color('#000000')

    def __init__(self, size):
        assert size.width > 0 and size.height > 0

        self._bounds = pygame.Rect(0, 0, size.width, size.height)
        self._background = Board.BACKGROUND_COLOR

    def update(self, elapsed):
        pass

    def draw(self, screen):
        screen.fill(self._background)