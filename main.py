import neat
import os
import pickle
import threading
from hashlib import md5
from math import log2
from multiprocessing.pool import Pool
from time import time
from datetime import datetime

from board import Board

VERSION = 'v0.0.1'
NUM_THREADS = 16

runID = f'2048run-{md5(str(time()).encode()).hexdigest()}'
generationNum = 0
maxFitness = 0


def tileActivationLevel(val):
    """An "improvement" on the log_2 function that will map each tile to an activation level

    Arguments:
        val {Integer} -- The value of the tile

    Returns:
        [Integer] -- An activation level between 0 and 1
    """
    return log2(val) / 32 if val != 0 else 0


def eval(genomes, config):
    """ Finds the fitness values for a list of genomes

    Arguments:
        genomes {array of (int, genome objects)} -- An array (or other iterable) of genomes to be evaluated
        config {config object} -- The configuration settings for the neural networks
    """
    global NUM_THREADS, generationNum, maxFitness

    # Split the the genomes across the available threads
    threadArgs = [[]] * NUM_THREADS

    currentThreadAssignmentNum = 0
    for genomeID, genome in genomes:
        genome.fitness = 0
        threadArgs[currentThreadAssignmentNum].append((genomeID, genome))
        currentThreadAssignmentNum += 1
        currentThreadAssignmentNum %= NUM_THREADS

    # Start the threads
    with Pool(NUM_THREADS) as p:
        results = p.map(evalThread, threadArgs)

        # Conglomerate the results from all of the threads
        fitnessDictionary = {}

        for d in results:
            fitnessDictionary.update(d)

        # Find the best genome from this generation
        bestGenomeID = max(fitnessDictionary, key=fitnessDictionary.get)

        # Save the fitnesses of all of the genomes for evaluation purposes
        for genomeID, genome in genomes:
            genome.fitness = fitnessDictionary[genomeID]

            # If the best genome in this generation was better than any genome that we've seen before, save it
            if bestGenomeID == genomeID:
                if genome.fitness > maxFitness:
                    genomeFile = open(
                        f'{runID}/gen{generationNum}-{genome.fitness}.gnm', 'ab')
                    pickle.dump(genome, genomeFile)
                    genomeFile.close()
                    maxFitness = genome.fitness

    generationNum += 1


def evalThread(genomes):
    """ Finds the fitnesses of a small collection of genomes

    Arguments:
        args {array of (int, genome objects)} -- An array (or other iterable) of genomes to be evaluated

    Returns:
        dictionary -- A dictionary from genomeID to genome fitness
    """
    fitnessDictionary = {}

    # Work over all the genomes
    for genomeID, genome in genomes:

        # Create a neural network based on the genome
        nn = neat.nn.FeedForwardNetwork.create(genome, config)

        # start a game for the nn to play
        b = Board()
        b.placeTile()
        b.placeTile()

        # Have the nn play the game
        while not b.isGameOver():

            # TODO Find a good set of inputs for this ---v
            tilesUp, scoreUp = b.peek(Board.UP)
            tilesDown, scoreDown = b.peek(Board.DOWN)
            tilesLeft, scoreLeft = b.peek(Board.LEFT)
            tilesRight, scoreRight = b.peek(Board.RIGHT)

            inputs = list(map(tileActivationLevel, tilesUp.flatten()))
            inputs += list(map(tileActivationLevel, tilesDown.flatten()))
            inputs += list(map(tileActivationLevel, tilesLeft.flatten()))
            inputs += list(map(tileActivationLevel, tilesRight.flatten()))
            inputs.append(scoreUp)
            inputs.append(scoreDown)
            inputs.append(scoreLeft)
            inputs.append(scoreRight)
            inputs.append(1)

            output = nn.activate(inputs)
            # TODO Find a good set of inputs for this ---^

            # Find what direction the AI wants to move the tiles
            maxActivation = -1000000000
            for i in range(4):
                if output[i] > maxActivation and b.canMove(i):
                    maxActivation = output[i]

            for i in range(4):
                if output[i] >= maxActivation and b.canMove(i):
                    b.move(i)
                    break

            # Prepare the next turn
            b.placeTile()

        # Mark down this genome's fitness
        fitnessDictionary[genomeID] = int(b.score)

    return fitnessDictionary


if __name__ == '__main__':
    # Create a directory to store all of the generated output
    os.mkdir(runID)

    # Load in the configuration info
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Write some run information to the file
    readme = open(f'{runID}/readme.md', 'w')
    readme.write(f'# 2048 NEAT AI - run {runID}\n')
    readme.write(f'Stared on {time()}, version {VERSION}\n')
    readme.write('\n')
    readme.write(f'- *Population Size*: {p.config.pop_size}\n')
    readme.write(f'- *Max fitness*: {p.config.fitness_threshold}\n')
    readme.write(f'- *Thread Count*: {NUM_THREADS}\n')
    readme.close()

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # just give it a whole lotta parallel threads
    # te = neat.ParallelEvaluator(128, eval)
    winner = p.run(eval)

    # Save the first genome that broke the fitness threshold
    genomeFile = open(f'{runID}final.gnm', 'ab')
    pickle.dump(winner, genomeFile)
    genomeFile.close()
