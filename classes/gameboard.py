from board import Board
from camp import Camp
from formation import Formation

class GameBoard:

    def __init__(self, player: Camp, choFormation: Formation, hanFormation: Formation):
        self.board = Board()
        self.player = player

        choBoard = choFormation.makeBoard()
        hanBoard = hanFormation.makeBoard()

        choBoard.markCamp(Camp.CHO)
        hanBoard.markCamp(Camp.HAN)

        if self.player == Camp.CHO:
            hanBoard.rotate()
        else:
            choBoard.rotate()

        self.board.putAll(choBoard)
        self.board.putAll(hanBoard)