import random

from janggi.janggi_game import JanggiGame
from janggi.camp import Camp
from janggi.formation import Formation

if __name__ == '__main__':
    camp = Camp(random.choice([-1, 1]))
    cho_formation = Formation(random.randint(1, 4))
    han_formation = Formation(random.randint(1, 4))
    game = JanggiGame(camp, cho_formation, han_formation)
    print(f"cho: {game.cho_score} / han: {game.han_score}")
    print(game.board)
