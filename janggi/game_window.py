from turtle import window_height
import os
import pkg_resources
import pygame

from .board import Board

WIDTH, HEIGHT = 500, 500
BOARD_WIDTH, BOARD_HEIGHT = 500, 500
IMG_PATH = "images/"
BOARD_FILENAME = "board.png"

class GameWindow:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Janggi")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self._initialize_board()
    
    def _initialize_board(self):
        board_path = os.path.join(IMG_PATH, BOARD_FILENAME)
        board_file = pkg_resources.resource_filename(__name__, board_path)
        board_img = pygame.image.load(board_file)
        self.board_img = pygame.transform.scale(board_img, (BOARD_WIDTH, BOARD_HEIGHT))

    def render(self):
        self.display.blit(self.board_img, (0, 0))
        pygame.display.update()
