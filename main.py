import sys
import random
from board import Board
from monte_carlo import monte_carlo_search
from input_reader import read_input

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <input_file> <output_mode> <simulations>")
        print("output_mode options: Verbose, Brief, None")
        return

    input_file = sys.argv[1]
    output_mode = sys.argv[2]
    
    if output_mode not in ["Verbose", "Brief", "None"]:
        print("Error: output_mode must be 'Verbose', 'Brief', or 'None'")
        return
    
    try:
        simulations = int(sys.argv[3])
    except ValueError:
        print("Error: simulations must be an integer")
        return

    try:
        algorithm, player, grid = read_input(input_file)
        board = Board(grid, player)
        
        if algorithm == "PMCGS":
            move = monte_carlo_search(board, simulations, output_mode == "Verbose")
            if output_mode != "None":
                print(f"FINAL Move selected: {move + 1}")
        elif algorithm == "UCT":
            move = monte_carlo_search(board, simulations, output_mode == "Verbose")
            if output_mode != "None":
                print(f"FINAL Move selected: {move + 1}")
        elif algorithm == "UR":
            move = random.choice(board.get_valid_moves())
            if output_mode != "None":
                print(f"FINAL Move selected: {move + 1}")
        else:
            print(f"Unknown algorithm: {algorithm}")
            
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
