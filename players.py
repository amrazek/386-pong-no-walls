from entities import MovementDirection


class Player:
    def __init__(self, input_state, vertical_paddle, top_paddle, bottom_paddle):
        self._input_state = input_state
        self._vertical = vertical_paddle
        self._horizontal_paddles = [top_paddle, bottom_paddle]

    def update(self, elapsed, ball):
        pass

    def get_name(self):
        return "DefaultPlayer"


class HumanPlayer(Player):
    def __init__(self, input_state, vertical_paddle, top_paddle, bottom_paddle):
        super().__init__(input_state, vertical_paddle, top_paddle, bottom_paddle)

    def update(self, elapsed, ball):
        move_dir = MovementDirection.STOP

        if self._input_state.left and not self._input_state.right:
            move_dir = MovementDirection.LEFT
        elif self._input_state.right and not self._input_state.left:
            move_dir = MovementDirection.RIGHT
        else:
            move_dir = MovementDirection.STOP

        for p in self._horizontal_paddles:
            p.move(move_dir)

        if self._input_state.up and not self._input_state.down:
            move_dir = MovementDirection.UP
        elif self._input_state.down and not self._input_state.up:
            move_dir = MovementDirection.DOWN
        else:
            move_dir = MovementDirection.STOP

        self._vertical.move(move_dir)

    def get_name(self):
        return "Player"


class ComputerPlayer(Player):
    def __init__(self, input_state, vertical_paddle, top_paddle, bottom_paddle):
        super().__init__(input_state, vertical_paddle, top_paddle, bottom_paddle)

    @classmethod
    def _dist_squared(cls, coord1, coord2):
        delta = coord1 - coord2
        return delta * delta

    def update(self, elapsed, ball):
        vertical_pos = self._vertical.get_position().y
        ball_pos = ball.get_position()

        # handle center paddle
        # decide which direction to move it (or if it should not be moved at all)
        if ball_pos.y < vertical_pos:
            self._vertical.move(MovementDirection.UP)
        elif ball_pos.y > vertical_pos:
            self._vertical.move(MovementDirection.DOWN)
        else:
            self._vertical.move(MovementDirection.STOP)

        # handle horizontal paddles
        if self._horizontal_paddles[0].get_position().x > ball.get_position().x:
            direction = MovementDirection.LEFT
        else:
            direction = MovementDirection.RIGHT

        for h in self._horizontal_paddles:
            h.move(direction)

    def get_name(self):
        return "Computer"
