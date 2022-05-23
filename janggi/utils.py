import logging
import random

from .base.camp import Camp
from .base.formation import Formation
from .game.janggi_game import JanggiGame
from .game.game_log import GameLog
from .ui.game_player import GamePlayer
from .ui.replay_viewer import ReplayViewer
from .proto import log_pb2

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)


def replay(filepath: str):
    """
    Replay a game by parsing the log file at the given path.

    Args:
        filepath (str): Path of the proto-serialized log file.
    """
    log_file = open(filepath, "rb")
    log_proto = log_pb2.Log()
    log_proto.ParseFromString(log_file.read())
    game_log = GameLog.from_proto(log_proto)
    game_log.generate_board_log()
    replay_viewer = ReplayViewer(game_log)
    replay_viewer.run()


def play(game: JanggiGame):
    """
    Play a game by running GamePlayer.

    Args:
        game (JanggiGame): Pre-initialized game to play.
    """
    player = GamePlayer(game)
    player.run()


def generate_random_game():
    """Generate a random Janggi game."""
    camp = Camp(random.choice([-1, 1]))
    cho_formation = Formation(random.randint(1, 4))
    han_formation = Formation(random.randint(1, 4))
    return JanggiGame(camp, cho_formation, han_formation)
