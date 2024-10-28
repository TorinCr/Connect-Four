import math
import random
from board import Board
from node import Node

def ucb_value(node: Node, parent_visits: int, exploration_constant: float = 1.41) -> float:
    if node.visits == 0:
        return float('inf')  # Unvisited nodes are prioritized

    exploitation_value = node.wins / node.visits
    exploration_value = exploration_constant * math.sqrt(math.log(parent_visits) / node.visits) if parent_visits > 0 else 0  
    return exploitation_value + exploration_value

def uct_search(board: Board, simulations: int, verbose: bool):
    root = Node()
    initial_player = board.player

    for i in range(simulations):
        current = root
        current_board = board.copy()
        node_path = []

        # SELECTION AND EXPANSION
        while True:
            if current_board.get_result() is not None:
                break

            valid_moves = current_board.get_valid_moves()
            unexplored = [m for m in valid_moves if m not in current.children]

            # Expand if unexplored moves exist
            if unexplored:
                move = unexplored[0]
                new_node = Node(move)
                new_node.parent = current
                current.children[move] = new_node
                current_board.make_move(move)
                node_path.append(new_node)
                if verbose:
                    print("NODE ADDED")
                break

            # Calculate UCB values for each move
            ucb_values = {move: ucb_value(child, current.visits) for move, child in current.children.items()}

            # Select the move with the highest UCB value
            move = max(ucb_values, key=ucb_values.get)

            current_board.make_move(move)
            current = current.children[move]
            node_path.append(current)
            current_board.switch_player()

            if verbose:
                print(f"wi: {current.wins}")
                print(f"ni: {current.visits}")

                for i, move_key in enumerate(ucb_values, start=1):
                    print(f"V{i}: {ucb_values[move_key]:.2f}")
                print(f"Move selected: {move + 1}")

        # SIMULATION (Rollout)
        sim_board = current_board.copy()
        while sim_board.get_result() is None:
            moves = sim_board.get_valid_moves()
            move = random.choice(moves) if moves else None
            if move is not None:
                sim_board.make_move(move)
                sim_board.switch_player()

        result = sim_board.get_result()
        if verbose:
            print(f"TERMINAL NODE VALUE: {result}")

        # BACKPROPAGATION
        for node in reversed(node_path):
            node.visits += 1
            if (result == 1 and initial_player == 'Y') or (result == -1 and initial_player == 'R'):
                node.wins += 1
            if verbose:
                print(f"Updated values: \n wi: {node.wins} \n ni: {node.visits}")

    # FINAL MOVE SELECTION AND OUTPUT
    moves_values = {}
    for col in range(7):
        if col in root.children:
            node = root.children[col]
            value = node.wins / node.visits if node.visits > 0 else 0
            moves_values[col] = value
            if verbose:
                print(f"Column {col + 1}: {value:.2f}")
        else:
            moves_values[col] = float('-inf')
            if verbose:
                print(f"Column {col + 1}: Null")

    # Select the move with the highest value, with fallback for ties
    best_move = max((col for col in moves_values if moves_values[col] != float('-inf')),
                    key=moves_values.get, default=None)
    
    # Print final move selection
    if verbose:
        print(f"\nFINAL Move selected: {best_move + 1 if best_move is not None else 'No move available'}")
    
    return best_move
