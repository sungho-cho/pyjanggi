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

    def getPossibleMoves(self, origin: Grid):
        def isOutOfBound(grid: Grid):
            return (grid.row < constant.MIN_ROW or grid.row > constant.MAX_ROW or
                    grid.col < constant.MIN_COL or grid.col > constant.MAX_COL)

        customFn = {
            PieceType.SOLDIER: self.getSoldierMoves,
            PieceType.HORSE: self.getJumpyMoves,
            PieceType.ELEPHANT: self.getJumpyMoves,
            PieceType.CHARIOT: self.getStraightMoves,
            PieceType.CANNON: self.getStraightMoves,
            PieceType.GENERAL: self.getCastleMoves,
            PieceType.GUARD: self.getCastleMoves,
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
        
        print(customFn[piece.pieceType](origin, piece.pieceType))
    
    def getSoldierMoves(self, origin: Grid):
        moves = [(0, -1), (0, 1)]
        moves += [(-1, 0)] if self.player == self.turn else [(1, 0)]
        return moves

    def getCastleMoves(self, origin: Grid, pieceType: PieceType):
        # moves = [(i, j) for i in range(-1,2) for j in range(-1,2)]
        # moves.remove((0,0))
        # moves = [(i, j) for (i, j) in moves if]
        # return moves
        return []

    def getJumpyMoves(self, origin: Grid, pieceType: PieceType):
        return [3]

    def getStraightMoves(self, origin: Grid, pieceType: PieceType):
        return [2]

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

        # Run custom validation for each piece type
        customValidated = False
        if pieceType == PieceType.HORSE or pieceType == PieceType.ELEPHANT:
            customValidated = self.validateJumpyPieceMove(origin, dest)
        elif pieceType == PieceType.GENERAL or pieceType == PieceType.GUARD:
            customValidated = self.validateCastlePieceMove(origin, dest)
        elif pieceType == PieceType.SOLDIER:
            customValidated = self.validateSoldierPieceMove(origin, dest)
        elif pieceType == PieceType.CHARIOT or pieceType == PieceType.CANNON:
            customValidated = self.validateStraightPieceMove(origin, dest)
        if not customValidated:
            return False

        # Invalidate the move makes it enemy's "Janggun"
        return True

    def validateJumpyPieceMove(self, origin: Grid, dest: Grid):
        piece = self.board.get(origin.row, origin.col)
        jumpyMoves = piece.getJumpyMoves()
        for moves in jumpyMoves:
            validated = True
            row = origin.row
            col = origin.col
            for move in moves:
                row += move[0]
                col += move[1]
                if self.board.get(row, col):
                    pass
        return True

    def validateCastlePieceMove(self, origin: Grid, dest: Grid):
        return True

    def validateSoldierPieceMove(self, origin: Grid, dest: Grid):
        return True

    def validateStraightPieceMove(self, origin: Grid, dest: Grid):
        return True