from typing import List, Tuple

from .constants import MIN_ROW, MAX_ROW, MIN_COL, MAX_COL
from .location import Location
from .camp import Camp
from .piece import PieceType


class MoveSet:
    """
    MoveSet is a list of a piece's moves in order to complete a single action.
    MoveSet ~ [(dr1, dc1), (dr2, dc2), (dr3, dc3), ...].
    If a player makes an action to move a Chariot piece 3 tiles up,
    its move set will be [(-1,0), (-1,0), (-1,0)].
    """
    def __init__(self, moves: List[Tuple[int, int]]):
        """Initialize MoveSet with the given list of moves."""
        self.moves = moves

    def __str__(self) -> str:
        """Return string representation of MoveSet."""
        return str(self.moves)

    def get_dest(self, board: "Board", origin: Location, player: Camp) -> Location:
        """
        Get destination location of piece at given origin location for the given player.

        Args:
            board (Board): Current board being played.
            origin (Location): Original location of the piece being played.
            player (Camp): Current player to make an action.

        Returns:
            Location: Destination of the piece if it's played through self.moves from origin.
        """
        if self.is_valid(board, origin, player):
            row, col = (origin.row, origin.col)
            for dr, dc in self.moves:
                row += dr
                col += dc
            return Location(row, col)
        else:
            return None

    def is_valid(self, board: "Board", origin: Location, player: Camp) -> bool:
        """
        Check validity of a move set for piece at the given origin for the given player.

        Args:
            board (Board): Current board being played.
            origin (Location): Original location of the piece being played.
            player (Camp): Current player to make an action.

        Returns:
            bool: True if move set is valid; False otherwise
        """
        def _is_out_of_bound(row: int, col: int):
            return (row < MIN_ROW or row > MAX_ROW or
                    col < MIN_COL or col > MAX_COL)
        origin_piece = board.get(origin.row, origin.col)
        num_hurdles = 1 if origin_piece.piece_type == PieceType.CANNON else 0
        row, col = (origin.row, origin.col)
        for i in range(len(self.moves)):
            (dr, dc) = self.moves[i]
            row += dr
            col += dc
            if _is_out_of_bound(row, col):
                return False

            piece = board.get(row, col)

            if i == len(self.moves)-1:
                # invalidate if some hurdles are left for a cannon
                if origin_piece.piece_type == PieceType.CANNON and num_hurdles > 0:
                    return False
                # invalidate if landing on an ally piece
                if piece and piece.camp == player:
                    return False

            elif piece:
                if origin_piece.piece_type == PieceType.CANNON:
                    # cannon cannot ever pass cannon
                    if piece.piece_type == PieceType.CANNON:
                        return False
                    # decrement number of hurdles left when passing a piece
                    num_hurdles -= 1
                    if num_hurdles < 0:
                        return False
                else:
                    # invalidate if there's a blocking piece before move set is complete
                    return False
        return True
