import numpy as np


class Heuristic:
    @staticmethod
    def misplaced_tiles(matrix, goal):
        """
        Calculate the number of misplaced tiles heuristic.

        Args:
            matrix (numpy.ndarray): The current state matrix.
            goal (dict): The goal state dictionary.

        Returns:
            int: The number of misplaced tiles.
        """
        h = 0
        for y, _ in enumerate(matrix):
            for x, _ in enumerate(matrix[y]):
                num = matrix[y][x]
                if num and (y, x) != goal[num]:
                    h += 1
        return h

    @staticmethod
    def misplaced_tile_single(state, goal):
        """
        Calculate the number of misplaced tiles heuristic for a single tile.

        Args:
            state (State): The current state.
            goal (dict): The goal state dictionary.

        Returns:
            int: The number of misplaced tiles.
        """
        h = state.parent.h_misplaced

        y, x = state.parent.zero_tile
        tile = state.matrix[y][x]
        y2, x2 = goal[tile]
        h += (y, x) != (y2, x2)

        y, x = state.zero_tile
        h -= (y, x) != (y2, x2)

        return h

    @staticmethod
    def manhattan_distance(matrix, goal):
        """
        Calculate the Manhattan distance heuristic.

        Args:
            matrix (numpy.ndarray): The current state matrix.
            goal (dict): The goal state dictionary.

        Returns:
            int: The Manhattan distance.
        """
        h = 0
        for y, _ in enumerate(matrix):
            for x, _ in enumerate(matrix[y]):
                if matrix[y][x]:
                    y2, x2 = goal[matrix[y][x]]
                    h += abs(x - x2) + abs(y - y2)
        return h

    @staticmethod
    def manhattan_dist_single(state, goal):
        """
        Calculate the Manhattan distance heuristic for a single tile.

        Args:
            state (State): The current state.
            goal (dict): The goal state dictionary.

        Returns:
            int: The Manhattan distance.
        """
        h = state.parent.h_manhattan

        y, x = state.parent.zero_tile
        tile = state.matrix[y][x]
        y2, x2 = goal[tile]
        h += abs(x - x2) + abs(y - y2)

        y, x = state.zero_tile
        h -= abs(x - x2) + abs(y - y2)

        return h

    @staticmethod
    def euclidean_distance(matrix, goal):
        """
        Calculate the Euclidean distance heuristic.

        Args:
            matrix (numpy.ndarray): The current state matrix.
            goal (dict): The goal state dictionary.

        Returns:
            float: The Euclidean distance.
        """
        h = 0
        for y, _ in enumerate(matrix):
            for x, _ in enumerate(matrix[y]):
                if matrix[y][x]:
                    y2, x2 = goal[matrix[y][x]]
                    h += np.sqrt((x - x2) ** 2 + (y - y2) ** 2)
        return h

    @staticmethod
    def euclidean_dist_single(state, goal):
        """
        Calculate the Euclidean distance heuristic for a single tile.

        Args:
            state (State): The current state.
            goal (dict): The goal state dictionary.

        Returns:
            float: The Euclidean distance.
        """
        h = state.parent.h_euclidean

        y, x = state.parent.zero_tile
        tile = state.matrix[y][x]
        y2, x2 = goal[tile]
        h += np.sqrt((x - x2) ** 2 + (y - y2) ** 2)

        y, x = state.zero_tile
        h -= np.sqrt((x - x2) ** 2 + (y - y2) ** 2)

        return h
