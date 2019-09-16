from entities import *
from input import *
from entities import MovementDirection


class DefaultPlayer:
    def __init__(self, input, vertical_paddle, top_paddle, bottom_paddle):
        self.input = input
        self.vertical = vertical_paddle
        self.horizontal_paddles = [top_paddle, bottom_paddle]

    def update(self, elapsed, ball):
        pass


class PlayerController(DefaultPlayer):
    def __init__(self, input, vertical_paddle, top_paddle, bottom_paddle):
        super().__init__(input, vertical_paddle, top_paddle, bottom_paddle)

    def update(self, elapsed, ball):
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


# if target coordinate is within this fraction of a paddle's size from its
# center, don't move the paddle
DEAD_ZONE_MULTIPLIER = 0.05


class ComputerController(DefaultPlayer):
    def __init__(self, input, vertical_paddle, top_paddle, bottom_paddle):
        super().__init__(input, vertical_paddle, top_paddle, bottom_paddle)

        self.dead_zone_x = self.vertical.rect.width * DEAD_ZONE_MULTIPLIER
        self.dead_zone_y = self.horizontal_paddles[0].rect.height * DEAD_ZONE_MULTIPLIER

        self.dead_zone_x **= 2
        self.dead_zone_y **= 2

    @classmethod
    def _dist_squared(cls, coord1, coord2):
        delta = coord1 - coord2
        return delta ** 2

    def update(self, elapsed, ball):
        vertical_pos = self.vertical.get_position().y
        ball_pos = ball.get_position()

        # handle center paddle
        # decide which direction to move it (or if it should not be moved at all)
        in_dead_zone = ComputerController._dist_squared(vertical_pos, ball_pos.y) < self.dead_zone_y

        if ball_pos.y < vertical_pos and not in_dead_zone:
            self.vertical.move(MovementDirection.UP)
        elif ball_pos.y > vertical_pos and not in_dead_zone:
            self.vertical.move(MovementDirection.DOWN)
        else:
            self.vertical.move(MovementDirection.STOP)

        direction = MovementDirection.UP if self.vertical.get_position().y > ball.get_position().y else MovementDirection.DOWN
        self.vertical.move(direction)

        # handle horizontal paddles
        in_dead_zone = ComputerController._dist_squared(self.horizontal_paddles[0].get_position().x, ball_pos.x) < self.dead_zone_x

        if self.horizontal_paddles[0].get_position().x > ball.get_position().x:
            direction = MovementDirection.LEFT
        else:
            direction = MovementDirection.RIGHT

        direction = direction if not in_dead_zone else MovementDirection.STOP

        for h in self.horizontal_paddles:
            h.move(direction)
