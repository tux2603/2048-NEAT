from board import Board
from math import log2
import neat
import threading
from multiprocessing.pool import Pool
from time import time
from hashlib import md5
import pickle

NUM_THREADS = 8
runID = '0'
generationNum = 0
maxFitness = 0

def smartLog2(val):
    return log2(val) if val != 0 else 0

def eval(genomes, config):
    global NUM_THREADS, generationNum, maxFitness

    threadArgs = [[]] * NUM_THREADS

    currentThreadAssignmentNum = 0
    for genomeID, genome in genomes:
        genome.fitness = 0
        threadArgs[currentThreadAssignmentNum].append((genomeID, genome))
        currentThreadAssignmentNum += 1
        currentThreadAssignmentNum %= NUM_THREADS

    threads = []

    with Pool(NUM_THREADS) as p:
        results = p.map(evalThread, threadArgs)

        fitnessDictionary = {}

        for d in results:
            fitnessDictionary.update(d)

        bestGenomeID = max(fitnessDictionary, key=fitnessDictionary.get)

        for genomeID, genome in genomes:
            genome.fitness = fitnessDictionary[genomeID]
            if bestGenomeID == genomeID:
                if genome.fitness > maxFitness:
                    genomeFile = open(f'{runID}gen{generationNum}.gnm', 'ab') 
                    pickle.dump(genome, genomeFile)                      
                    genomeFile.close() 
                    maxFitness = genome.fitness

    generationNum += 1


def evalThread(args):
    fitnessDictionary = {}

    for genomeID, genome in args:
        nn = neat.nn.FeedForwardNetwork.create(genome, config)

        b = Board()
        b.placeTile()
        b.placeTile()

        while not b.isGameOver():
            inputs = list(map(smartLog2, b.tiles.flatten()))
            inputs.append(1)

            output = nn.activate(inputs)

            maxActivation = -1000000000
            for i in range(4):
                if output[i] > maxActivation and b.canMove(i):
                    maxActivation = output[i]

            for i in range(4):
                if output[i] >= maxActivation and b.canMove(i):
                    b.move(i)
                    break

            b.placeTile()
        fitnessDictionary[genomeID] = int(b.score)

    return fitnessDictionary
    
if __name__ == '__main__':
    runID = md5(str(time()).encode()).hexdigest()
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        'config')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # just give it a whole lotta parallel threads
    # te = neat.ParallelEvaluator(128, eval)
    winner = p.run(eval)

    genomeFile = open(f'{runID}final.gnm', 'ab') 
    pickle.dump(winner, genomeFile)                      
    genomeFile.close()