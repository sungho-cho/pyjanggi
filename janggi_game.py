import classes.constant as constant
from classes.board import Board
from classes.camp import Camp
from classes.formation import Formation
from classes.piece import Piece, PieceType
from classes.grid import Grid
from classes.move import MoveSet


class JanggiGame:

    def __init__(self, player: Camp, choFormation: Formation, hanFormation: Formation):
        self.player = player
        self.turn = Camp.CHO
        self._initializeBoard(choFormation, hanFormation)

    def makeMove(self, origin: Grid, dest: Grid, pieceType: PieceType):
        # Validate the given move
        if not self._validateMove(origin, dest, pieceType):
            print("The move cannot be made!")
            return

        # Detenmine if game's over
        gameOver = False
        destPiece = self.board.get(dest.row, dest.col)
        if destPiece and destPiece.pieceType == PieceType.GENERAL:
            gameOver = True

        # Make the move
        piece = self.board.get(origin.row, origin.col)
        self.board.remove(origin.row, origin.col)
        self.board.put(dest.row, dest.col, piece)

        # Update Cho and Han's scores
        self._updateScores()

        # Switch "turn"
        self.turn = self.turn.opponent

        print(self.board)

        return gameOver

    def getAllDestinations(self, origin: Grid):
        moveSets = self._getPossibleMoveSets(origin)
        allDest = [ms.getDest(self.board, origin, self.turn)
                   for ms in moveSets]
        return allDest

    def _initializeBoard(self, choFormation: Formation, hanFormation: Formation):
        self.board = Board()
        choBoard = choFormation.makeBoard()
        hanBoard = hanFormation.makeBoard()
        choBoard.markCamp(Camp.CHO)
        hanBoard.markCamp(Camp.HAN)
        if self.player == Camp.CHO:
            hanBoard.rotate()
        else:
            choBoard.rotate()

        self.board.merge(choBoard)
        self.board.merge(hanBoard)
        self._updateScores()

    def _updateScores(self):
        self.choScore = self.board.getScore(Camp.CHO)
        self.hanScore = self.board.getScore(Camp.HAN) + constant.HAN_ADVANTAGE

    def _getPossibleMoveSets(self, origin: Grid):
        def isOutOfBound(grid: Grid):
            return (grid.row < constant.MIN_ROW or grid.row > constant.MAX_ROW or
                    grid.col < constant.MIN_COL or grid.col > constant.MAX_COL)

        piece = self.board.get(origin.row, origin.col)
        # Invalidate when given grids are out of bound
        if isOutOfBound(origin):
            return []

        # Invalidate when no piece is on "origin" grid
        if not piece:
            return []

        if piece.camp != self.turn:
            return []

        # Get MoveSets depending on piece type
        if piece.pieceType == PieceType.SOLDIER:
            moveSets = piece.getSoldierMoveSets(self.player == self.turn)
        elif piece.pieceType == PieceType.HORSE or piece.pieceType == PieceType.ELEPHANT:
            moveSets = piece.getJumpyMoveSets()
        elif piece.pieceType == PieceType.CHARIOT or piece.pieceType == PieceType.CANNON:
            moveSets = piece.getStraightMoveSets(origin, piece.pieceType)
        elif piece.pieceType == PieceType.GENERAL or piece.pieceType == PieceType.GUARD:
            moveSets = piece.getJumpyMoveSets(origin, self.player == self.turn)

        moveSets = [ms for ms in moveSets if ms.isValid(
            self.board, origin, self.turn)]
        return moveSets

    def _validateMove(self, origin: Grid, dest: Grid, pieceType: PieceType):
        def _isOutOfBound(grid: Grid):
            return (grid.row < constant.MIN_ROW or grid.row > constant.MAX_ROW or
                    grid.col < constant.MIN_COL or grid.col > constant.MAX_COL)

        originPiece = self.board.get(origin.row, origin.col)
        destPiece = self.board.get(dest.row, dest.col)
        # Invalidate when given grids are out of bound
        if _isOutOfBound(origin) or _isOutOfBound(dest):
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

        # See if destination is in list of all possible destinatins from origin
        allDest = self.getAllDestinations(origin)
        if dest not in allDest:
            return False

        # TODO: Invalidate the move makes it enemy's "Janggun"
        return True

    def _getSoldierMoveSets(self, origin: Grid):
        piece = self.board.get(origin.row, origin.col)
        return piece.getSoldierMoveSets(self.player == self.turn)

    def _getCastleMoveSets(self, origin: Grid):
        piece = self.board.get(origin.row, origin.col)
        return piece.getJumpyMoveSets(origin, self.player == self.turn)

    def _getJumpyMoveSets(self, origin: Grid):
        piece = self.board.get(origin.row, origin.col)
        return piece.getJumpyMoveSets()

    def _getStraightMoveSets(self, origin: Grid, pieceType: PieceType):
        piece = self.board.get(origin.row, origin.col)
        return piece.getStraightMoveSets(origin, pieceType)
