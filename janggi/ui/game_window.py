import logging
import os
import pkg_resources
import pygame
from typing import List, Optional

from ..base.board import Board
from ..base.camp import Camp
from ..base.location import Location
from ..base.piece import PieceType
from ..constants import MIN_ROW, MAX_ROW, MIN_COL, MAX_COL
from .marker import BoardMarker

WIDTH, HEIGHT = 500, 500
BOARD_WIDTH, BOARD_HEIGHT = 500, 500
PIECE_WIDTH, PIECE_HEIGHT = 40, 40
BOARD_Y, BOARD_X = 10, 10
ROW_GAP, COL_GAP = 50, 55
IMG_PATH = "images/"
BOARD_FILENAME = "board.png"

class GameWindow:
    """Class that renders board display using pygame."""
    def __init__(self, board: Optional[Board] = None):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("Janggi")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = board
        self.board_img = None
        self.piece_imgs = {Camp.CHO: {}, Camp.HAN: {}}
        self.board_markers = []

        self._initialize_board_image()
        self._initialize_piece_images()

    def render(self):
        self.display.blit(self.board_img, (0, 0))
        # Draw pieces
        if self.board:
            for row, col in self.board.get_piece_locations():
                piece = self.board.get(row,col)
                if piece.camp is None:
                    logging.warning(f"(GameWindow) Camp is not assigned for piece {piece.piece_type}")
                    continue
                piece_img = self.piece_imgs[piece.camp][piece.piece_type]
                x, y = self.get_board_xy(row, col)
                self.display.blit(
                    piece_img, 
                    (
                        x - PIECE_WIDTH // 2, 
                        y - PIECE_HEIGHT // 2
                    )
                )
        # Draw markers
        for marker in self.board_markers:
            marker.draw()

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.quit()

    def switch_board(self, board: Board):
        self.board = board
        pygame.event.pump()

    def get_board_xy(self, row: int, col: int):
        return (
            BOARD_X + COL_GAP * col + PIECE_WIDTH // 2, 
            BOARD_Y + ROW_GAP * row + PIECE_HEIGHT // 2
        )
    
    def _initialize_board_image(self):
        board_path = os.path.join(IMG_PATH, BOARD_FILENAME)
        board_file = pkg_resources.resource_filename(__name__, board_path)
        board_img = pygame.image.load(board_file)
        self.board_img = pygame.transform.scale(board_img, (BOARD_WIDTH, BOARD_HEIGHT))

    def _initialize_piece_images(self):
        for camp in Camp:
            if camp == Camp.UNDECIDED:
                continue
            for piece_type in PieceType:
                piece_path = self._get_image_path(camp, piece_type)
                piece_file = pkg_resources.resource_filename(__name__, piece_path)
                piece_img = pygame.image.load(piece_file)
                self.piece_imgs[camp][piece_type] = pygame.transform.scale(
                    piece_img, (PIECE_WIDTH, PIECE_HEIGHT))

    def _get_image_path(self, camp: Camp, piece_type: PieceType):
        filename = f"{camp.name.lower()}_{piece_type.name.lower()}.png"
        return os.path.join(IMG_PATH, filename)
