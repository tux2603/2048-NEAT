from board import Board
from math import log2
import neat

def smartLog2(val):
    return log2(val) if val != 0 else 0

def eval(genome, config):
    b = Board()
    b.placeTile()
    b.placeTile()

    nn = neat.nn.FeedForwardNetwork.create(genome, config)

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

    return int(b.score)
    
if __name__ == '__main__':
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        'config')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # just give it a whole lotta parallel threads
    te = neat.ParallelEvaluator(128, eval)
    winner = p.run(te.evaluate)