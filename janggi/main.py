import random
import time

from janggi.janggi_game import JanggiGame
from janggi.camp import Camp
from janggi.formation import Formation
from janggi.game_window import GameWindow

if __name__ == '__main__':
    camp = Camp(random.choice([-1, 1]))
    cho_formation = Formation(random.randint(1, 4))
    han_formation = Formation(random.randint(1, 4))
    game = JanggiGame(camp, cho_formation, han_formation)
    print(f"cho: {game.cho_score} / han: {game.han_score}")
    print(game.board)

    game_window = GameWindow()
    game_window.render()
    time.sleep(5)
