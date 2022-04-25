import random

from classes.gameboard import GameBoard
from classes.camp import Camp
from classes.formation import Formation

if __name__ == '__main__':
    camp = Camp(random.randint(0, 1))
    choFormation = Formation(random.randint(1, 4))
    hanFormation = Formation(random.randint(1, 4))
    gameboard = GameBoard(camp, choFormation, hanFormation)
    print(gameboard.board)
