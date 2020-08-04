from SnakeGame.SnakeEngine.Direction import Direction
import numpy as np


class Snake:

    def __init__(self, pos: [int, int], boardSize: [int, int], maxSteps: int, startingSize: int):
        self.length: int = 1
        self.maxSteps = maxSteps
        self.stepsTaken = 0
        self.stepsSinceApple = 0
        self.boardSize: [int, int] = boardSize
        self.head: [int, int] = pos
        self.tail: [[int, int]] = []
        self.currentDirection: Direction = Direction.N
        self.apple: [int, int]
        self.startingSize = startingSize
        for i in range(startingSize - 1):
            self.addTail()
        self.generateApple()

    def move(self) -> (bool, str):
        moveVec = self.currentDirection.getVector()
        for i in reversed(range(self.length - 1)):
            self.tail[i] = self.tail[i - 1]
        if self.length > 1:
            self.tail[0] = self.head
        self.head = [self.head[0] + moveVec[0], self.head[1] + moveVec[1]]
        self.stepsTaken += 1
        self.stepsSinceApple += 1
        return self.applyRules()

    def applyRules(self) -> (bool, str):
        # check border collision
        if not (
            0 <= self.head[0] < self.boardSize[0] and
            0 <= self.head[1] < self.boardSize[1]
        ):
            return False, "Hit a wall"
        #  check self collision
        if self.head in self.tail:
            return False, "Hit itself"
        # check if it starved
        if self.stepsSinceApple > self.maxSteps:
            return False, "Starved"
        # check if it caught an apple
        if self.apple == self.head:
            self.addTail()
            self.stepsSinceApple = 0
            self.generateApple()
        return True, ""

    def addTail(self):
        self.tail.append([-2, -2])
        self.length += 1

    def generateApple(self):
        possiblePositions: [[int, int]] = []
        for i in range(self.boardSize[0]):
            for j in range(self.boardSize[1]):
                if not ([i, j] in self.tail or [i, j] == self.head):
                    possiblePositions.append([i, j])

        self.apple = possiblePositions[int(np.floor(len(possiblePositions) * np.random.default_rng().random()))]
