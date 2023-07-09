import sys
import argparse
import numpy as np


class Parser:
    def __init__(self):
        """
        Initialize the Parser object.
        """
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description="* npuzzle solver using A* pathfinding *\n\nif no heuristic flags are chosen, "
                        "defaults to both Manhattan distance and linear conflict heuristics"
        )
        self._add_arguments()

    def _add_arguments(self):
        """
        Add command-line arguments to the parser.
        """
        self.parser.add_argument(
            "filepath",
            nargs="?",
            help="path to input file. If none is specified, the user will be prompted for puzzle generation input",
        )
        self.parser.add_argument(
            "--greedy",
            "-g",
            help="find a path as fast as possible, not guaranteed to be the shortest solution",
            action="store_true",
        )
        self.parser.add_argument(
            "--uniform",
            "-u",
            help="find the shortest path with no heuristic, only the cost",
            action="store_true",
        )
        self.parser.add_argument(
            "--verbose",
            "-v",
            help="show key steps in output",
            action="store_true",
        )
        self.parser.add_argument(
            "--misplaced",
            "-m",
            help="use the misplaced tiles heuristic",
            action="store_true",
        )
        self.parser.add_argument(
            "--manhattan",
            "-t",
            help="use the Manhattan distance heuristic",
            action="store_true",
        )
        self.parser.add_argument(
            "--euclidean",
            "-e",
            help="use the Euclidean distance heuristic",
            action="store_true",
        )

    def parse_arguments(self):
        """
        Parse the command-line arguments.

        Returns:
            args: The parsed arguments.
        """
        args = self.parser.parse_args()

        # If no heuristic argument is provided, use Manhattan
        if True not in (args.misplaced, args.manhattan, args.euclidean):
            args.manhattan = True

        return args


def parse_input_file(filepath):
    """
    Parse the input file and extract the puzzle size and initial state.

    Args:
        filepath (str): Path to the input file.

    Returns:
        puzzle_size (int): Size of the puzzle.
        start_state (numpy.ndarray): Initial state of the puzzle.
    """
    try:
        with open(filepath, "r") as input_file:
            start_state = []
            puzzle_size = None
            lines = input_file.readlines()
            for line in lines:
                # Ignore everything after a '#'
                line = line.split("#")[0]

                values = []
                tokens = line.split()
                for token in tokens:
                    if token.isdigit():
                        num = int(token)
                        if puzzle_size is None:
                            puzzle_size = num
                            if not 0 <= puzzle_size <= 100:
                                _handle_error(ValueError)
                        else:
                            values.append(num)
                    else:
                        _handle_error(SyntaxError)
                if values:
                    start_state.append(values)
    except Exception as e:
        _handle_error(e)

    start_state = np.array(start_state, dtype=np.uint16)

    # Check if the matrix is the right shape
    if np.shape(start_state) != (puzzle_size, puzzle_size):
        _handle_error(SyntaxError)

    # Check if the tile numbers are correct
    if not np.in1d(list(range(puzzle_size ** 2)), start_state).all():
        _handle_error(SyntaxError)

    return puzzle_size, start_state


def _handle_error(error):
    """
    Handle different types of errors and print appropriate error messages.

    Args:
        error: The error type.
    """
    if error == SyntaxError:
        print("Input file is not correctly formatted.")
    elif error == ValueError:
        print("Puzzle size must be between 3 and 100.")
    else:
        print(error)
    sys.exit()
