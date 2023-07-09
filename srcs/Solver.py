import sys
import heapq
import numpy as np
from Parser import Parser, parse_input_file
from Heuristics import Heuristic
from Puzzle import Puzzle
from State import State


class Solver:
    def __init__(self, args):
        """
        Initialize the Solver object.

        Args:
            args: Command-line arguments.
        """
        self.args = args

    def get_heuristics(self, state, puzzle):
        """
        Calculate and assign heuristics to the given state based on the provided arguments.

        Args:
            state (State): The current state of the puzzle.
            puzzle (Puzzle): The puzzle object representing the game.
        """
        if not self.args.uniform:
            if self.args.misplaced:
                state.h_misplaced = Heuristic.misplaced_tiles(state.matrix, puzzle.goal)
            if self.args.manhattan:
                state.h_manhattan = Heuristic.manhattan_distance(state.matrix, puzzle.goal)
            if self.args.euclidean:
                state.h_euclidean = Heuristic.euclidean_distance(state.matrix, puzzle.goal)

        state.h_total = state.h_misplaced + state.h_manhattan + state.h_euclidean

    def get_optimized_heuristics(self, state, puzzle):
        """
        Calculate and assign optimized heuristics to the given state based on the provided arguments.

        Args:
            state (State): The current state of the puzzle.
            puzzle (Puzzle): The puzzle object representing the game.
        """
        if not self.args.uniform:
            if self.args.misplaced:
                state.h_misplaced = Heuristic.misplaced_tile_single(state, puzzle.goal)
            if self.args.manhattan:
                state.h_manhattan = Heuristic.manhattan_dist_single(state, puzzle.goal)
            if self.args.euclidean:
                state.h_euclidean = Heuristic.euclidean_dist_single(state, puzzle.goal)

        state.h_total = state.h_misplaced + state.h_manhattan + state.h_euclidean

    def solve_puzzle(self):
        """
        Solve the puzzle based on the provided arguments.
        """
        shuffles_amount = 0
        if self.args.filepath:
            try:
                puzzle_size, start_state = parse_input_file(self.args.filepath)
            except Exception as e:
                _handle_error(e)
        else:
            puzzle_size = input("Please enter the n size of an n x n puzzle:\n")
            while not puzzle_size.isdigit() or not 3 <= int(puzzle_size) <= 100:
                print("Wrong input. Please enter a number between 3 and 100.")
                puzzle_size = input("Please enter the n size of an n x n puzzle:\n")

            shuffles_amount = input("How many times should the puzzle be shuffled?\n")
            while not shuffles_amount.isdigit() or int(shuffles_amount) < 1:
                print("Wrong input. Please enter a number above 0.")
                shuffles_amount = input("How many times should the puzzle be shuffled?\n")

        puzzle = Puzzle(int(puzzle_size))

        if puzzle.size == 1:
            start_state = goal_state = State(puzzle.goal_array)
            self.print_solution(goal_state, start_state, 1, 0)

        puzzle.get_goal()
        if self.args.filepath:
            start_state = State(start_state)
        else:
            start_state = State(puzzle.goal_array)
        start_state.zero_tile = start_state.find_zero()
        start_state = puzzle.shuffle(start_state, int(shuffles_amount))
        start_state.parent = None
        self.get_heuristics(start_state, puzzle)

        if self.args.filepath and not start_state.can_be_solved(puzzle):
            print("Can't be solved")
            sys.exit()

        solution_state, time, space = self.a_star_search(puzzle, start_state)

        self.print_solution(solution_state, start_state, time, space)

    def a_star_search(self, puzzle, start_state):
        """
        Perform the A* search algorithm to find the solution.

        Args:
            puzzle (Puzzle): The puzzle object representing the game.
            start_state (State): The initial state of the puzzle.

        Returns:
            solution_state (State): The solution state.
            time (int): Time complexity.
            space (int): Space complexity.
        """
        openset = []
        seenset = {}
        tiebreaker = 0
        heapq.heappush(openset, (start_state.g + start_state.h_total, start_state.h_total, tiebreaker, start_state))
        seenset[start_state.matrix.tobytes()] = start_state.g
        time, space = 0, 0

        while openset:
            current_state = heapq.heappop(openset)[3]
            if self.args.verbose:
                print("Current node heuristic value:", current_state.h_total)
            time += 1

            if current_state.h_total == 0:
                if not self.args.uniform and self.args.manhattan:
                    return current_state, time, space
                elif np.array_equal(current_state.matrix, puzzle.goal_array):
                    return current_state, time, space

            for matrix, zero_loc in current_state.get_neighbours(puzzle):
                move = State(matrix)
                move.zero_tile = zero_loc
                move.parent = current_state
                self.get_optimized_heuristics(move, puzzle)
                move.g = current_state.g + 1
                key = move.matrix.tobytes()
                seen = key in seenset
                if not seen or move.g < seenset[key]:
                    if not seen:
                        space += 1
                    seenset[key] = move.g
                    heapq.heappush(openset, (move.g + move.h_total, move.h_total, tiebreaker, move))
                    tiebreaker += 1

        print("Can't be solved")
        sys.exit()

    def print_path(self, solution_state, start_state, moves):
        """
        Print thesolution path from the solution state to the start state recursively.

        Args:
            solution_state (State): The solution state.
            start_state (State): The start state.
            moves (int): The number of moves.

        Returns:
            moves (int): The updated number of moves.
        """
        if solution_state is not start_state:
            moves += 1
            moves = self.print_path(solution_state.parent, start_state, moves)
        print(np.array(solution_state.matrix), '\n')  # Convert to numpy array before printing
        return moves

    def print_solution(self, solution_state, start_state, time, space):
        """
        Print the final solution, including the total moves, time complexity, and space complexity.

        Args:
            solution_state (State): The solution state.
            start_state (State): The start state.
            time (int): Time complexity.
            space (int): Space complexity.
        """
        np.set_printoptions(linewidth=1000, threshold=10000)
        moves = self.print_path(solution_state, start_state, 0)
        print("Total moves:\t\t%10i\nTime complexity:\t%10i\nSpace complexity:\t%10i" % (moves, time, space))
        sys.exit()
