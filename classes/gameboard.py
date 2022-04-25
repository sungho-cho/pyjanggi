import classes.constant as constant
from classes.board import Board
from classes.camp import Camp
from classes.formation import Formation
from classes.piece import Piece, PieceType
from classes.grid import Grid
from classes.move import MoveSet


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
        if not self.validateMove(origin, dest, pieceType):
            print("The move cannot be made!")
            return

        # Make the move
        piece = self.board.get(origin.row, origin.col)
        self.board.remove(origin.row, origin.col)
        self.board.put(dest.row, dest.col, piece)

        # Switch "turn"
        self.turn = self.turn.opponent

        print(self.board)

    def getPossibleMoveSets(self, origin: Grid):
        def isOutOfBound(grid: Grid):
            return (grid.row < constant.MIN_ROW or grid.row > constant.MAX_ROW or
                    grid.col < constant.MIN_COL or grid.col > constant.MAX_COL)

        customFn = {
            PieceType.SOLDIER: self.getSoldierMoveSets,
            PieceType.HORSE: self.getJumpyMoveSets,
            PieceType.ELEPHANT: self.getJumpyMoveSets,
            PieceType.CHARIOT: self.getStraightMoveSets,
            PieceType.CANNON: self.getStraightMoveSets,
            PieceType.GENERAL: self.getCastleMoveSets,
            PieceType.GUARD: self.getCastleMoveSets,
        }

        piece = self.board.get(origin.row, origin.col)
        # Invalidate when given grids are out of bound
        if isOutOfBound(origin):
            return []

        # Invalidate when no piece is on "origin" grid
        if not piece:
            return []

        if piece.camp != self.turn:
            return []

        moveSets = customFn[piece.pieceType](origin, piece.pieceType)
        moveSets = [ms for ms in moveSets if ms.validate(
            self.board, origin, self.turn)]
        return moveSets

    def getSoldierMoveSets(self, origin: Grid, pieceType: PieceType):
        steps = [(0, -1), (0, 1)]
        steps += [(-1, 0)] if self.player == self.turn else [(1, 0)]
        return [MoveSet([(dr, dc)], False) for (dr, dc) in steps]

    def getCastleMoveSets(self, origin: Grid, pieceType: PieceType):
        def isOutOfBound(row: int, col: int):
            return (col < 4 or col > 6 or
                    (self.turn == self.player and (row < 8 or row > 10)) and
                    (self.turn != self.player and (row < 1 or row > 3)))
        steps = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        steps.remove((0, 0))
        steps = [(i, j) for (i, j) in steps
                 if not isOutOfBound(origin.row+i, origin.col+j)]
        return [MoveSet([(dr, dc)], False) for (dr, dc) in steps]

    def getJumpyMoveSets(self, origin: Grid, pieceType: PieceType):
        piece = self.board.get(origin.row, origin.col)
        return piece.getJumpyMoveSets()

    def getStraightMoveSets(self, origin: Grid, pieceType: PieceType):
        def isOutOfBound(row: int, col: int):
            return (row < constant.MIN_ROW or row > constant.MAX_ROW or
                    col < constant.MIN_COL or col > constant.MAX_COL)

        def getMoveSetsInDirection(origin: Grid, dr: int, dc: int):
            (row, col) = (origin.row, origin.col)
            steps = []
            moveSets = []
            while not isOutOfBound(row+dr, col+dc):
                row += dr
                col += dc
                steps.append((dr, dc))
                moveSets.append(
                    MoveSet(steps.copy(), pieceType == PieceType.CANNON))
            return moveSets

        moveSets = []
        for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            moveSets += getMoveSetsInDirection(origin, dr, dc)
        return moveSets

    def validateMove(self, origin: Grid, dest: Grid, pieceType: PieceType):
        def isOutOfBound(grid: Grid):
            return (grid.row < constant.MIN_ROW or grid.row > constant.MAX_ROW or
                    grid.col < constant.MIN_COL or grid.col > constant.MAX_COL)

        originPiece = self.board.get(origin.row, origin.col)
        destPiece = self.board.get(dest.row, dest.col)
        # Invalidate when given grids are out of bound
        if isOutOfBound(origin) or isOutOfBound(dest):
            return False

        # Invalidate when no piece is on "origin" grid
        if not originPiece:
            return False

        # Invalidate when piece type is wrong
        if originPiece.pieceType != pieceType:
            return False

        # Invalidate when wrong camp
        if originPiece.camp != self.turn:
            return False

        # Invalidate when ally piece is already on "dest" grid
        if destPiece and destPiece.camp == originPiece.camp:
            return False

        # See if dest is in list of all possible destinatins from origin
        moveSets = self.getPossibleMoveSets(origin)
        allDest = [ms.getDest(self.board, origin, self.turn)
                   for ms in moveSets]
        if dest not in allDest:
            return False

        # TODO: Invalidate the move makes it enemy's "Janggun"
        return True
