from __future__ import annotations
from typing import List

from .constants import MIN_ROW, MAX_ROW, MIN_COL, MAX_COL
from .piece import Piece
from .camp import Camp
from .location import Location


class Board:
    """
    Simple board class used for the game of Janggi. Contains and handles a single 
    10x9 two-dimensional list that contains either a Piece object or None.
    """
    def __init__(self):
        self.num_rows = MAX_ROW-MIN_ROW+1
        self.num_cols = MAX_COL-MIN_COL+1
        self.__board = [[None for i in range(self.num_cols)]
                        for j in range(self.num_rows)]

    def __str__(self) -> str:
        """Generate colored and structured string representation of the board."""
        print_str = ""
        for row in range(-1, MAX_ROW+1):
            for col in range(-1, MAX_COL+1):
                if row == -1 and col >= 0:
                    print_str += " " + str(col)
                elif row >= 0 and col == -1:
                    print_str += " " + str(row % 10)
                elif row >= 0 and col >= 0:
                    if self.__board[row][col]:
                        print_str += str(self.__board[row][col])
                    else:
                        print_str += "  "
                else:
                    print_str += " "
                print_str += " "
            print_str += "\n"
        return print_str

    def put(self, row: int, col: int, piece: Piece):
        """
        Put piece into board at the given (row,col) location.
        Used row and col as inputs instead of Location to make it easier to generate
        initial boards in formation.py.

        Args:
            row (int): Row that the given piece that will placed on.
            col (int): Column that the given piece that will be placed on.
            piece (Piece): Piece that will be placed on the board.
        """
        self.__board[row][col] = piece

    def merge(self, board: Board):
        """
        Merge the given board into self.__board by overwriting.

        Args:
            board (Board): Input board that will be merged into self.__board.
        """
        for row in range(MIN_ROW, MAX_ROW+1):
            for col in range(MIN_COL, MAX_COL+1):
                if board.get(row, col):
                    self.__board[row][col] = board.get(row, col)

    def get(self, row: int, col: int) -> Piece:
        """
        Return the piece that is located at the given location of the board.

        Args:
            row (int): Row of piece.
            col (int): Column of piece.

        Returns:
            Piece: Piece located at (row,col) on the board. Can be None.
        """
        return self.__board[row][col]

    def remove(self, row: int, col: int):
        """
        Remove piece at the given location of the board.

        Args:
            row (int): Row of the piece to be removed.
            col (int): Column of the piece to be removed.
        """
        self.__board[row][col] = None

    def rotate(self):
        """Rotate the board 180 degrees and update self.__board."""
        new_board = [[None for i in range(self.num_cols)]
                     for j in range(self.num_rows)]
        for row in range(MIN_ROW, MAX_ROW+1):
            for col in range(MIN_COL, MAX_COL+1):
                if self.__board[row][col]:
                    new_board[self.num_rows-row-1][self.num_cols -
                                                   col-1] = self.__board[row][col]
        self.__board = new_board

    def mark_camp(self, camp: Camp):
        """
        Mark all pieces on the board with the given camp (CHO or HAN).
        Used to mark half-boards when setting up initial boards.

        Args:
            camp (Camp): Camp enum to mark pieces with.
        """
        for row in range(MIN_ROW, MAX_ROW+1):
            for col in range(MIN_COL, MAX_COL+1):
                if self.__board[row][col]:
                    self.__board[row][col].camp = camp

    def get_score(self, camp: Camp) -> int:
        """
        Return score for the player who's playing the given camp.

        Args:
            camp (Camp): Camp of the player whose score will be calculated.

        Returns:
            int: Score of the player who's playing the given camp.
        """
        score = 0
        for row in range(MIN_ROW, MAX_ROW+1):
            for col in range(MIN_COL, MAX_COL+1):
                if self.__board[row][col] and self.__board[row][col].camp == camp:
                    score += self.__board[row][col].value
        return score

    def get_piece_locations(self, camp: Camp) -> List[Location]:
        """
        Get locations of all pieces with the given camp.

        Args:
            camp (Camp): Camp of the pieces to fetch.

        Returns:
            List[Location]: List of all locations of the pieces with the given camp.
        """
        piece_locations = []
        for row in range(MIN_ROW, MAX_ROW+1):
            for col in range(MIN_COL, MAX_COL+1):
                if self.__board[row][col] and self.__board[row][col].camp == camp:
                    piece_locations.append(Location(row, col))
        return piece_locations
