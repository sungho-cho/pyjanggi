import logging
import random
import time

from janggi import Camp
from janggi import Formation
from janggi import Location
from janggi import GameLog
from janggi import JanggiGame
from janggi import GameWindow
from janggi import ReplayViewer

logging.basicConfig()
logging.root.setLevel(logging.INFO)

if __name__ == '__main__':
    camp = Camp(random.choice([-1, 1]))
    cho_formation = Formation(random.randint(1, 4))
    han_formation = Formation(random.randint(1, 4))
    game = JanggiGame(camp, cho_formation, han_formation)
    print(f"cho: {game.cho_score} / han: {game.han_score}")
    print(game.board)

    # Test replay viewer
    moves = [(Location(3,0), Location(3,1)), (Location(6,8), Location(6,7)), (Location(0,0), Location(4,0))]
    game_log = GameLog(cho_formation, han_formation, camp, moves)
    replay_viewer = ReplayViewer(game_log)
    replay_viewer.run()