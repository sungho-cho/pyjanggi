import logging
import pygame
from pygame.locals import *

from ..game.game_log import GameLog
from .game_window import GameWindow


class ReplayViewer:
    """Display replay of a single game using GameWindow."""

    def __init__(self, game_log: GameLog):
        self.window = GameWindow(game_log.board_log[0])
        self.game_log = game_log

    def run(self):
        self.window.render()
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                self.window.close()
            if event.type == KEYDOWN:
                try:
                    if event.key == K_ESCAPE:
                        self.window.close()
                        return
                    elif event.key == K_RIGHT:
                        board = self.game_log.next()
                        self.window.switch_board(board)
                        self.window.render()
                    elif event.key == K_LEFT:
                        board = self.game_log.prev()
                        self.window.switch_board(board)
                        self.window.render()
                except StopIteration:
                    logging.info("Reached end of the game log.")
