import random
import math
from board import Board
from Node import Node

def monte_carlo_search(board: Board, simulations: int, verbose: bool, use_uct: bool = True) -> int:
    root = Node()
    initial_player = board.player

    def get_uct_value(node, parent_visits):
        if node.visits == 0:
            return float('inf')
        
        win_rate = node.wins / node.visits
        exploration = math.sqrt(math.log(parent_visits) / node.visits) if parent_visits > 0 else 0
        return win_rate + (1.41 * exploration)

    valid_moves = board.get_valid_moves()
    for move in valid_moves:
        root.children[move] = Node(move)

    # Run simulations
    for _ in range(simulations):
        current = root
        current_board = board.copy()
        node_path = []

        # Selection/Expansion phase
        while True:
            if current_board.get_result() is not None:
                break

            valid_moves = current_board.get_valid_moves()
            if not valid_moves:
                break

            # Handle unexplored moves
            unexplored = [m for m in valid_moves if m not in current.children]
            if unexplored:
                move = random.choice(unexplored)
                new_node = Node(move)
                current.children[move] = new_node
                current_board.make_move(move)
                node_path.append(new_node)
                break

            # Select next move
            move = None
            best_value = float('-inf')
            
            try:
                for m in valid_moves:
                    if m in current.children:
                        if use_uct:
                            value = get_uct_value(current.children[m], current.visits)
                        else:
                            value = random.random()  # For PMCGS
                            
                        if value > best_value:
                            best_value = value
                            move = m
            except Exception:
                # Fallback to random selection
                move = random.choice(valid_moves)

            if move is None:
                move = random.choice(valid_moves)

            current_board.make_move(move)
            current = current.children[move]
            node_path.append(current)
            current_board.switch_player()

        # Simulation phase
        sim_board = current_board.copy()
        while sim_board.get_result() is None:
            moves = sim_board.get_valid_moves()
            if not moves:
                break
            move = random.choice(moves)
            sim_board.make_move(move)
            sim_board.switch_player()

        # Backpropagation phase
        result = sim_board.get_result()
        for node in node_path:
            node.visits += 1
            if (result == 1 and initial_player == 'Y') or (result == -1 and initial_player == 'R'):
                node.wins += 1

    best_move = valid_moves[0]
    most_visits = -1
    
    for move in valid_moves:
        if move in root.children:
            visits = root.children[move].visits
            if visits > most_visits:
                most_visits = visits
                best_move = move
            
            if verbose:
                wins = root.children[move].wins
                win_rate = wins / visits if visits > 0 else 0
                print(f"Column {move + 1}: {win_rate:.2f}")

    if verbose:
        print(f"\nFINAL Move selected: {best_move + 1}")
        
    return best_move
