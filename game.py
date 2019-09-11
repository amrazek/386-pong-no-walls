import pygame
import sys
from pygame.locals import *
from entities import *
from input import *
import controllers

window_size = (800, 400)
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


top_horizontal_bounds = pygame.Rect(half_width, 0, half_width - pdl_short, pdl_short)
bottom_horizontal_bounds = top_horizontal_bounds.copy()
bottom_horizontal_bounds.top = window_size[1] - pdl_short

center_vertical_bounds_left = pygame.Rect(0, 0, pdl_short, window_size[1])
center_vertical_bounds_right = center_vertical_bounds_left.copy()
center_vertical_bounds_right.left = window_size[0] - pdl_short

ball = Ball(screen, 10, pygame.color.Color('#FF0000'), pygame.Vector2(400, 0))
player_center = Paddle((20, 100), 400, center_vertical_bounds_right)
player_top = Paddle((100, 20), 400, top_horizontal_bounds)
player_bottom = Paddle((100, 20), 400, bottom_horizontal_bounds)

paddles = pygame.sprite.Group()
paddles.add(player_center)
paddles.add(player_top)
paddles.add(player_bottom)

balls = pygame.sprite.Group(ball)

player = controllers.PlayerController(input, player_center, [player_top, player_bottom])

elapsed_time = 0.0

while not input.quit:
    input.event_loop()

    #handle_player_input(input, bottom=player_bottom, top=player_top, vertical=player_center)
    player.update()

    # update all sprites
    paddles.update(elapsed_time)
    balls.update(paddles, elapsed_time)

    # render all sprites
    screen.fill(bkg_color)
    paddles.draw(screen)
    balls.draw(screen)
    pygame.display.flip()

    # limit FPS to 60, but otherwise execute as quickly as possible
    elapsed_time = clock.tick_busy_loop(60) / 1000.0

pygame.quit()
sys.exit(0)