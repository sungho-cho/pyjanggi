from typing import List, Tuple

from ..constants import MIN_ROW, MAX_ROW, MIN_COL, MAX_COL, HAN_ADVANTAGE
from ..base.board import Board
from ..base.camp import Camp
from ..base.formation import Formation
from ..base.piece import PieceType
from ..base.location import Location
from ..base.move import MoveSet
from .game_log import GameLog


class JanggiGame:
    """
    A game of Janggi with a game board, players, and scores.
    With two public methods, this class can help make a single action on the board,
    and it can also get all possible moves from a current state of the board.
    """

    def __init__(self, player: Camp, cho_formation: Formation, han_formation: Formation):
        """
        Initialize Janggi game instance.

        Args:
            player (Camp): Camp that the main player is playing.
            cho_formation (Formation): Formation of camp cho.
            han_formation (Formation): Formation of camp han.
        """
        self.player = player
        self.cho_formation = cho_formation
        self.han_formation = han_formation

        self.turn = Camp.CHO
        self.cho_score = self.han_score = 0.0
        self.log = GameLog(cho_formation, han_formation, player)
        self.board = Board.full_board_from_formations(
            cho_formation, han_formation, player)
        self.initial_board = self.board.copy()
        self._update_scores()

    def make_action(self, origin: Location, dest: Location) -> Tuple[float, bool]:
        """
        Move a piece from the given origin location to the given destination.

        Args:
            origin (Location): Original location of the piece to be moved.
            dest (Location): Destination of the piece to be moved.

        Raises:
            Exception: When the given action is invalid.

        Returns:
            piece_value (float): An enemy piece's value if it was killed; 0 otherwise.
            game_over (bool): True if the action ends the game; False otherwise.
        """
        # validate the given action
        if not self._validate_action(origin, dest):
            raise Exception("The action cannot be made!")

        # make the action
        piece_removed = self.board.move(origin, dest)

        # detenmine if game's over
        game_over = False
        piece_value = 0
        if piece_removed:
            piece_value = piece_removed.value
            if piece_removed.piece_type == PieceType.GENERAL:
                game_over = True

        # update cho and han's scores
        self._update_scores()

        # switch "turn"
        self.turn = self.turn.opponent

        # record move logs
        self.log.add_move((origin, dest))

        return float(piece_value), game_over

    def get_all_actions(self) -> List[Tuple[Location, Location]]:
        """
        Get list of all possible moves that can be made for the current player.

        Returns:
            List[Tuple[Location, Location]]: List of moves in (origin, dest) format 
              where it means a piece at origin location being moved to dest location.
        """
        possible_actions = []
        piece_locations = self.board.get_piece_locations_for_camp(self.turn)
        for piece_location in piece_locations:
            destinations = self.get_all_destinations(piece_location)
            possible_actions += [(piece_location, dest_location)
                                 for dest_location in destinations]
        return possible_actions

    def get_all_destinations(self, origin: Location) -> List[Location]:
        """
        List all possible locations where a piece at given origin can move to.

        Args:
            origin (Location): Location of the piece to get destionations for.

        Returns:
            List[Location]: List of all possible locations the piece can go to.
        """
        move_sets = self._get_possible_move_sets(origin)
        all_dest = [ms.get_dest(self.board, origin, self.turn)
                    for ms in move_sets]
        return all_dest

    def _update_scores(self):
        """
        Update cho and han's scores by summing up each of their piece's value.
        """
        self.cho_score = self.board.get_score(Camp.CHO)
        self.han_score = self.board.get_score(Camp.HAN) + HAN_ADVANTAGE

    def _get_possible_move_sets(self, origin: Location) -> List[MoveSet]:
        """
        Get all move sets that pertain to a piece at origin location.
        In other words, get list of all moves a piece at origin can make, as MoveSet instances.

        Args:
            origin (Location): Location of the piece in question.

        Raises:
            Exception: When the given input is invalid.

        Returns:
            List[MoveSet]: MoveSets that the piece can possibly perform.
        """
        def _is_out_of_bound(location: Location):
            return (location.row < MIN_ROW or location.row > MAX_ROW or
                    location.col < MIN_COL or location.col > MAX_COL)

        piece = self.board.get(origin.row, origin.col)
        # Invalidate when given locations are out of bound
        if _is_out_of_bound(origin):
            raise Exception(f"The location {origin} is out of bound.")

        # Invalidate when no piece is on "origin" location
        if not piece:
            raise Exception(f"There is not piece on the location {origin}.")

        # Invalidate when the piece does not belong to the current player
        if piece.camp != self.turn:
            raise Exception(
                f"The piece {piece.piece_type} does not belong to the current player {self.turn}.")

        # Get MoveSets based on piece type
        if piece.piece_type == PieceType.SOLDIER:
            move_sets = piece.get_soldier_move_sets(
                origin, self.player == self.turn)
        elif piece.piece_type == PieceType.HORSE or piece.piece_type == PieceType.ELEPHANT:
            move_sets = piece.get_jumpy_move_sets()
        elif piece.piece_type == PieceType.CHARIOT or piece.piece_type == PieceType.CANNON:
            move_sets = piece.get_straight_move_sets(origin)
        elif piece.piece_type == PieceType.GENERAL or piece.piece_type == PieceType.GUARD:
            move_sets = piece.get_castle_move_sets(
                origin, self.player == self.turn)

        # Filter out all the invalid move sets
        move_sets = [ms for ms in move_sets if ms.is_valid(
            self.board, origin, self.turn)]
        return move_sets

    def _validate_action(self, origin: Location, dest: Location) -> bool:
        """
        Check if the given action is valid.

        Args:
            origin (Location): Original location of the piece in question.
            dest (Location): Desired location for the piece to be moved.

        Returns:
            bool: True if action is valid; False otherwise.
        """
        def _is_out_of_bound(location: Location):
            return (location.row < MIN_ROW or location.row > MAX_ROW or
                    location.col < MIN_COL or location.col > MAX_COL)

        origin_piece = self.board.get(origin.row, origin.col)
        dest_piece = self.board.get(dest.row, dest.col)
        # Invalidate when given locations are out of bound
        if _is_out_of_bound(origin) or _is_out_of_bound(dest):
            return False

        # Invalidate when no piece is on "origin" location
        if not origin_piece:
            return False

        # Invalidate when wrong camp
        if origin_piece.camp != self.turn:
            return False

        # Invalidate when ally piece is already on "dest" location
        if dest_piece and dest_piece.camp == origin_piece.camp:
            return False

        # See if destination is in list of all possible destinatins from origin
        if dest not in self.get_all_destinations(origin):
            return False

        # TODO: Invalidate the move makes it enemy's "Janggun"
        return True
