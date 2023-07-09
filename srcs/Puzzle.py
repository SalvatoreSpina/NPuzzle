import numpy as np
from random import choice
from State import State


class Puzzle:
    def __init__(self, size):
        """
        Initialize the Puzzle object.

        Args:
            size (int): The size of the puzzle grid.
        """
        self.size = size
        self.goal_array = np.array(self._generate_goal_array(self.size, self.size, 1), dtype=np.uint16)
        self.goal = [None] * (self.size ** 2)
        self.get_goal()

    def _generate_goal_array(self, rows, cols, start_value):
        """
        Recursively generate the goal array for the puzzle.

        Args:
            rows (int): The number of rows.
            cols (int): The number of columns.
            start_value (int): The starting value for the array.

        Returns:
            List[List[int]]: The generated goal array.
        """
        if rows == 1 and cols == 1:
            return [[0]]
        return (
            [list(range(start_value, start_value + cols))]
            + [list(reversed(x)) for x in zip(*self._generate_goal_array(cols, rows - 1, start_value + cols))]
            if cols > 0
            else [[0]]
        )

    def get_goal(self):
        """
        Generate the goal positions for each tile value in the puzzle.
        """
        for y, row in enumerate(self.goal_array):
            for x, value in enumerate(row):
                self.goal[value] = (y, x)

    def shuffle(self, state, amount):
        """
        Shuffle the puzzle by performing random moves.

        Args:
            state (State): The current state of the puzzle.
            amount (int): The number of shuffling moves to perform.

        Returns:
            State: The shuffled state.
        """
        for _ in range(amount):
            neighbours, zero_loc = choice(state.get_neighbours(self))
            neighbour = State(neighbours)
            neighbour.zero_tile = zero_loc
            state = neighbour
        return state
