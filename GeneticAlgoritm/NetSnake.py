import GeneticAlgoritm.FFNeuralNetwork as Network
import SnakeGame.SnakeEngine.Direction as Direction
import SnakeGame.SnakeEngine.SnakeController as SnakeController
import GeneticAlgoritm.GeneticUtil as gu
from GeneticAlgoritm.GeneticConfig import *
import numpy as np
import typing


class NetSnake(SnakeController.SnakeController):

    def __init__(self):
        self.net: Network.FFNeuralNetwork
        self.fitness = 0
        self.livesLeft = livesPerSnake

    def calcFitness(self, snakeGame):
        snakeGame.currentDirection = self.getMove(snakeGame)
        while snakeGame.move()[0]:
            snakeGame.currentDirection = self.getMove(snakeGame)
        apples = (len(snakeGame.tail) + 1) - snakeGame.startingSize
        steps = snakeGame.stepsTaken
        self.fitness = steps + (2 ** apples) + (apples ** 2.1) * 500 - (apples ** 1.2) * (0.25 * steps) ** 1.3

    def getFitness(self):
        return self.fitness

    tailDirection = -1

    # also returns the activation in layers, only used to visualize the net
    def getMoveAndActivation(self, snakeGame) -> (Direction.Direction, any):
        appleRays = [0] * 8
        wallRays = [0] * 8
        tailRays = [0] * 8

        rays = NetSnake.getRays(snakeGame)
        for i in range(len(rays)):
            if rays[i][1] == "WALL":
                wallRays[i] = rays[i][0]
            elif rays[i][1] == "TAIL":
                tailRays[i] = rays[i][0]
            elif rays[i][1] == "APPLE":
                appleRays[i] = rays[i][0]
            else:
                print("RAY TAG NOT RECOGNIZED: ", rays[i][1])

        oneHotDirectionVec = [0] * 4
        oneHotDirectionVec[snakeGame.currentDirection.value] = 1

        oneHotTailDirectionVec = [0] * 4
        if isinstance(self.tailDirection, Direction.Direction):
            oneHotTailDirectionVec[self.tailDirection.value] = 1

        finalizedVector = appleRays + wallRays + tailRays + oneHotDirectionVec + oneHotTailDirectionVec
        activations = self.net.getSinglePredictionWithActivations(np.asarray(finalizedVector, dtype=float))
        pred = activations[-1].tolist()
        self.tailDirection = snakeGame.currentDirection.right().right()
        return Direction.Direction(pred.index(max(pred))), activations


    def getMove(self, snakeGame) -> Direction.Direction:
        appleRays = [0] * 8
        wallRays = [0] * 8
        tailRays = [0] * 8

        rays = NetSnake.getRays(snakeGame)
        for i in range(len(rays)):
            if rays[i][1] == "WALL":
                wallRays[i] = rays[i][0]
            elif rays[i][1] == "TAIL":
                tailRays[i] = rays[i][0]
            elif rays[i][1] == "APPLE":
                appleRays[i] = rays[i][0]
            else:
                print("RAY TAG NOT RECOGNIZED: ", rays[i][1])

        oneHotDirectionVec = [0] * 4
        oneHotDirectionVec[snakeGame.currentDirection.value] = 1

        oneHotTailDirectionVec = [0] * 4
        if isinstance(self.tailDirection, Direction.Direction):
            oneHotTailDirectionVec[self.tailDirection.value] = 1

        finalizedVector = appleRays + wallRays + tailRays + oneHotDirectionVec + oneHotTailDirectionVec
        pred = self.net.getSinglePrediction(np.asarray(finalizedVector, dtype=float)).tolist()
        self.tailDirection = snakeGame.currentDirection.right().right()
        return Direction.Direction(pred.index(max(pred)))

    """""
    shoots 8 evenly spread rays clockwise, North being the first, and returns a list of distances and 
    tags for ["APPLE", "WALL", "SNAKE"] corresponding to the first object hit
    
    snakeGame is the snake game in which the rays are shot
    """""

    def crossover(self, p2) -> any:
        brain1 = Network.FFNeuralNetwork()
        brain2 = Network.FFNeuralNetwork()
        for i in range(len(self.net.thetas)):
            if np.random.default_rng().random() < spbxChance:
                res = gu.singlePointBinaryCrossover(self.net.thetas[i], p2.net.thetas[i])
            else:
                res = gu.simulatedBinaryCrossover(self.net.thetas[i], p2.net.thetas[i])
            brain1.thetas.append(res[0])
            brain2.thetas.append(res[1])

        c1 = NetSnake()
        c1.net = brain1
        c2 = NetSnake()
        c2.net = brain2
        return [c1, c2]

    @staticmethod
    def getRays(snakeGame) -> typing.List[typing.Tuple[float, str]]:
        vectors = [[0, -1],
                   [1, -1],
                   [1, 0],
                   [1, 1],
                   [0, 1],
                   [-1, 1],
                   [-1, 0],
                   [-1, -1]
                   ]
        outRays: typing.List[(float, str)] = []
        for vec in vectors:
            tileCursor = snakeGame.head
            nonFound = True
            while nonFound:
                tileCursor = [tileCursor[0] + vec[0], tileCursor[1] + vec[1]]
                if tileCursor in snakeGame.tail:
                    outRays.append((NetSnake.distance(snakeGame.head, tileCursor), "TAIL"))
                    nonFound = False
                elif not (
                        0 <= tileCursor[0] < snakeGame.boardSize[0] and
                        0 <= tileCursor[1] < snakeGame.boardSize[1]
                ):
                    outRays.append((NetSnake.distance(snakeGame.head, tileCursor), "WALL"))
                    nonFound = False
                elif tileCursor == snakeGame.apple:
                    outRays.append((NetSnake.distance(snakeGame.head, tileCursor), "APPLE"))
                    nonFound = False
        return outRays

    @staticmethod
    def distance(p1: [int, int], p2: [int, int]) -> float:
        deltaX = p1[0] - p2[0]
        deltaY = p1[1] - p2[1]
        return np.sqrt(deltaX ** 2 + deltaY ** 2)
