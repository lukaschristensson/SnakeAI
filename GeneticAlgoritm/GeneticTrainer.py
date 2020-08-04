import sys
import time
import psutil
import os
import multiprocessing
import typing

import numpy as np

import GeneticAlgoritm.FFNeuralNetwork as Network
import GeneticAlgoritm.NetSnake as NetSnake
import SnakeGame.GameGenerator as GameGenerator
from GeneticAlgoritm.GeneticConfig import *


class GeneticTrainer:

    def __init__(self):
        self.gameGenerator = GameGenerator.GameGenerator(boardSize, startingSize, maxSteps)
        # generate initial population
        self.netSnakes = []
        self.generation = 0
        for i in range(numberOfParents):
            self.netSnakes.append(GeneticTrainer.getRandomSnakeInit(epsilon))
        self.bestFitness = 0
        self.bestSnake = self.netSnakes[0]

    def startTraining(self):
        for s in self.netSnakes:
            s.calcFitness(self.gameGenerator.newGame())
        self.netSnakes.sort(key=NetSnake.NetSnake.getFitness, reverse=True)
        self.bestSnake = self.netSnakes[0]
        self.bestFitness = self.bestSnake.getFitness()
        self.lastBitUsage = 0
        maxBitUsage = 0
        while True:
            startTime = time.time()
            print("Generation ", self.generation, end=": ")

            returnQueue = multiprocessing.Queue()
            p = multiprocessing.Process(target=self.advanceGeneration,
                                        args=(self.netSnakes, returnQueue, self.gameGenerator))
            p.start()
            self.netSnakes = returnQueue.get()
            p.join()
            self.netSnakes.sort(key=NetSnake.NetSnake.getFitness, reverse=True)
            self.bestSnake = self.netSnakes[0]
            self.bestFitness = self.bestSnake.getFitness()
            self.generation += 1
            for s in self.netSnakes:
                s.livesLeft -= 1
            print(str(np.round((time.time() - startTime), 4)) + "s", "::", "Best fitness =", self.bestFitness)

            if False:
                currentUsage = psutil.Process(os.getpid()).memory_info().rss
                if maxBitUsage < currentUsage:
                    maxBitUsage = currentUsage
                print("     mem bits used= ", str(np.floor(currentUsage / 1000000)) + " mb", "::", "max= ",
                      str(np.floor(maxBitUsage / 1000000)) + " mb")

    @staticmethod
    def advanceGeneration(currentPop: typing.List[NetSnake.NetSnake], returnQueue: multiprocessing.Queue,
                          gameGenerator: GameGenerator.GameGenerator):
        totalFitness = 0
        prevPop = []
        for s in currentPop:
            if s.livesLeft >= 0:
                prevPop.append(s)
        for s in prevPop:
            totalFitness += s.fitness
        rng = np.random.default_rng()

        if numberOfParents > len(prevPop):
            for i in range(numberOfParents - len(prevPop)):
                prevPop.append(GeneticTrainer.getRandomSnakeInit(epsilon))
            print("Random snakes added=", numberOfParents - len(prevPop))

        parents = []
        for i in range(numberOfParents):
            rand = rng.random() * totalFitness
            fitnessCursor = prevPop[0].fitness
            indexCursor = 0
            while fitnessCursor < rand:
                fitnessCursor += rand
                indexCursor += 1
            winner = prevPop[indexCursor]
            parents.append(winner)
            totalFitness -= winner.fitness
            prevPop.remove(winner)
        np.random.shuffle(parents)
        outPop = []
        for s in parents:
            outPop.append(s)
        for i in range(int(np.round(childrenPerParent / 2))):
            for j in range(len(parents)):
                p1 = parents[j]
                p2 = parents[j - 1]
                children = p1.crossover(p2)
                outPop.append(children[0])
                outPop.append(children[1])

        for s in outPop:
            s.calcFitness(gameGenerator.newGame())
        returnQueue.put(outPop)

    @staticmethod
    def getRandomSnakeInit(epsilon) -> NetSnake.NetSnake:
        s = NetSnake.NetSnake()
        sBrain = Network.FFNeuralNetwork()
        for j in range(len(topology) - 1):
            t = np.random.random((topology[j] + 1, topology[j + 1]))
            t *= 2
            t = np.subtract(t, 1)
            t *= epsilon
            sBrain.thetas.append(t)
        s.net = sBrain
        return s
