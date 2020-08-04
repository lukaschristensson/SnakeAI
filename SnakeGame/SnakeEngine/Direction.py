import enum


class Direction(enum.Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    def getVector(self) -> [int, int]:
        if self is Direction.N:
            return [0, -1]
        if self is Direction.E:
            return [1, 0]
        if self is Direction.S:
            return [0, 1]
        if self is Direction.W:
            return [-1, 0]

    def right(self) -> any:
        if self is Direction.N:
            return Direction.E
        if self is Direction.E:
            return Direction.S
        if self is Direction.S:
            return Direction.W
        if self is Direction.W:
            return Direction.N

    def left(self) -> any:
        if self is Direction.N:
            return Direction.W
        if self is Direction.W:
            return Direction.S
        if self is Direction.S:
            return Direction.E
        if self is Direction.E:
            return Direction.N
