from Parser import Parser
from Solver import Solver

def main():
    # Create a parser object and parse the command-line arguments
    parser = Parser()
    args = parser.parse_arguments()

    # Create a solver object and solve the puzzle
    solver = Solver(args)
    solver.solve_puzzle()

if __name__ == "__main__":
    main()
