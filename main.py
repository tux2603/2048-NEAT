from board import Board

if __name__ == '__main__':
    b = Board()
    b.placeTile()
    b.placeTile()
    while not b.isGameOver():

        print("\n--------")
        print(f'SCORE: {b.score}\n')
        print(b)
        
        direction = input("move: ")

        while True: 
            if direction == "w" and b.canMove(Board.UP): break
            if direction == "a" and b.canMove(Board.LEFT): break
            if direction == "s" and b.canMove(Board.DOWN): break
            if direction == "d" and b.canMove(Board.RIGHT): break
            direction = input("no. move: ")

        if direction == "w":
            b.move(Board.UP)
        if direction == "a":
            b.move(Board.LEFT)
        if direction == "s":
            b.move(Board.DOWN)
        if direction == "d":
            b.move(Board.RIGHT)
        
        b.placeTile()

    print(f'FINAL SCORE: {b.score}')