from classes import constants
from classes.board import Board
from classes.camp import Camp
from classes.formation import Formation
from classes.piece import PieceType
from classes.grid import Grid


class JanggiGame:

    def __init__(self, player: Camp, cho_formation: Formation, han_formation: Formation):
        self.player = player
        self.turn = Camp.CHO
        self.cho_score = self.han_score = 0.0
        self._initialize_board(cho_formation, han_formation)

    def make_move(self, origin: Grid, dest: Grid, piece_type: PieceType):
        # validate the given move
        if not self._validate_move(origin, dest, piece_type):
            print("the move cannot be made!")
            return

        # detenmine if game's over
        game_over = False
        dest_piece = self.board.get(dest.row, dest.col)
        if dest_piece and dest_piece.piece_type == PieceType.GENERAL:
            game_over = True

        # make the move
        piece = self.board.get(origin.row, origin.col)
        self.board.remove(origin.row, origin.col)
        self.board.put(dest.row, dest.col, piece)

        # update cho and han's scores
        self._update_scores()

        # switch "turn"
        self.turn = self.turn.opponent

        print(self.board)

        return game_over

    def get_all_destinations(self, origin: Grid):
        move_sets = self._get_possible_move_sets(origin)
        all_dest = [ms.get_dest(self.board, origin, self.turn)
                    for ms in move_sets]
        return all_dest

    def _initialize_board(self, cho_formation: Formation, han_formation: Formation):
        self.board = Board()
        cho_board = cho_formation.make_board()
        han_board = han_formation.make_board()
        cho_board.mark_camp(Camp.CHO)
        han_board.mark_camp(Camp.HAN)
        if self.player == Camp.CHO:
            han_board.rotate()
        else:
            cho_board.rotate()

        self.board.merge(cho_board)
        self.board.merge(han_board)
        self._update_scores()

    def _update_scores(self):
        self.cho_score = self.board.get_score(Camp.CHO)
        self.han_score = self.board.get_score(
            Camp.HAN) + constants.HAN_ADVANTAGE

    def _get_possible_move_sets(self, origin: Grid):
        def is_out_of_bound(grid: Grid):
            return (grid.row < constants.MIN_ROW or grid.row > constants.MAX_ROW or
                    grid.col < constants.MIN_COL or grid.col > constants.MAX_COL)

        piece = self.board.get(origin.row, origin.col)
        # Invalidate when given grids are out of bound
        if is_out_of_bound(origin):
            return []

        # Invalidate when no piece is on "origin" grid
        if not piece:
            return []

        if piece.camp != self.turn:
            return []

        # Get MoveSets based on piece type
        if piece.piece_type == PieceType.SOLDIER:
            move_sets = piece.get_soldier_move_sets(self.player == self.turn)
        elif piece.piece_type == PieceType.HORSE or piece.piece_type == PieceType.ELEPHANT:
            move_sets = piece.get_jumpy_move_sets()
        elif piece.piece_type == PieceType.CHARIOT or piece.piece_type == PieceType.CANNON:
            move_sets = piece.get_straight_move_sets(origin, piece.piece_type)
        elif piece.piece_type == PieceType.GENERAL or piece.piece_type == PieceType.GUARD:
            move_sets = piece.get_jumpy_move_sets(
                origin, self.player == self.turn)

        move_sets = [ms for ms in move_sets if ms.is_valid(
            self.board, origin, self.turn)]
        return move_sets

    def _validate_move(self, origin: Grid, dest: Grid, piece_type: PieceType):
        def _is_out_of_bound(grid: Grid):
            return (grid.row < constants.MIN_ROW or grid.row > constants.MAX_ROW or
                    grid.col < constants.MIN_COL or grid.col > constants.MAX_COL)

        origin_piece = self.board.get(origin.row, origin.col)
        dest_piece = self.board.get(dest.row, dest.col)
        # Invalidate when given grids are out of bound
        if _is_out_of_bound(origin) or _is_out_of_bound(dest):
            return False

        # Invalidate when no piece is on "origin" grid
        if not origin_piece:
            return False

        # Invalidate when piece type is wrong
        if origin_piece.piece_type != piece_type:
            return False

        # Invalidate when wrong camp
        if origin_piece.camp != self.turn:
            return False

        # Invalidate when ally piece is already on "dest" grid
        if dest_piece and dest_piece.camp == origin_piece.camp:
            return False

        # See if destination is in list of all possible destinatins from origin
        all_dest = self.getAllDestinations(origin)
        if dest not in all_dest:
            return False

        # TODO: Invalidate the move makes it enemy's "Janggun"
        return True

    def _get_soldier_move_sets(self, origin: Grid):
        piece = self.board.get(origin.row, origin.col)
        return piece.get_soldier_move_sets(self.player == self.turn)

    def _get_castle_move_sets(self, origin: Grid):
        piece = self.board.get(origin.row, origin.col)
        return piece.get_jumpy_move_sets(origin, self.player == self.turn)

    def _get_jumpy_move_sets(self, origin: Grid):
        piece = self.board.get(origin.row, origin.col)
        return piece.get_jumpy_move_sets()

    def _get_straight_move_sets(self, origin: Grid, piece_type: PieceType):
        piece = self.board.get(origin.row, origin.col)
        return piece.get_straight_move_sets(origin, piece_type)
