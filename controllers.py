from entities import *
import input
from entities import MovementDirection

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


class ComputerController:
    def __init__(self, vertical_paddle, horizontal_paddles):
        self.vertical = vertical_paddle
        self.horizontal_paddles = horizontal_paddles

    def update(self, ball):
        vertical_pos = self.vertical.get_position().y
        ball_pos = ball.get_position()

        if ball_pos.y < vertical_pos:
            self.vertical.move(MovementDirection.UP)
        elif ball_pos.y > vertical_pos:
            self.vertical.move(MovementDirection.DOWN)
        else:
            self.vertical.move(MovementDirection.STOP)

        direction = MovementDirection.UP if self.vertical.get_position().y > ball.get_position().y else MovementDirection.DOWN
        self.vertical.move(direction)

        go_left = self.horizontal_paddles[0].get_position().x > ball.get_position().x

        for h in self.horizontal_paddles:
            h.move(MovementDirection.LEFT if go_left else MovementDirection.RIGHT)
