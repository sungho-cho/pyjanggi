import classes.constant as constant


class Grid:
    def __init__(self, row: int, col: int):
        self.row = row if row != 0 else row+10
        self.col = col

        if self.row < constant.MIN_ROW or self.row > constant.MAX_ROW:
            raise Exception(f"Grid row is out of range: {self.row}")

        if self.col < constant.MIN_COL or self.col > constant.MAX_COL:
            raise Exception(f"Grid column is out of range: {self.col}")

    def __iter__(self):
        yield self.row
        yield self.col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
