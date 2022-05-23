import pygame

GREEN = (0, 255, 0)

class BoardMarker:
    def __init__(self, screen, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(self.screen, GREEN, (self.x, self.y), 10)