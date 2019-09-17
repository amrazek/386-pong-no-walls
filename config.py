from helper import Dimensions
from pygame import Color
import pygame

WINDOW_SIZE = Dimensions(800, 400)
BACKGROUND_COLOR = Color('#000000')
BALL_COLOR = Color('#FF0000')
SCORE_COLOR = Color('#FFFFFF')

PADDLE_LENGTH = 100  # paddle dimensions const for now, need to alter image loading
PADDLE_THICKNESS = 10

PADDLE_SPEED = 400.0

BALL_RADIUS = 10
BALL_SPEED = 100.0

NET_DASH_LENGTH = 30
NET_WIDTH = 2

COUNTDOWN_BEGIN = 3
DURATION_PER_MESSAGE = 0.5  # in seconds

VERTICAL_PADDLE_SURFACE = None
HORIZONTAL_PADDLE_SURFACE = None


def load_images():
    base_image = pygame.image.load("images/paddle.png")

    # construct vertical and horizontal paddles using appropriate dimensions and
    # this base image

    # first construct a horizontal paddle
    global HORIZONTAL_PADDLE_SURFACE
    HORIZONTAL_PADDLE_SURFACE = pygame.transform.smoothscale(base_image, (PADDLE_LENGTH, PADDLE_THICKNESS))
    HORIZONTAL_PADDLE_SURFACE = HORIZONTAL_PADDLE_SURFACE.convert()

    # now vertical paddle, with dimensions flipped
    global VERTICAL_PADDLE_SURFACE
    VERTICAL_PADDLE_SURFACE = pygame.transform.smoothscale(base_image, (PADDLE_THICKNESS, PADDLE_LENGTH))
    VERTICAL_PADDLE_SURFACE = VERTICAL_PADDLE_SURFACE.convert()
