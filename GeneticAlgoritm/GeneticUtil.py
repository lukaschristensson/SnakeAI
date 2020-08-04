import numpy as np
from GeneticAlgoritm.GeneticConfig import *


def singlePointBinaryCrossover(p1: np.ndarray, p2: np.ndarray) -> [np.ndarray, np.ndarray]:
    index = int(np.floor(np.random.default_rng().random() * p1.size))

    c1 = np.append(p1.ravel()[:index], p2.ravel()[index:])
    c2 = np.append(p2.ravel()[:index], p1.ravel()[index:])

    c1 = c1.reshape(p1.shape)
    c2 = c2.reshape(p1.shape)
    if p1.shape != p2.shape:
        print(p1.shape, ":::", p2.shape)
    gaussianMutation(c1)
    gaussianMutation(c2)

    return c1, c2


def simulatedBinaryCrossover(p1: np.ndarray, p2: np.ndarray) -> [np.ndarray, np.ndarray]:
    rand = np.random.random(p1.shape)
    beta = np.empty(p1.shape)

    beta[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1 / (eta + 1))
    beta[rand > 0.5] = (2 * rand[rand > 0.5]) ** (1 / (eta + 1))

    c1 = 0.5 * ((1 + beta) * p1 + (1 - beta) * p2)
    c2 = 0.5 * ((1 - beta) * p1 + (1 + beta) * p2)
    gaussianMutation(c1)
    gaussianMutation(c2)
    return [c1, c2]


def gaussianMutation(theta: np.ndarray):
    mutatedGenes = np.random.random(theta.shape) < mutationRate  # choose which genes to mutate, puts 0 in all but the chosen ones which gets a 1
    mutation = np.random.normal() * mutationScale  # SD around (0, 1), scaled to the mutationScale
    mutatedGenes = mutatedGenes * mutation
    theta += mutatedGenes
