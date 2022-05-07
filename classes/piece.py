from enum import Enum
from termcolor import colored

from . import constants
from .camp import Camp
from .grid import Grid


class PieceType(Enum):
    GENERAL = 1
    GUARD = 2
    HORSE = 3
    ELEPHANT = 4
    CHARIOT = 5
    CANNON = 6
    SOLDIER = 7


class Piece:
    from .move import MoveSet

    def __init__(self, piece_type: PieceType):
        self.piece_type = piece_type
        self.camp = None

    def __int__(self):
        if not self.camp:
            raise Exception(
                f"{self.piece_type} does not have a camp assigned.")

        if self.camp == Camp.HAN:
            return self.piece_type.value * -1
        else:
            return self.piece_type.value

    @property
    def value(self):
        value_dict = {
            PieceType.GUARD: 3,
            PieceType.HORSE: 5,
            PieceType.ELEPHANT: 3,
            PieceType.CHARIOT: 13,
            PieceType.CANNON: 7,
            PieceType.SOLDIER: 2,
            PieceType.GENERAL: 0,
        }
        return value_dict[self.piece_type]

    def _piece_to_str(self):
        piece_dict = {
            PieceType.GUARD: "士",
            PieceType.HORSE: "馬",
            PieceType.ELEPHANT: "象",
            PieceType.CHARIOT: "車",
            PieceType.CANNON: "包",
        }

        if self.piece_type in piece_dict:
            return piece_dict[self.piece_type]
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

    def __str__(self):
        print_str = self._piece_to_str()
        if self.camp == Camp.CHO:
            print_str = colored(print_str, 'green')
        elif self.camp == Camp.HAN:
            print_str = colored(print_str, 'red')
        return print_str

    def get_soldier_move_sets(self, is_player: bool):
        steps = [(0, -1), (0, 1)]
        steps += [(-1, 0)] if is_player else [(1, 0)]
        return [MoveSet([(dr, dc)]) for (dr, dc) in steps]

    def get_castle_move_sets(self, origin: Grid, is_player: bool):
        def is_out_of_bound(row: int, col: int):
            return (col < 4 or col > 6 or
                    (is_player and (row < 8 or row > 10)) and
                    (is_player and (row < 1 or row > 3)))
        steps = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        steps.remove((0, 0))
        steps = [(i, j) for (i, j) in steps
                 if not is_out_of_bound(origin.row+i, origin.col+j)]
        return [MoveSet([(dr, dc)]) for (dr, dc) in steps]

    def get_jumpy_move_sets(self):
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

    def get_straight_move_sets(self, origin: Grid, piece_type: PieceType):
        def _is_out_of_bound(row: int, col: int):
            return (row < constants.MIN_ROW or row > constants.MAX_ROW or
                    col < constants.MIN_COL or col > constants.MAX_COL)

        def _get_move_sets_in_direction(origin: Grid, dr: int, dc: int):
            (row, col) = (origin.row, origin.col)
            steps = []
            move_sets = []
            while not _is_out_of_bound(row+dr, col+dc):
                row += dr
                col += dc
                steps.append((dr, dc))
                move_sets.append(
                    MoveSet(steps.copy(), piece_type == PieceType.CANNON))
            return move_sets

        move_sets = []
        for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            move_sets += _get_move_sets_in_direction(origin, dr, dc)
        return move_sets
