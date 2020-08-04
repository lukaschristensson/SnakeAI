import SnakeGame.SnakeEngine.SnakeController as SnakeController
import SnakeGame.SnakeEngine.Snake as SnakeGame
from SnakeGame.SnakeEngine.Direction import Direction


class DebugController(SnakeController.SnakeController):
    flipFlop = False

    def getMove(self, snakeGame: SnakeGame) -> Direction:
        self.flipFlop = not self.flipFlop
        if self.flipFlop:
            return snakeGame.currentDirection
        else:
            return snakeGame.currentDirection.left()
