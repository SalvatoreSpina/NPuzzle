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
        self.h_euclidean = 0
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

    def can_be_solved(self, puzzle):
        """
        Check if the state can be solved based on the number of inversions.

        Args:
            puzzle (Puzzle): The puzzle object representing the game.

        Returns:
            bool: True if the state can be solved, False otherwise.
        """
        inversions = 0
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] == 0:
                    zero_row = y
                    zero_col = x
                for y2 in range(y, puzzle.size):
                    start_x = x + 1 if y2 == y else 0
                    for x2 in range(start_x, puzzle.size):
                        if not (
                            self.matrix[y2][x2] in puzzle.goal_array[(puzzle.goal[self.matrix[y][x]])[0]][
                                puzzle.goal[self.matrix[y][x]]][1:]
                        ) and not any(
                            self.matrix[y2][x2]
                            in row
                            for row in puzzle.goal_array[(puzzle.goal[self.matrix[y][x]])[0] + 1 :][:]
                        ):
                            inversions += 1

        if (
            (inversions + puzzle.size) % 2
            != (abs(puzzle.size // 2 - zero_col) + abs(puzzle.size // 2 - zero_row)) % 2
        ):
            return True
        return False

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
