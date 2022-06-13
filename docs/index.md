# janggi package

## Subpackages
* [janggi.base package](#janggibase-package)
  * [janggi.base.board module](#janggibaseboard-module)
  * [janggi.base.camp module](#janggibasecamp-module)
  * [janggi.base.formation module](#janggibaseformation-module)
  * [janggi.base.location module](#janggibaselocation-module)
  * [janggi.base.move module](#janggibasemove-module)
  * [janggi.base.piece module](#janggibasepiece-module)
* [janggi.game package](#janggigame-package)
  * [janggi.game.game_log module](#janggigamegamelog-module)
  * [janggi.game.janggi_game module](#janggigamejanggigame-module)
* [janggi.proto package](#janggiproto-package)
  * [janggi.proto.log_pb2 module](#janggiprotologpb2-module)
* [janggi.ui package](#janggiui-md)
  * [janggi.ui.game_player module](#janggiuigameplayer-module)
  * [janggi.ui.game_window module](#janggiuigamewindow-module)
  * [janggi.ui.marker module](#janggiuimarker-module)
  * [janggi.ui.replay_viewer module](#janggiuireplayviewer-module)
* [janggi.utils module](#janggiutils-module)


# janggi.base package


## janggi.base.board module


### _class_ janggi.base.board.Board(cho_formation, han_formation, bottom_camp)
Bases: `object`

Simple board class used for the game of Janggi. Contains and handles a single 
10x9 two-dimensional list that contains either a Piece object or None.


#### \__init__(cho_formation, han_formation, bottom_camp)

#### copy()
Return a copied Board class.

Returns:

    Board: Copied version of the board.
* **Return type**

    `Board`



#### _classmethod_ full_board_from_formations(cho_formation, han_formation, player)
Return Board class instance that represents a full board.

Args:

    cho_formation (Formation): Formation of Camp Cho.
    han_formation (Formation): Formation of Camp Han.
    player (Camp): Camp that the player is playing. This is used to assign that camp as the bottom camp.

Returns:

    Board: Full Board class.
* **Return type**

    `Board`



#### get(row, col)
Return the piece that is located at the given location of the board.

Args:

    row (int): Row of piece.
    col (int): Column of piece.

Returns:

    Piece: Piece located at (row,col) on the board. Can be None.
* **Return type**

    `Piece`



#### get_piece_locations()
Get locations of all pieces on the board.

Returns:

    List[Location]: List of all locations of the pieces on the board.
* **Return type**

    `List`[`Location`]



#### get_piece_locations_for_camp(camp)
Get locations of all pieces with the given camp.

Args:

    camp (Camp): Camp of the pieces to fetch.

Returns:

    List[Location]: List of all locations of the pieces with the given camp.
* **Return type**

    `List`[`Location`]



#### get_score(camp)
Return score for the player who’s playing the given camp.

Args:

    camp (Camp): Camp of the player whose score will be calculated.

Returns:

    int: Score of the player who’s playing the given camp.
* **Return type**

    `int`



#### mark_camp(camp)
Mark all pieces on the board with the given camp (CHO or HAN).
Used to mark half-boards when setting up initial boards.

Args:

    camp (Camp): Camp enum to mark pieces with.


#### merge(board)
Merge the given board into self.__board by overwriting.

Args:

    board (Board): Input board that will be merged into self.__board.


#### move(origin, dest)
Move piece from origin to destination and return the piece that was
originally placed at the given dest.

Args:

    origin (Location): Original location of the piece being played.
    dest (Location): Destination of the piece being played.
* **Return type**

    `Optional`[`Piece`]



#### put(row, col, piece)
Put piece into board at the given (row,col) location.
Used row and col as inputs instead of Location to make it easier to generate
initial boards in formation.py.

Args:

    row (int): Row that the given piece that will placed on.
    col (int): Column that the given piece that will be placed on.
    piece (Piece): Piece that will be placed on the board.


#### remove(row, col)
Remove piece at the given location of the board.

Args:

    row (int): Row of the piece to be removed.
    col (int): Column of the piece to be removed.


#### rotate()
Rotate the board 180 degrees and update self.__board.


## janggi.base.camp module


### _class_ janggi.base.camp.Camp(value)
Bases: `IntEnum`

Enum that represents two sides of the game of Janggi.
It’s just like black and white in chess except it’s called cho and han.


#### CHO(_ = _ )

#### HAN(_ = -_ )

#### UNDECIDED(_ = _ )

#### _classmethod_ from_proto(camp_proto)
Convert from proto Camp enum.


#### _property_ opponent(_: Cam_ )
Return opponent’s enum. (Camp.CHO for Camp.HAN / Camp.HAN for Camp.CHO).

Returns:

    Camp: Opponent’s enum instance.
* **Return type**

    `Camp`



#### to_proto()
Convert to proto Camp enum.


## janggi.base.formation module


### _class_ janggi.base.formation.Formation(value)
Bases: `IntEnum`

Enum class that represents 4 different formations of the game of Janggi.
See [https://en.wikipedia.org/wiki/Janggi#Setting_up](https://en.wikipedia.org/wiki/Janggi#Setting_up) for details on formations.
In Korean terminology,
the inner elephant setup is called Won-Ang-Ma,
the outer elephant setup is called Yang-Gwi-Ma,
the left elephant and right elephant setup are called Gwi-Ma.


#### INNER_ELEPHANT(_ = _ )

#### LEFT_ELEPHANT(_ = _ )

#### OUTER_ELEPHANT(_ = _ )

#### RIGHT_ELEPHANT(_ = _ )

#### UNDECIDED(_ = _ )

#### _classmethod_ from_proto(formation_proto)
Convert from proto Formation enum.


#### to_proto()
Convert to proto Formation enum.

## janggi.base.location module


### _class_ janggi.base.location.Location(row, col)
Bases: `object`

Location class that each represents a single location on the board grid.


#### \__init__(row, col)
Initialize location.

Args:

    row (int): row number in range 0 <= row <= 9.
    col (int): column number in range 0 <= col <= 8.

Raises:

    Exception: row is out of range.
    Exception: column is out of range.


#### _classmethod_ from_proto(location_proto)
Convert from proto Location message.
* **Return type**

    `Location`



#### to_proto()
Convert to proto Location message.
* **Return type**

    [`Location`](janggi.proto.md#janggi.proto.log_pb2.Location)


## janggi.base.move module


### _class_ janggi.base.move.MoveSet(moves)
Bases: `object`

MoveSet is a list of a piece’s moves in order to complete a single action.
MoveSet ~ [(dr1, dc1), (dr2, dc2), (dr3, dc3), …].
If a player makes an action to move a Chariot piece 3 tiles up,
its move set will be [(-1,0), (-1,0), (-1,0)].


#### \__init__(moves)
Initialize MoveSet with the given list of moves.


#### get_dest(board, origin, player)
Get destination location of piece at given origin location for the given player.

Args:

    board (Board): Current board being played.
    origin (Location): Original location of the piece being played.
    player (Camp): Current player to make an action.

Returns:

    Location: Destination of the piece if it’s played through self.moves from origin.
* **Return type**

    `Location`



#### is_valid(board, origin, player)
Check validity of a move set for piece at the given origin for the given player.

Args:

    board (Board): Current board being played.
    origin (Location): Original location of the piece being played.
    player (Camp): Current player to make an action.

Returns:

    bool: True if move set is valid; False otherwise
* **Return type**

    `bool`


## janggi.base.piece module


### _class_ janggi.base.piece.Piece(piece_type)
Bases: `object`

Piece class represents a single piece on the game board.
The class is capable of getting move sets based on its piece type.


#### \__init__(piece_type)
Initialize Piece class by setting the given piece type.
Camp attribute is later initialized by Board.mark_camp.


#### get_castle_move_sets(origin, is_player)
Get move sets for castle pieces (generals and guards).
The directions a soldier piece can take depends on which camp it belongs to.

Args:

    origin (Location): Original location of the piece.
    is_player (bool): True if the piece belongs to the main player; False otherwise.

Returns:

    List[MoveSet]: All move sets a castle piece can make regardless of validity.
* **Return type**

    `List`[`MoveSet`]



#### get_jumpy_move_sets()
Get move sets for jumpy pieces (horses and elephants).

Returns:

    List[MoveSet]: All move sets a jumpy piece can make regardless of validity.
* **Return type**

    `List`[`MoveSet`]



#### get_soldier_move_sets(origin, is_player)
Get move sets for soldier pieces.
The directions a soldier piece can take depends on which camp it belongs to.

Args:

    is_player (bool): True if the piece belongs to the main player; False otherwise.

Returns:

    List[MoveSet]: All move sets a soldier piece can make regardless of validity.
* **Return type**

    `List`[`MoveSet`]



#### get_straight_move_sets(origin)
Get move sets for straight pieces (chariots and cannons).

Args:

    origin (Location): Original location of the piece.

Returns:s

    List[MoveSet]: All move sets a straight piece can make regardless of validity.
* **Return type**

    `List`[`MoveSet`]



#### _property_ value(_: in_ )
Return piece’s value based on its piece type. Each piece in Janggi has a 
value assigned, and the values contribute to the players’ current scores.

Returns:

    int: piece’s value based on type.
* **Return type**

    `int`



### _class_ janggi.base.piece.PieceType(value)
Bases: `Enum`

Enum class representing a piece’s type.


#### CANNON(_ = _ )

#### CHARIOT(_ = _ )

#### ELEPHANT(_ = _ )

#### GENERAL(_ = _ )

#### GUARD(_ = _ )

#### HORSE(_ = _ )

#### SOLDIER(_ = _ )


# janggi.ui package

## janggi.ui.game_player module


### _class_ janggi.ui.game_player.GamePlayer(game)
Bases: `object`

Class used to play the game.


#### \__init__(game)

#### run()

### _class_ janggi.ui.game_player.MoveSelection(origin, dest)
Bases: `object`


#### \__init__(origin, dest)
## janggi.ui.game_window module


### _class_ janggi.ui.game_window.GameWindow(board=None)
Bases: `object`

Class that renders board display using pygame.


#### \__init__(board=None)

#### close()

#### get_board_xy(row, col)

#### render()

#### switch_board(board)
## janggi.ui.marker module


### _class_ janggi.ui.marker.BoardMarker(screen, x, y)
Bases: `object`


#### \__init__(screen, x, y)

#### draw()
## janggi.ui.replay_viewer module


### _class_ janggi.ui.replay_viewer.ReplayViewer(game_log)
Bases: `object`

Display replay of a single game using GameWindow.


#### \__init__(game_log)

#### run()


# janggi.proto package


## janggi.proto.log_pb2 module

Generated protocol buffer code.


### _class_ janggi.proto.log_pb2.Location()
Bases: `CMessage`, `Message`


#### DESCRIPTOR(_ = <google.protobuf.pyext._message.MessageDescriptor object_ )
The `google.protobuf.descriptor.Descriptor` for this message type.


#### col()
Field janggi.Location.col


#### row()
Field janggi.Location.row


### _class_ janggi.proto.log_pb2.Log()
Bases: `CMessage`, `Message`


#### DESCRIPTOR(_ = <google.protobuf.pyext._message.MessageDescriptor object_ )
The `google.protobuf.descriptor.Descriptor` for this message type.


#### bottom_camp()
Field janggi.Log.bottom_camp


#### cho_formation()
Field janggi.Log.cho_formation


#### han_formation()
Field janggi.Log.han_formation


#### moves()
Field janggi.Log.moves


### _class_ janggi.proto.log_pb2.Move()
Bases: `CMessage`, `Message`


#### DESCRIPTOR(_ = <google.protobuf.pyext._message.MessageDescriptor object_ )
The `google.protobuf.descriptor.Descriptor` for this message type.


#### dest()
Field janggi.Move.dest


#### origin()
Field janggi.Move.origin


# janggi.game package


## janggi.game.game_log module


### _class_ janggi.game.game_log.GameLog(cho_formation, han_formation, bottom_camp, moves=[])
Bases: `object`

Simple class that represents list of moves made in a janggi game.


#### \__init__(cho_formation, han_formation, bottom_camp, moves=[])

#### add_move(move)
Add a single move to the move log

Args:

    move (Tuple[Location ,Location]): _description_


#### _classmethod_ from_proto(log_proto)
Convert from proto Log message.


#### generate_board_log()

#### next()
Used to access the next board when iterating through self.board_logs.
* **Return type**

    [`Board`](janggi.base.md#janggi.base.board.Board)



#### prev()
Used to access the previous board when iterating through self.board_logs.
* **Return type**

    [`Board`](janggi.base.md#janggi.base.board.Board)



#### to_proto()
Convert to proto Log message.


## janggi.game.janggi_game module


### _class_ janggi.game.janggi_game.JanggiGame(player, cho_formation, han_formation)
Bases: `object`

A game of Janggi with a game board, players, and scores.
With two public methods, this class can help make a single action on the board,
and it can also get all possible moves from a current state of the board.


#### \__init__(player, cho_formation, han_formation)
Initialize Janggi game instance.

Args:

    player (Camp): Camp that the main player is playing.
    cho_formation (Formation): Formation of camp cho.
    han_formation (Formation): Formation of camp han.


#### get_all_actions()
Get list of all possible moves that can be made for the current player.

Returns:

    List[Tuple[Location, Location]]: List of moves in (origin, dest) format 

        where it means a piece at origin location being moved to dest location.
* **Return type**

    `List`[`Tuple`[[`Location`](janggi.base.md#janggi.base.location.Location), [`Location`](janggi.base.md#janggi.base.location.Location)]]



#### get_all_destinations(origin)
List all possible locations where a piece at given origin can move to.

Args:

    origin (Location): Location of the piece to get destionations for.

Returns:

    List[Location]: List of all possible locations the piece can go to.
* **Return type**

    `List`[[`Location`](janggi.base.md#janggi.base.location.Location)]



#### make_action(origin, dest)
Move a piece from the given origin location to the given destination.

Args:

    origin (Location): Original location of the piece to be moved.
    dest (Location): Destination of the piece to be moved.

Raises:

    Exception: When the given action is invalid.

Returns:

    piece_value (float): An enemy piece’s value if it was killed; 0 otherwise.
    game_over (bool): True if the action ends the game; False otherwise.
* **Return type**

    `Tuple`[`float`, `bool`]


# janggi.utils module


### janggi.utils.generate_random_game()
Generate a random Janggi game.


### janggi.utils.play(game)
Play a game by running GamePlayer.

Args:

    game (JanggiGame): Pre-initialized game to play.


### janggi.utils.replay(filepath)
Replay a game by parsing the log file at the given path.

Args:

    filepath (str): Path of the proto-serialized log file.