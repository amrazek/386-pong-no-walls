from entities import *
import input

class PlayerController:
    def __init__(self, input, vertical_paddle, horizontal_paddles):
        self.input = input
        self.vertical = vertical_paddle
        self.horizontal_paddles = horizontal_paddles

    def update(self):
        move_dir = MovementDirection.STOP

        if self.input.left and not self.input.right:
            move_dir = MovementDirection.LEFT
        elif self.input.right and not self.input.left:
            move_dir = MovementDirection.RIGHT
        else:
            move_dir = MovementDirection.STOP

        for p in self.horizontal_paddles:
            p.move(move_dir)

        move_dir = MovementDirection.STOP

        if self.input.up and not self.input.down:
            move_dir = MovementDirection.UP
        elif self.input.down and not self.input.up:
            move_dir = MovementDirection.DOWN
        else:
            move_dir = MovementDirection.STOP

        self.vertical.move(move_dir)