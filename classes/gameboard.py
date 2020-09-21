import constant
from board import Board
from camp import Camp
from formation import Formation
from piece import Piece, PieceType
from grid import Grid

class GameBoard:

    def __init__(self, player: Camp, choFormation: Formation, hanFormation: Formation):
        self.board = Board()
        self.player = player
        self.turn = Camp.CHO

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

    def makeMove(self, origin: Grid, dest: Grid, pieceType: PieceType):
        # Validate the given move
        validated = self.validateMove(origin, dest, pieceType)
        if not validated:
            return

        # Make the move
        piece = self.board.get(origin.row, origin.col)
        self.board.remove(origin.row, origin.col)
        self.board.put(dest.row, dest.col, piece)

        # Check for "Janggun" or "Oitong"

        # Switch "turn"
        self.turn = self.turn.opponent

    def validateMove(self, origin: Grid, dest: Grid, pieceType: PieceType):
        def isOutOfBound(grid: Grid):
            return (grid.row < constant.MIN_ROW or grid.row > constant.MAX_ROW or
                    grid.col < constant.MIN_COL or grid.col > constant.MAX_COL)
        # Invalidate when given grids are out of bound
        if isOutOfBound(origin) or isOutOfBound(dest):
            return False
        
        # Invalidate when no piece is on "origin" grid
        # Invalidate when piece type is wrong
        # Invalidate when wrong camp
        # Invalidate when ally piece is already on "dest" grid
        # Run special validation for each piece type
        # Invalidate the move makes it enemy's "Janggun"
        return True