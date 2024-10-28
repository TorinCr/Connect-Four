import random
from board import Board
from monte_carlo import monte_carlo_search

def create_empty_board():
    """Create an empty Connect Four board"""
    empty_grid = [['O' for _ in range(7)] for _ in range(6)]
    return Board(empty_grid, 'Y')

def play_single_game(algo1, sims1, algo2, sims2):
    """Play a single game between two algorithms"""
    try:
        board = create_empty_board()
        moves_count = 0
        
        while board.get_result() is None and moves_count < 43:
            current_algo = algo1 if board.player == 'Y' else algo2
            current_sims = sims1 if board.player == 'Y' else sims2
            
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                break
                
            try:
                if current_algo == "UR":
                    move = random.choice(valid_moves)
                else:
                    use_uct = (current_algo == "UCT")
                    move = monte_carlo_search(board, current_sims, verbose=False, use_uct=use_uct)
                    
                if move not in valid_moves:
                    print(f"Invalid move {move} returned by {current_algo}")
                    return 0
                    
                board.make_move(move)
                board.switch_player()
                moves_count += 1
                
            except Exception as e:
                print(f"Error during move selection: {str(e)}")
                return 0
        
        return board.get_result()
        
    except Exception as e:
        print(f"Error during game: {str(e)}")
        return 0

def run_tournament():
    algorithms = [
        ("UR", 0),
        ("PMCGS", 500),
        ("PMCGS", 1000),
        ("UCT", 500),
        ("UCT", 1000)
    ]
    
    results = {}
    games_per_match = 100
    
    print("\nStarting tournament - 100 games per match")
    print("=" * 50)
    
    for i, (algo1, sims1) in enumerate(algorithms):
        for j, (algo2, sims2) in enumerate(algorithms):
            wins = draws = 0
            print(f"\nPlaying: {algo1}({sims1}) vs {algo2}({sims2})")
            
            for game in range(games_per_match):
                try:
                    if game % 10 == 0:
                        print(f"Game {game + 1}/{games_per_match}")
                        
                    result = play_single_game(algo1, sims1, algo2, sims2)
                    if result == 1:
                        wins += 1
                    elif result == 0:
                        draws += 0.5
                        
                except Exception as e:
                    print(f"Error in game {game + 1}: {str(e)}")
                    draws += 0.5
            
            win_percentage = (wins + draws) / games_per_match * 100
            results[(algo1, sims1, algo2, sims2)] = win_percentage
            print(f"Win percentage: {win_percentage:.1f}%")
    
    print("\nTournament Results (Win percentages)")
    print("-" * 80)
    
    print(f"{'':15}", end="")
    for algo, sims in algorithms:
        header = f"{algo}({sims})" if sims > 0 else "UR"
        print(f"{header:15}", end="")
    print()
    
    for algo1, sims1 in algorithms:
        row_header = f"{algo1}({sims1})" if sims1 > 0 else "UR"
        print(f"{row_header:15}", end="")
        
        for algo2, sims2 in algorithms:
            win_pct = results.get((algo1, sims1, algo2, sims2), 0.0)
            print(f"{win_pct:14.1f}%", end="")
        print()

if __name__ == "__main__":
    try:
        run_tournament()
    except Exception as e:
        print(f"Tournament failed: {str(e)}")
