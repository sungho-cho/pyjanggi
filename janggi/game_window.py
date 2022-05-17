import logging
import os
import pkg_resources
import pygame

from .board import Board
from .camp import Camp
from .piece import Piece, PieceType
from .constants import MIN_ROW, MAX_ROW, MIN_COL, MAX_COL

WIDTH, HEIGHT = 500, 500
BOARD_WIDTH, BOARD_HEIGHT = 500, 500
PIECE_WIDTH, PIECE_HEIGHT = 40, 40
ROW_MARGIN, COL_MARGIN = 10, 10
ROW_GAP, COL_GAP = 50, 55
IMG_PATH = "images/"
BOARD_FILENAME = "board.png"

class GameWindow:
    def __init__(self, board: Board = None):
        pygame.init()
        pygame.display.set_caption("Janggi")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = board
        self.board_img = None
        self.piece_imgs = {Camp.CHO: {}, Camp.HAN: {}}

        self._initialize_board_image()
        self._initialize_piece_images()

    def render(self):
        self.display.blit(self.board_img, (0, 0))
        if self.board:
            for row in range(MIN_ROW, MAX_ROW+1):
                for col in range(MIN_COL, MAX_COL+1):
                    if self.board.get(row,col):
                        piece = self.board.get(row,col)
                        if piece.camp is None:
                            logging.warning(f"(GameWindow) Camp is not assigned for piece {piece.piece_type}")
                            continue
                        piece_img = self.piece_imgs[piece.camp][piece.piece_type]
                        (x, y) = (COL_MARGIN + COL_GAP * col, ROW_MARGIN + ROW_GAP * row)
                        self.display.blit(piece_img, (x, y))
                        
        pygame.display.update()
    
    def _initialize_board_image(self):
        board_path = os.path.join(IMG_PATH, BOARD_FILENAME)
        board_file = pkg_resources.resource_filename(__name__, board_path)
        board_img = pygame.image.load(board_file)
        self.board_img = pygame.transform.scale(board_img, (BOARD_WIDTH, BOARD_HEIGHT))

    def _initialize_piece_images(self):
        for camp in Camp:
            if camp == Camp.UNDEDCIDED:
                continue
            for piece_type in PieceType:
                piece_path = self._camp_piece_type_to_image_path(camp, piece_type)
                piece_file = pkg_resources.resource_filename(__name__, piece_path)
                piece_img = pygame.image.load(piece_file)
                self.piece_imgs[camp][piece_type] = pygame.transform.scale(
                    piece_img, (PIECE_WIDTH, PIECE_HEIGHT))

    def _camp_piece_type_to_image_path(self, camp: Camp, piece_type: PieceType):
        filename = f"{camp.name.lower()}_{piece_type.name.lower()}.png"
        return os.path.join(IMG_PATH, filename)

    def _piece_to_image_path(self, piece: Piece):
        if piece.camp is None:
            logging.warning(f"(GameWindow) Camp is not assigned for piece {piece.piece_type}")
        return self._camp_piece_type_to_image_path(piece.camp, piece.piece_type)
