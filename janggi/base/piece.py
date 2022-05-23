from .move import MoveSet  # Imported here to avoid an import loop.
from enum import Enum
from termcolor import colored
from typing import List

from ..constants import (
    MIN_ROW, MAX_ROW, MIN_COL, MAX_COL,
    CASTLE_MIN_COL, CASTLE_MAX_COL,
    CASTLE_TOP_MIN_ROW, CASTLE_TOP_MAX_ROW,
    CASTLE_BOT_MIN_ROW, CASTLE_BOT_MAX_ROW,
    CASTLE_TOP_SOLDIER_EXCEPTION_LEFT,
    CASTLE_TOP_SOLDIER_EXCEPTION_RIGHT,
    CASTLE_BOT_SOLDIER_EXCEPTION_LEFT,
    CASTLE_BOT_SOLDIER_EXCEPTION_RIGHT,
)
from .camp import Camp
from .location import Location


class PieceType(Enum):
    """Enum class representing a piece's type."""
    GENERAL = 1
    GUARD = 2
    HORSE = 3
    ELEPHANT = 4
    CHARIOT = 5
    CANNON = 6
    SOLDIER = 7


PIECE_VALUE = {
    PieceType.GUARD: 3,
    PieceType.HORSE: 5,
    PieceType.ELEPHANT: 3,
    PieceType.CHARIOT: 13,
    PieceType.CANNON: 7,
    PieceType.SOLDIER: 2,
    PieceType.GENERAL: 0,
}


