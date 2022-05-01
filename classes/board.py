import classes.constant as constant
from classes.piece import Piece
from classes.camp import Camp


class Board:
    def __init__(self):
        self.numRows = constant.MAX_ROW-constant.MIN_ROW+1
        self.numCols = constant.MAX_COL-constant.MIN_COL+1
        self.__board = [[None for i in range(self.numCols+1)]
                        for j in range(self.numRows+1)]

    def __str__(self):
        printStr = ""
        for row in range(constant.MAX_ROW+1):
            for col in range(constant.MAX_COL+1):
                if row == 0 and col > 0:
                    printStr += " " + str(col)
                elif row > 0 and col == 0:
                    printStr += " " + str(row % 10)
                elif row > 0 and col > 0:
                    if self.__board[row][col]:
                        printStr += str(self.__board[row][col])
                    else:
                        printStr += "  "
                else:
                    printStr += " "
                printStr += " "
            printStr += "\n"
        return printStr

    def put(self, row: int, col: int, piece: Piece):
        self.__board[row][col] = piece

    def merge(self, board):
        for row in range(constant.MIN_ROW, constant.MAX_ROW+1):
            for col in range(constant.MIN_COL, constant.MAX_COL+1):
                if board.get(row, col):
                    self.__board[row][col] = board.get(row, col)

    def get(self, row: int, col: int):
        return self.__board[row][col]

    def remove(self, row: int, col: int):
        self.__board[row][col] = None

    def rotate(self):
        newBoard = [[None for i in range(self.numCols+1)]
                    for j in range(self.numRows+1)]
        for row in range(constant.MIN_ROW, constant.MAX_ROW+1):
            for col in range(constant.MIN_COL, constant.MAX_COL+1):
                if self.__board[row][col]:
                    newBoard[self.numRows-row+1][self.numCols -
                                                 col+1] = self.__board[row][col]
        self.__board = newBoard

    def markCamp(self, camp: Camp):
        for row in range(constant.MIN_ROW, constant.MAX_ROW+1):
            for col in range(constant.MIN_COL, constant.MAX_COL+1):
                if self.__board[row][col]:
                    self.__board[row][col].camp = camp
