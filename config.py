import os
from helper import Dimensions
from pygame import Color
import pygame

WINDOW_SIZE = Dimensions(800, 400)
BACKGROUND_COLOR = Color('#000000')
SCORE_COLOR = Color('#FFFFFF')

PADDLE_LENGTH = 100  # paddle dimensions const for now, need to alter image loading
PADDLE_THICKNESS = 8

PADDLE_SPEED = 400.0
PADDLE_BALL_VELOCITY_MODIFIER = 1.75  # this multiplies the velocity bonus ball gets from a moving paddle

BALL_RADIUS = 10
BALL_MIN_SPEED = 300.0
BALL_MAX_SPEED = 500.0

NET_DASH_LENGTH = 15
NET_WIDTH = 2

COUNTDOWN_BEGIN = 3
DURATION_PER_MESSAGE = 1  # in seconds for countdown messages
DURATION_PER_GAME_VICTORY_MESSAGE = 1.0  # in seconds
DURATION_VICTORY_SLIDE = 2  # in seconds, how long it takes to slide view in victory screen

VERTICAL_PADDLE_SURFACE = None
HORIZONTAL_PADDLE_SURFACE = None
BALL_SURFACE = None

NUMBER_GAMES_REQUIRED_VICTORY = 3  # player must win this many games in a set for victory
MIN_POINTS_TO_WIN_GAME = 11  # player must have at least this many points to win a rally
MIN_POINT_DIFFERENCE_TO_WIN = 2  # winner must have at least this many more points than loser to win a rally

PADDLE_BOUNCE_SOUNDS = []
VICTORY_SHORT = None
FAILURE_SHORT = None
VICTORY_LONG = None
FAILURE_LONG = None


def load_images():
    base_paddle_image = pygame.image.load(os.path.join("images", "paddle.png"))
    base_ball_image = pygame.image.load(os.path.join("images", "ball.png"))

    # construct vertical and horizontal paddles using appropriate dimensions and
    # this base image

    # first construct a horizontal paddle
    global HORIZONTAL_PADDLE_SURFACE
    HORIZONTAL_PADDLE_SURFACE = pygame.transform.smoothscale(base_paddle_image, (PADDLE_LENGTH, PADDLE_THICKNESS))
    HORIZONTAL_PADDLE_SURFACE = HORIZONTAL_PADDLE_SURFACE.convert()

    # now vertical paddle, with dimensions flipped
    global VERTICAL_PADDLE_SURFACE
    VERTICAL_PADDLE_SURFACE = pygame.transform.smoothscale(base_paddle_image, (PADDLE_THICKNESS, PADDLE_LENGTH))
    VERTICAL_PADDLE_SURFACE = VERTICAL_PADDLE_SURFACE.convert()

    # generate ball surface
    # note that it needs a color key (if it does not have an alpha channel)
    global BALL_SURFACE
    BALL_SURFACE = pygame.transform.smoothscale(base_ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
    mask_color = (0, 0, 0)
    BALL_SURFACE.set_colorkey(mask_color)

    BALL_SURFACE = BALL_SURFACE.convert_alpha()


def load_sounds():
    global PADDLE_BOUNCE_SOUNDS
    global VICTORY_SHORT
    global VICTORY_LONG
    global FAILURE_SHORT
    global FAILURE_LONG

    if pygame.mixer:
        pygame.mixer.init()

        for sound_name in ["blip" + str(i) + ".wav" for i in range(1, 6)]:
            sound = load_sound(sound_name)

            if sound is not None:
                PADDLE_BOUNCE_SOUNDS.append(sound)

        pygame.mixer.music.load(os.path.join("sounds", "your-call-by-kevin-macleod.mp3"))
        pygame.mixer.music.play(-1, 0)

        VICTORY_SHORT = load_sound("win sound 1-2.wav")
        VICTORY_LONG = load_sound("Fanfare 02.ogg")
        FAILURE_SHORT = load_sound("lose.wav")
        FAILURE_LONG = load_sound("GameOver.ogg")


def load_sound(file_name):
    path = os.path.join("sounds", file_name)

    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print("failed to load sound: ", path)

    return None
