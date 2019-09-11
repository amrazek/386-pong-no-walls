import pygame
import sys
from pygame.locals import *
from entities import *
from input import *

window_size = (400, 400)
bkg_color = (0, 0, 0)

screen = pygame.display.set_mode(size=window_size, flags=HWSURFACE)
pygame.display.set_caption("Pong No Walls")
clock = pygame.time.Clock()
input = Input()

pdl_long = 100
pdl_short = 20

board_bounds = pygame.Rect(0, 0, window_size[0], window_size[1])

half_width = window_size[0] * 0.5
half_height = window_size[1] * 0.5


top_horizontal_bounds = pygame.Rect(half_width, 0, half_width, pdl_short)
bottom_horizontal_bounds = top_horizontal_bounds.copy()
bottom_horizontal_bounds.top = window_size[1] - pdl_short

center_vertical_bounds_left = pygame.Rect(0, 0, pdl_short, window_size[1])
center_vertical_bounds_right = center_vertical_bounds_left.copy()
center_vertical_bounds_right.left = window_size[0] - pdl_short

ball = Ball(screen, 10, pygame.color.Color('#FF0000'), pygame.Vector2(100, 0))
player_center = VerticalPaddle((20, 100), 100, center_vertical_bounds_right)
player_top = HorizontalPaddle((100, 20), 100, top_horizontal_bounds)
player_bottom = HorizontalPaddle((100, 20), 100, bottom_horizontal_bounds)

sprites = pygame.sprite.Group(ball)
sprites.add(player_center)
sprites.add(player_top)
sprites.add(player_bottom)

elapsed_time = 0.0

while not input.quit:
    input.event_loop()

    handle_player_input(input, board_bounds, bottom=player_bottom, top=player_top, vertical=player_center)

    # update all sprites
    sprites.update(elapsed_time)

    # render all sprites
    screen.fill(bkg_color)
    sprites.draw(screen)
    pygame.display.flip()

    # limit FPS to 60, but otherwise execute as quickly as possible
    elapsed_time = clock.tick_busy_loop(60) / 1000.0

pygame.quit()
sys.exit(0)