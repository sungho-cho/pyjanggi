from __future__ import annotations
from typing import Iterable
from ..constants import MIN_ROW, MAX_ROW, MIN_COL, MAX_COL
from ..proto import log_pb2


class Location:
    """
    Location class that each represents a single location on the board grid.
    """

    def __init__(self, row: int, col: int):
        """
        Initialize location.

        Args:
            row (int): row number in range 0 <= row <= 9.
            col (int): column number in range 0 <= col <= 8.

        Raises:
            Exception: row is out of range.
            Exception: column is out of range.
        """
        self.row = row
        self.col = col

        if self.row < MIN_ROW or self.row > MAX_ROW:
            raise Exception(f"location row is out of range: {self.row}")

        if self.col < MIN_COL or self.col > MAX_COL:
            raise Exception(f"location column is out of range: {self.col}")

    def __str__(self) -> str:
        """Return string representation of location."""
        return f"({self.row},{self.col})"

    def __iter__(self) -> Iterable:
        """Make location iterable so that it can easily be converted into a tuple or list."""
        yield self.row
        yield self.col

    def __eq__(self, other) -> bool:
        """Return True if two location classes have same row and col; False otherwise."""
        return self.row == other.row and self.col == other.col

    @classmethod
    def from_proto(cls, location_proto: log_pb2.Location) -> Location:
        """Convert from proto Location message."""
        return Location(location_proto.row, location_proto.col)

    def to_proto(self) -> log_pb2.Location:
        """Convert to proto Location message."""
        location_proto = log_pb2.Location()
        location_proto.row = self.row
        location_proto.col = self.col
        return location_proto