class Piece:
    """
    Piece class represents a single piece on the game board.
    The class is capable of getting move sets based on its piece type.
    """

    def __init__(self, piece_type: PieceType):
        """
        Initialize Piece class by setting the given piece type.
        Camp attribute is later initialized by Board.mark_camp.
        """
        self.piece_type = piece_type
        self.camp = None

    def __float__(self) -> float:
        """
        Get unique float value for the piece's type.
        For all camp cho's pieces, this returns +(self.piece_type.value)
        For all camp han's pieces, this returns -(self.piece_type.value)

        Raises:
            Exception: if a piece does not have a camp assigned yet.

        Returns:
            float: uniqued float value for the piece's type.
        """
        if self.camp == None:
            raise Exception(
                f"{self.piece_type} does not have a camp assigned.")

        if self.camp == Camp.HAN:
            return float(self.piece_type.value) * -1.0
        else:
            return float(self.piece_type.value)

    @property
    def value(self) -> int:
        """
        Return piece's value based on its piece type. Each piece in Janggi has a 
        value assigned, and the values contribute to the players' current scores.

        Returns:
            int: piece's value based on type.
        """
        return PIECE_VALUE[self.piece_type]

    def __str__(self) -> str:
        """
        Return string representation of piece while applying different colors for each camp.
        """
        print_str = self._piece_to_chinese_character()
        if self.camp == Camp.CHO:
            print_str = colored(print_str, 'green')
        elif self.camp == Camp.HAN:
            print_str = colored(print_str, 'red')
        return print_str

    def _piece_to_chinese_character(self) -> str:
        """
        Return a Chinese character for the piece based on its type and camp.

        Returns:
            str: a single Chinese character for the piece.
        """
        piece_name_dict = {
            PieceType.GUARD: "士",
            PieceType.HORSE: "馬",
            PieceType.ELEPHANT: "象",
            PieceType.CHARIOT: "車",
            PieceType.CANNON: "包",
        }

        if self.piece_type in piece_name_dict:
            return piece_name_dict[self.piece_type]
        else:
            if self.piece_type == PieceType.GENERAL:
                if self.camp == Camp.CHO:
                    return "楚"
                else:
                    return "漢"
            elif self.piece_type == PieceType.SOLDIER:
                if self.camp == Camp.CHO:
                    return "卒"
                else:
                    return "兵"

    def get_soldier_move_sets(self, origin: Location, is_player: bool) -> List[MoveSet]:
        """
        Get move sets for soldier pieces.
        The directions a soldier piece can take depends on which camp it belongs to.

        Args:
            is_player (bool): True if the piece belongs to the main player; False otherwise.

        Returns:
            List[MoveSet]: All move sets a soldier piece can make regardless of validity.
        """
        steps = [(0, -1), (0, 1)]
        steps += [(-1, 0)] if is_player else [(1, 0)]
        # soldiers can move diagonally in enemy's castle
        if is_player:
            if tuple(origin) == CASTLE_TOP_SOLDIER_EXCEPTION_LEFT:
                steps += [(-1, 1)]
            elif tuple(origin) == CASTLE_TOP_SOLDIER_EXCEPTION_RIGHT:
                steps += [(-1, -1)]
        else:
            if tuple(origin) == CASTLE_BOT_SOLDIER_EXCEPTION_LEFT:
                steps += [(1, 1)]
            elif tuple(origin) == CASTLE_BOT_SOLDIER_EXCEPTION_RIGHT:
                steps += [(1, -1)]
        return [MoveSet([(dr, dc)]) for (dr, dc) in steps]

    def get_castle_move_sets(self, origin: Location, is_player: bool) -> List[MoveSet]:
        """
        Get move sets for castle pieces (generals and guards).
        The directions a soldier piece can take depends on which camp it belongs to.

        Args:
            origin (Location): Original location of the piece.
            is_player (bool): True if the piece belongs to the main player; False otherwise.

        Returns:
            List[MoveSet]: All move sets a castle piece can make regardless of validity.
        """
        def _is_out_of_bound(row: int, col: int):
            return (col < CASTLE_MIN_COL or col > CASTLE_MAX_COL or
                    (is_player and (row < CASTLE_BOT_MIN_ROW or row > CASTLE_BOT_MAX_ROW)) or
                    (not is_player and (row < CASTLE_TOP_MIN_ROW or row > CASTLE_TOP_MAX_ROW)))
        steps = [(i, j) for i in range(-1, 2)
                 for j in range(-1, 2) if i != 0 or j != 0]
        steps = [(i, j) for (i, j) in steps if not _is_out_of_bound(
            origin.row+i, origin.col+j)]
        return [MoveSet([(dr, dc)]) for (dr, dc) in steps]

    def get_jumpy_move_sets(self) -> List[MoveSet]:
        """
        Get move sets for jumpy pieces (horses and elephants).

        Returns:
            List[MoveSet]: All move sets a jumpy piece can make regardless of validity.
        """
        move_sets = []
        if self.piece_type == PieceType.HORSE:
            move_sets.append(MoveSet([(0, 1), (-1, 1)]))
            move_sets.append(MoveSet([(0, 1), (1, 1)]))
            move_sets.append(MoveSet([(1, 0), (1, 1)]))
            move_sets.append(MoveSet([(1, 0), (1, -1)]))
            move_sets.append(MoveSet([(0, -1), (-1, -1)]))
            move_sets.append(MoveSet([(0, -1), (1, -1)]))
            move_sets.append(MoveSet([(-1, 0), (-1, 1)]))
            move_sets.append(MoveSet([(-1, 0), (-1, -1)]))
        elif self.piece_type == PieceType.ELEPHANT:
            move_sets.append(MoveSet([(0, 1), (-1, 1), (-1, 1)]))
            move_sets.append(MoveSet([(0, 1), (1, 1), (1, 1)]))
            move_sets.append(MoveSet([(1, 0), (1, 1), (1, 1)]))
            move_sets.append(MoveSet([(1, 0), (1, -1), (1, -1)]))
            move_sets.append(MoveSet([(0, -1), (-1, -1), (-1, -1)]))
            move_sets.append(MoveSet([(0, -1), (1, -1), (1, -1)]))
            move_sets.append(MoveSet([(-1, 0), (-1, 1), (-1, 1)]))
            move_sets.append(MoveSet([(-1, 0), (-1, -1), (-1, -1)]))
        return move_sets

    def get_straight_move_sets(self, origin: Location) -> List[MoveSet]:
        """
        Get move sets for straight pieces (chariots and cannons).

        Args:
            origin (Location): Original location of the piece.

        Returns:s
            List[MoveSet]: All move sets a straight piece can make regardless of validity.
        """
        def _is_out_of_bound(row: int, col: int):
            return (row < MIN_ROW or row > MAX_ROW or
                    col < MIN_COL or col > MAX_COL)

        def _get_move_sets_in_direction(origin: Location, dr: int, dc: int):
            (row, col) = (origin.row, origin.col)
            steps = []
            move_sets = []
            while not _is_out_of_bound(row+dr, col+dc):
                row += dr
                col += dc
                steps.append((dr, dc))
                move_sets.append(MoveSet(steps.copy()))
            return move_sets

        move_sets = []
        for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            move_sets += _get_move_sets_in_direction(origin, dr, dc)
        return move_sets
