# PyJanggi

<img width="400" alt="Screen Shot 2022-06-13 at 6 04 29 PM" src="https://user-images.githubusercontent.com/46757971/173320609-075acc71-0f0a-47d6-9082-2418ca2775e8.png">

PyJanggi is a Python library for a Korean chess called [Janggi](https://en.wikipedia.org/wiki/Janggi).
It provides functionalities to simulate a game, maintain a game board, list all possible moves, make a move, and validate a move.

## Documentation
Check out the [GitHub Page](https://sungho-cho.github.io/pyjanggi/) for package documentation.

## Getting Started

### Using PyJanggi in Your Package

1. Install package via pip:
    `pip install janggi`

2. Import in your Python module:
    `import janggi`

    You can also import inner modules:
    `from janggi import JanggiGame, generate_random_game`

3. Call methods to the `JanggiGame` class instance to play the game.

    3 public methods are:
    - `make_action(self, origin: Location, dest: Location) -> Tuple[float, bool]`
    - `get_all_actions(self) -> List[Tuple[Location, Location]]`
    - `get_all_destinations(self, origin: Location) -> List[Location]`

    Check out the [Documentation](#documentation) section for more details

### Testing Functionality
PyJanggi is originally designed to be imported by other packages and provide Janggi game logic and classes, but if you want to check if the PyJanggi package is working, you can follow these steps:

1. Clone the repository:

    `git clone https://github.com/sungho-cho/pyjanggi.git`

2. Install dependencies:

    `pip install -r requirements.txt`

3. Run `main.py`:

    `python janggi/main.py`

    If you see the UI window and can navigate with left and right arrow keys, your PyJanggi package is working!



## Releases
Check out the [PyPi Package](https://pypi.org/project/janggi) for releases

## License
[MIT License](LICENSE)
