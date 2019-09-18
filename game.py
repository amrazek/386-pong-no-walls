import sys
import config
from pygame.locals import *
from gamestate import GameState, InputState
from helper import *

screen = pygame.display.set_mode(size=config.WINDOW_SIZE, flags=HWSURFACE)
pygame.display.set_caption("Pong No Walls")
pygame.font.init()
config.load_images()

clock = pygame.time.Clock()
input_state = InputState()

board_bounds = pygame.Rect(0, 0, config.WINDOW_SIZE.width, config.WINDOW_SIZE.height)

elapsed_time = 0.0

# create initial game state: this will control each stage of the game
state = GameState.create_initial(input_state)

while not input_state.quit and (state is not None and not state.finished):
    input_state.event_loop()
    state.update(elapsed_time)
    state.draw(screen)
    pygame.display.flip()

    state = state if not state.finished else state.next_state

    # limit FPS to 60, but otherwise execute as quickly as possible
    elapsed_time = clock.tick_busy_loop(60) / 1000.0

pygame.quit()
sys.exit(0)
