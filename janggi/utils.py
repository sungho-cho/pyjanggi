from .game.game_log import GameLog
from .game.replay_viewer import ReplayViewer
from .proto import log_pb2

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