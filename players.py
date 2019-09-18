from entities import MovementDirection


class Player:
    def __init__(self, input_state, vertical_paddle, top_paddle, bottom_paddle):
        self._input_state = input_state
        self._vertical = vertical_paddle
        self._horizontal_paddles = [top_paddle, bottom_paddle]

    def update(self, elapsed, ball):
        pass

    @property
    def name(self):
        return "DefaultPlayer"


class HumanPlayer(Player):
    def __init__(self, input_state, vertical_paddle, top_paddle, bottom_paddle):
        super().__init__(input_state, vertical_paddle, top_paddle, bottom_paddle)

    def update(self, elapsed, ball):
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

    @property
    def name(self):
        return "Player"


class ComputerPlayer(Player):
    def __init__(self, input_state, vertical_paddle, top_paddle, bottom_paddle):
        super().__init__(input_state, vertical_paddle, top_paddle, bottom_paddle)

    def update(self, elapsed, ball):
        ball_pos = ball.get_position()

        # if target is less than this amount, the paddle will overshoot the target position
        # and cause a jittery motion next frame
        min_movement = self._vertical.speed * elapsed

        # handle center paddle
        # decide which direction to move it (or if it should not be moved at all)
        delta_y = ball_pos.y - self._vertical.get_position().y

        if delta_y < 0 and abs(delta_y) > min_movement:
            self._vertical.move(MovementDirection.UP)
        elif delta_y > 0 and abs(delta_y) > min_movement:
            self._vertical.move(MovementDirection.DOWN)
        else:
            self._vertical.move(MovementDirection.STOP)

        # handle horizontal paddles
        delta_x = ball_pos.x - self._horizontal_paddles[0].get_position().x
        min_movement = self._horizontal_paddles[0].speed * elapsed

        if delta_x < 0 and abs(delta_x) > min_movement:
            direction = MovementDirection.LEFT
        elif delta_x > 0 and abs(delta_x > min_movement):
            direction = MovementDirection.RIGHT
        else:
            direction = MovementDirection.STOP

        for h in self._horizontal_paddles:
            h.move(direction)

    @property
    def name(self):
        return "Computer"
