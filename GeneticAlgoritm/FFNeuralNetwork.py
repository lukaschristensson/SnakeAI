import numpy as np
from typing import List


class FFNeuralNetwork:

    def __init__(self):
        self.thetas: List[np.ndarray] = []

    def getSinglePredictionWithActivations(self, inputData: np.ndarray) -> np.ndarray:
        X = np.append(1, inputData.ravel())
        z = [np.zeros((1, 1))]  # ignore the first z
        a = [X]

        # feed hidden layers
        for i in range(len(self.thetas) - 1):
            z.append(self.thetas[i].T.dot(a[i]))
            a.append(self.hiddenActivation(z[i + 1]))
            a[i + 1] = np.append(1, a[i + 1].ravel())

        # feed outputLayer
        z.append(self.thetas[len(self.thetas) - 1].T.dot(a[len(self.thetas) - 1]))
        a.append(self.outputActivation(z[-1]))
        return a

    def getSinglePrediction(self, inputData: np.ndarray) -> np.ndarray:
        X = np.append(1, inputData.ravel())
        z = [np.zeros((1, 1))]  # ignore the first z
        a = [X]

        # feed hidden layers
        for i in range(len(self.thetas) - 1):
            z.append(self.thetas[i].T.dot(a[i]))
            a.append(self.hiddenActivation(z[i + 1]))
            a[i + 1] = np.append(1, a[i + 1].ravel())

        # feed outputLayer
        z.append(self.thetas[len(self.thetas) - 1].T.dot(a[len(self.thetas) - 1]))
        a.append(self.outputActivation(z[-1]))
        return a[-1]

    def copy(self) -> any:
        FFNNcopy = FFNeuralNetwork()
        for t in self.thetas:
            FFNNcopy.thetas.append(t.copy())

    @staticmethod
    def outputActivation(arg) -> any:
        return 1 / (1 + np.exp(-arg))   # sigmoid

    @staticmethod
    def hiddenActivation(arg) -> any:
        return arg * (arg > 0)  # ReLU
