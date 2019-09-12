import pygame
import sys
from pygame.locals import *
from entities import *
from input import *
import controllers
import random

window_size = (800, 400)
bkg_color = (0, 0, 0)
pdl_long = 100
pdl_short = 10
player_color = (255, 242, 0)
computer_color = (255, 0, 0)

screen = pygame.display.set_mode(size=window_size, flags=HWSURFACE)
pygame.display.set_caption("Pong No Walls")
clock = pygame.time.Clock()
input = Input()



board_bounds = pygame.Rect(0, 0, window_size[0], window_size[1])

half_width = window_size[0] * 0.5
half_height = window_size[1] * 0.5


top_horizontal_bounds = pygame.Rect(half_width, 0, half_width - pdl_short, pdl_short)
bottom_horizontal_bounds = top_horizontal_bounds.copy()
bottom_horizontal_bounds.top = window_size[1] - pdl_short

center_vertical_bounds_left = pygame.Rect(0, 0, pdl_short, window_size[1])
center_vertical_bounds_right = center_vertical_bounds_left.copy()
center_vertical_bounds_right.left = window_size[0] - pdl_short

angle = random.uniform(0, 2.0 * 3.14159)
ball_velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * 300

ball = Ball(screen, 10, pygame.color.Color('#FF0000'), ball_velocity)

# player paddles
player_center = Paddle((pdl_short, 100), 400, center_vertical_bounds_right, player_color)
player_top = Paddle((100, pdl_short), 400, top_horizontal_bounds, player_color)
player_bottom = Paddle((100, pdl_short), 400, bottom_horizontal_bounds, player_color)

# computer paddles
top_horizontal_bounds.left = bottom_horizontal_bounds.left = 0

computer_center = Paddle((pdl_short, 100), 400, center_vertical_bounds_left, computer_color)
computer_top = Paddle((100, pdl_short), 400, top_horizontal_bounds, computer_color)
computer_bottom = Paddle((100, pdl_short), 400, bottom_horizontal_bounds, computer_color)

paddles = pygame.sprite.Group()
paddles.add(player_center)
paddles.add(player_top)
paddles.add(player_bottom)

paddles.add(computer_top, computer_bottom, computer_center)

balls = pygame.sprite.Group(ball)

player = controllers.PlayerController(input, player_center, [player_top, player_bottom])
computer = controllers.ComputerController(computer_center, [computer_top, computer_bottom])

elapsed_time = 0.0

while not input.quit:
    input.event_loop()

    player.update()
    computer.update(ball)

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