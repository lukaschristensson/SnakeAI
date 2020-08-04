import SnakeGame.SnakeEngine.Snake as Game
import numpy as np


class GameGenerator:

    def __init__(self, boardSize: [int, int], startingSize: int, maxSteps: int):
        self.maxSteps = maxSteps
        self.startingSize = startingSize
        self.boardSize = boardSize

    def newGame(self) -> Game.Snake:
        return Game.Snake(
            [int(np.floor(self.boardSize[0] / 2)), int(np.floor(self.boardSize[1] / 2))],
            self.boardSize, self.maxSteps, self.startingSize
        )
