from . import constants


class Grid:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

        if self.row < constants.MIN_ROW or self.row > constants.MAX_ROW:
            raise Exception(f"grid row is out of range: {self.row}")

        if self.col < constants.MIN_COL or self.col > constants.MAX_COL:
            raise Exception(f"grid column is out of range: {self.col}")

    def __str__(self):
        return f"Grid({self.row},{self.col})"

    def __iter__(self):
        yield self.row
        yield self.col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
