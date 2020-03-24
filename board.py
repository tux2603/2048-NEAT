import numpy as np
import random


class Board():
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self):
        self.score = 0
        # If the computer gets good enough to excede 32 bit integers, that's good enough for me
        self.tiles = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]], np.int32)

    def canMove(self, direction):

        if direction == Board.UP:
            for col in range(4):
                tile = 0
                for row in range(4):
                    if tile != 0 and self.tiles[col][row] in (tile, 0):
                        return True
                    tile = self.tiles[col][row] if self.tiles[col][row] != 0 else tile

        elif direction == Board.DOWN:
            for col in range(4):
                tile = 0
                for row in range(3, -1, -1):
                    if tile != 0 and self.tiles[col][row] in (tile, 0):
                        return True
                    tile = self.tiles[col][row] if self.tiles[col][row] != 0 else tile

        elif direction == Board.LEFT:
            for row in range(4):
                tile = 0
                for col in range(3, -1, -1):
                    if tile != 0 and self.tiles[col][row] in (tile, 0):
                        return True
                    tile = self.tiles[col][row] if self.tiles[col][row] != 0 else tile

        elif direction == Board.RIGHT:
            for row in range(4):
                tile = 0
                for col in range(4):
                    if tile != 0 and self.tiles[col][row] in (tile, 0):
                        return True
                    tile = self.tiles[col][row] if self.tiles[col][row] != 0 else tile

        return False

    def move(self, direction):
        if direction == Board.UP:
            for col in range(4):
                for row in range(3, 0, -1):
                    for search in range(row-1, -1, -1):
                        if self.tiles[col][row] == 0:
                            self.tiles[col][row] = self.tiles[col][search]
                            self.tiles[col][search] = 0
                        elif self.tiles[col][row] == self.tiles[col][search]:
                            self.tiles[col][row] *= 2
                            self.score += self.tiles[col][row]
                            self.tiles[col][search] = 0
                            break
                        elif self.tiles[col][search] != 0:
                            break

        elif direction == Board.DOWN:
            for col in range(4):
                for row in range(3):
                    for search in range(row+1, 4):
                        if self.tiles[col][row] == 0:
                            self.tiles[col][row] = self.tiles[col][search]
                            self.tiles[col][search] = 0
                        elif self.tiles[col][row] == self.tiles[col][search]:
                            self.tiles[col][row] *= 2
                            self.score += self.tiles[col][row]
                            self.tiles[col][search] = 0
                            break
                        elif self.tiles[col][search] != 0:
                            break

        elif direction == Board.LEFT:
            for row in range(4):
                for col in range(3):
                    for search in range(col+1, 4):
                        if self.tiles[col][row] == 0:
                            self.tiles[col][row] = self.tiles[search][row]
                            self.tiles[search][row] = 0
                        elif self.tiles[col][row] == self.tiles[search][row]:
                            self.tiles[col][row] *= 2
                            self.score += self.tiles[col][row]
                            self.tiles[search][row] = 0
                            break
                        elif self.tiles[search][row] != 0:
                            break

        elif direction == Board.RIGHT:
            for row in range(4):
                for col in range(3, 0, -1):
                    for search in range(col-1, -1, -1):
                        if self.tiles[col][row] == 0:
                            self.tiles[col][row] = self.tiles[search][row]
                            self.tiles[search][row] = 0
                        elif self.tiles[col][row] == self.tiles[search][row]:
                            self.tiles[col][row] *= 2
                            self.score += self.tiles[col][row]
                            self.tiles[search][row] = 0
                            break
                        elif self.tiles[search][row] != 0:
                            break

    def peak(self, direction):
        tiles = self.tiles.copy()

        if direction == Board.UP:
            for col in range(4):
                for row in range(3, 0, -1):
                    for search in range(row-1, -1, -1):
                        if tiles[col][row] == 0:
                            tiles[col][row] = tiles[col][search]
                            tiles[col][search] = 0
                        elif tiles[col][row] == tiles[col][search]:
                            tiles[col][row] *= 2
                            tiles[col][search] = 0
                            break
                        elif tiles[col][search] != 0:
                            break

        elif direction == Board.DOWN:
            for col in range(4):
                for row in range(3):
                    for search in range(row+1, 4):
                        if tiles[col][row] == 0:
                            tiles[col][row] = tiles[col][search]
                            tiles[col][search] = 0
                        elif tiles[col][row] == tiles[col][search]:
                            tiles[col][row] *= 2
                            tiles[col][search] = 0
                            break
                        elif tiles[col][search] != 0:
                            break

        elif direction == Board.LEFT:
            for row in range(4):
                for col in range(3):
                    for search in range(col+1, 4):
                        if tiles[col][row] == 0:
                            tiles[col][row] = tiles[search][row]
                            tiles[search][row] = 0
                        elif tiles[col][row] == tiles[search][row]:
                            tiles[col][row] *= 2
                            tiles[search][row] = 0
                            break
                        elif tiles[search][row] != 0:
                            break

        elif direction == Board.RIGHT:
            for row in range(4):
                for col in range(3, 0, -1):
                    for search in range(col-1, -1, -1):
                        if tiles[col][row] == 0:
                            tiles[col][row] = tiles[search][row]
                            tiles[search][row] = 0
                        elif tiles[col][row] == tiles[search][row]:
                            tiles[col][row] *= 2
                            tiles[search][row] = 0
                            break
                        elif tiles[search][row] != 0:
                            break

    def placeTile(self):
        validSquares = []

        for col in range(4):
            for row in range(4):
                if self.tiles[col][row] == 0:
                    validSquares.append((col, row))

        # Game is over when no more squares can be placed
        if len(validSquares) == 0:
            return False

        s = random.choice(validSquares)
        self.tiles[s[0]][s[1]] = 2 if random.random() < 0.9 else 4

    def isGameOver(self):
        return not (self.canMove(Board.UP) or self.canMove(Board.DOWN) or self.canMove(Board.LEFT) or self.canMove(Board.RIGHT))

    def __str__(self):
        return f'{self.tiles[0][3]} {self.tiles[1][3]} {self.tiles[2][3]} {self.tiles[3][3]} \n' +\
            f'{self.tiles[0][2]} {self.tiles[1][2]} {self.tiles[2][2]} {self.tiles[3][2]} \n' +\
            f'{self.tiles[0][1]} {self.tiles[1][1]} {self.tiles[2][1]} {self.tiles[3][1]} \n' +\
            f'{self.tiles[0][0]} {self.tiles[1][0]} {self.tiles[2][0]} {self.tiles[3][0]}'

    def print(self):
        print(self)
