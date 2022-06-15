from enum import Enum
from termcolor import colored
from typing import List, Tuple

from ..constants import (
    MIN_ROW, MAX_ROW, MIN_COL, MAX_COL,
    CASTLE_MIN_COL, CASTLE_MAX_COL,
    CASTLE_TOP_MIN_ROW, CASTLE_TOP_MAX_ROW,
    CASTLE_BOT_MIN_ROW, CASTLE_BOT_MAX_ROW,
    CASTLE_TOP_CENTER, CASTLE_BOT_CENTER,
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

from .move import MoveSet  # Imported here to avoid circular import.


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
        def _is_forward(move_set: MoveSet) -> bool:
            for (dr, _) in move_set.moves:
                if (is_player and dr > 0) or (not is_player and dr < 0):
                    return False
            return True
        steps = [(0, -1), (0, 1)]
        steps += [(-1, 0)] if is_player else [(1, 0)]
        move_sets = [MoveSet([(dr, dc)]) for (dr, dc) in steps]
        # Add castle move sets
        is_in_castle = self._is_in_castle(origin)
        if is_in_castle > -1:
            castle_move_sets = self.get_castle_move_sets(
                origin, is_in_castle, 1)
            castle_move_sets = filter(_is_forward, castle_move_sets)
            move_sets.extend(castle_move_sets)
        return move_sets

    def get_castle_move_sets(
            self,
            origin: Location,
            is_player: bool,
            max_step: int = 1) -> List[MoveSet]:
        """
        Get move sets for castle pieces (generals and guards).
        The directions a soldier piece can take depends on which camp it belongs to.

        Args:
            origin (Location): Original location of the piece.
            is_player (bool): True if the piece belongs to the main player; False otherwise.

        Returns:
            List[MoveSet]: All move sets a castle piece can make regardless of validity.
        """
        castle_locations = self._castle_locations(is_player)
        move_sets = []
        for dest in castle_locations:
            dr = dest.row - origin.row
            dc = dest.col - origin.col
            if origin == dest:
                continue
            if max(abs(dr), abs(dc)) > max_step:
                continue
            if self._is_move_diagonal(dr, dc) and not self._validate_castle_diagonal_move(origin, dest):
                continue
            dr_per_step = -1 if dr < 0 else 1 if dr > 0 else 0
            dc_per_step = -1 if dc < 0 else 1 if dc > 0 else 0
            move_sets.append(
                MoveSet([(dr_per_step, dc_per_step)] * max(abs(dr), abs(dc))))
        return move_sets

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
            while not _is_out_of_bound(row + dr, col + dc):
                row += dr
                col += dc
                steps.append((dr, dc))
                move_sets.append(MoveSet(steps.copy()))
            return move_sets

        move_sets = []
        # Add regular move sets
        for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            move_sets += _get_move_sets_in_direction(origin, dr, dc)
        # Add castle move sets
        is_in_castle = self._is_in_castle(origin)
        if is_in_castle > -1:
            castle_move_sets = self.get_castle_move_sets(
                origin, is_in_castle, 2)
            move_sets.extend(castle_move_sets)
        return move_sets

    # **************************************************
    # *********** Castle Helper Functions **************
    # **************************************************

    # Return 1 if in bottom castle, 0 if in top castle, -1 if not in csatle
    def _is_in_castle(self, l: Location) -> int:
        if l.col < CASTLE_MIN_COL and l.col > CASTLE_MAX_COL:
            return -1
        elif l.row >= CASTLE_TOP_MIN_ROW and l.row <= CASTLE_TOP_MAX_ROW:
            return 0
        elif l.row >= CASTLE_BOT_MIN_ROW and l.row <= CASTLE_BOT_MAX_ROW:
            return 1
        else:
            return -1

    def _is_move_diagonal(self, drow: int, dcol: int) -> bool:
        return drow != 0 and dcol != 0 and abs(drow) == abs(dcol)

    def _is_castle_vertex(self, l: Location) -> bool:
        return \
            (l.col == CASTLE_MIN_COL or l.col == CASTLE_MAX_COL) and\
            (l.row == CASTLE_TOP_MIN_ROW or l.row == CASTLE_TOP_MAX_ROW or
             l.row == CASTLE_BOT_MIN_ROW or l.row == CASTLE_BOT_MAX_ROW)

    # Return true if either origin or destination is castle's center
    def _validate_castle_diagonal_move(self, origin: Location, dest: Location) -> bool:
        return (tuple(origin) == CASTLE_TOP_CENTER or
                tuple(dest) == CASTLE_TOP_CENTER or
                tuple(origin) == CASTLE_BOT_CENTER or
                tuple(dest) == CASTLE_BOT_CENTER or
                (self._is_castle_vertex(origin) and self._is_castle_vertex(dest)))

    def _castle_locations(self, is_player: bool) -> List[Location]:
        min_row = CASTLE_BOT_MIN_ROW if is_player else CASTLE_TOP_MIN_ROW
        max_row = CASTLE_BOT_MAX_ROW if is_player else CASTLE_TOP_MAX_ROW
        min_col = CASTLE_MIN_COL
        max_col = CASTLE_MAX_COL
        return [Location(r, c) for r in range(min_row, max_row + 1) for c in range(min_col, max_col + 1)]
