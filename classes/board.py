from . import constants
from .piece import Piece
from .camp import Camp
from .grid import Grid


class Board:
    def __init__(self):
        self.num_rows = constants.MAX_ROW-constants.MIN_ROW+1
        self.num_cols = constants.MAX_COL-constants.MIN_COL+1
        self.__board = [[None for i in range(self.num_cols+1)]
                        for j in range(self.num_rows+1)]

    def __str__(self):
        print_str = ""
        for row in range(constants.MAX_ROW+1):
            for col in range(constants.MAX_COL+1):
                if row == 0 and col > 0:
                    print_str += " " + str(col)
                elif row > 0 and col == 0:
                    print_str += " " + str(row % 10)
                elif row > 0 and col > 0:
                    if self.__board[row][col]:
                        print_str += str(self.__board[row][col])
                    else:
                        print_str += "  "
                else:
                    print_str += " "
                print_str += " "
            print_str += "\n"
        return print_str

    # used row,col as inputs instead of grid to make it easier to generate boards in formation.py
    def put(self, row: int, col: int, piece: Piece):
        self.__board[row][col] = piece

    def merge(self, board):
        for row in range(constants.MIN_ROW, constants.MAX_ROW+1):
            for col in range(constants.MIN_COL, constants.MAX_COL+1):
                if board.get(row, col):
                    self.__board[row][col] = board.get(row, col)

    def get(self, row: int, col: int):
        return self.__board[row][col]

    def remove(self, row: int, col: int):
        self.__board[row][col] = None

    def rotate(self):
        new_board = [[None for i in range(self.num_cols+1)]
                     for j in range(self.num_rows+1)]
        for row in range(constants.MIN_ROW, constants.MAX_ROW+1):
            for col in range(constants.MIN_COL, constants.MAX_COL+1):
                if self.__board[row][col]:
                    new_board[self.num_rows-row+1][self.num_cols -
                                                   col+1] = self.__board[row][col]
        self.__board = new_board

    def mark_camp(self, camp: Camp):
        for row in range(constants.MIN_ROW, constants.MAX_ROW+1):
            for col in range(constants.MIN_COL, constants.MAX_COL+1):
                if self.__board[row][col]:
                    self.__board[row][col].camp = camp

    def get_score(self, camp: Camp):
        score = 0
        for row in range(constants.MIN_ROW, constants.MAX_ROW+1):
            for col in range(constants.MIN_COL, constants.MAX_COL+1):
                if self.__board[row][col] and self.__board[row][col].camp == camp:
                    score += self.__board[row][col].value
        return score

    def get_piece_locations(self, camp: Camp):
        piece_locations = []
        for row in range(constants.MIN_ROW, constants.MAX_ROW+1):
            for col in range(constants.MIN_COL, constants.MAX_COL+1):
                if self.__board[row][col] and self.__board[row][col].camp == camp:
                    piece_locations.append(Grid(row, col))
        return piece_locations
