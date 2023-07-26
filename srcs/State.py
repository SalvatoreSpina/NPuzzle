import numpy as np
from random import choice


class State:
    def __init__(self, matrix):
        """
        Initialize the State object.

        Args:
            matrix (List[List[int]]): The matrix representing the state.
        """
        self.matrix = matrix
        self.parent = None
        self.h_total = 0
        self.h_misplaced = 0
        self.h_manhattan = 0
        self.g = 0
        self.zero_tile = self.find_zero()

    def find_zero(self):
        """
        Find the coordinates of the zero tile (empty cell) in the state.

        Returns:
            Tuple[int, int]: The coordinates of the zero tile.
        """
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == 0:
                    return y, x

    def can_puzzle_be_solved(self, puzzle):
        """
        Check if the current state of the puzzle can be solved.

        This is based on the principle that a puzzle state is solvable if the 
        number of inversions is even, considering also the distance of the empty 
        space from the center of the puzzle.

        Args:
            puzzle (Puzzle): An instance of the Puzzle class representing the 
                            current puzzle.

        Returns:
            bool: True if the puzzle can be solved, False otherwise.
        """

        total_inversions = 0
        for row_index in range(len(self.matrix)):
            for column_index, item in enumerate(self.matrix[row_index]):
                if item == 0:
                    zero_row = row_index
                    zero_column = column_index
                column_index_2, row_index_2 = column_index + 1, row_index
                while row_index_2 < puzzle.size:
                    while column_index_2 < puzzle.size:
                        if not (self.matrix[row_index_2][column_index_2] in puzzle.goal_array[(puzzle.goal[item])[0]][puzzle.goal[item][1]:]) \
                        and not any(self.matrix[row_index_2][column_index_2] in row for row in puzzle.goal_array[(puzzle.goal[item])[0]+1:][:]):
                            total_inversions += 1
                        column_index_2 += 1
                    row_index_2 += 1
                    column_index_2 = 0

        return (total_inversions + puzzle.size) % 2 is not (abs(puzzle.size // 2 - zero_column) + abs(puzzle.size // 2 - zero_row)) % 2

    def get_neighbours(self, puzzle):
        """
        Generate and return the neighbor states.

        Args:
            puzzle (Puzzle): The puzzle object representing the game.

        Returns:
            Tuple: A tuple containing the neighbor states and zero tile coordinates.
        """
        y, x = self.zero_tile
        if self.parent:
            yp, xp = self.parent.zero_tile
        neighbour_coords = _get_neighbour_coordinates(puzzle.size, y, x)
        neighbours = []
        zero_locs = []

        for i in range(len(neighbour_coords)):
            y2, x2 = neighbour_coords[i]
            if self.parent and (y2, x2) == (yp, xp):
                continue
            neighbour_matrix = np.copy(self.matrix)
            neighbour_matrix[y][x], neighbour_matrix[y2][x2] = neighbour_matrix[y2][x2], neighbour_matrix[y][x]
            neighbours.append(neighbour_matrix)
            zero_locs.append((y2, x2))

        return tuple(zip(neighbours, zero_locs))


def _get_neighbour_coordinates(size, y, x):
    """
    Get the coordinates of the neighboring cells for a given cell.

    Args:
        size (int): The size of the puzzle grid.
        y (int): The y-coordinate of the cell.
        x (int): The x-coordinate of the cell.

    Returns:
        List[Tuple[int, int]]: The coordinates of the neighboring cells.
    """
    return [
        (y2, x2)
        for y2, x2 in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        if 0 <= y2 < size and 0 <= x2 < size
    ]
