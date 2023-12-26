from project.chess_agents.agent import Agent
from project.chess_utilities.enhanced_utility import Utility

import chess
import random
import math
import time

# A class representing a node in the Monte Carlo search tree
class MonteCarloNode:
    def __init__(self, board: chess.Board, move: chess.Move = None, parent: 'MonteCarloNode' = None):
        # Initialize node attributes
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.visit_count = 0
        self.total_score = 0

    def is_fully_expanded(self) -> bool:
        # Check if all legal moves have corresponding child nodes
        return len(self.children) == len(list(self.board.legal_moves))

    def is_terminal(self) -> bool:
        # Check if the current board state represents the end of the game
        return self.board.is_game_over()

    def expand(self) -> 'MonteCarloNode':
        # Generate a new child node by making a random legal move
        legal_moves = list(self.board.legal_moves)
        untried_moves = [move for move in legal_moves if move not in [child.move for child in self.children]]
        new_move = random.choice(untried_moves)
        new_board = self.board.copy()
        new_board.push(new_move)
        new_node = MonteCarloNode(new_board, move=new_move, parent=self)
        self.children.append(new_node)
        return new_node

# A chess agent class using Monte Carlo Tree Search
class MonteCarloChessAgent(Agent):
    def __init__(self, utility: Utility, time_limit_move: float, exploration_weight: float):
        # Initialize the agent with utility, time limit for moves, and exploration weight
        super().__init__(utility, time_limit_move)
        self.exploration_weight = exploration_weight

    def calculate_move(self, board: chess.Board) -> chess.Move:
        # Initialize the root node with the current board state
        start_time = time.time()
        root = MonteCarloNode(board)

        while time.time() - start_time < self.time_limit_move:
            # Perform Monte Carlo Tree Search to find the best move
            node_to_expand = self.select(root)
            simulation_result = self.simulate(node_to_expand)
            self.backpropagate(node_to_expand, simulation_result)

        # Choose the best move based on statistics
        best_move = self.best_child(root).move
        return best_move

    def select(self, node: 'MonteCarloNode') -> 'MonteCarloNode':
        # Traverse the tree to find the node to expand, balancing exploration and exploitation
        while not node.is_terminal() and node.is_fully_expanded():
            node = self.best_uct(node)
        if not node.is_terminal():
            return node.expand()
        return node

    def simulate(self, node: 'MonteCarloNode') -> float:
        # Simulate a random game from the current board state
        simulation_board = node.board.copy()
        while not simulation_board.is_game_over():
            legal_moves = list(simulation_board.legal_moves)
            random_move = random.choice(legal_moves)
            simulation_board.push(random_move)
        return self.calculate_score(simulation_board)

    def backpropagate(self, node: 'MonteCarloNode', result: float):
        # Backpropagate the simulation result through the tree
        while node is not None:
            node.visit_count += 1
            node.total_score += result
            node = node.parent
            if node and node.parent is None:
                break

    def best_uct(self, node: 'MonteCarloNode') -> 'MonteCarloNode':
        # Calculate the UCT value for child nodes and select the one with the highest UCT
        if node.parent is None or node.parent.visit_count == 0:
            # Handle the root node or nodes without a parent
            return max(node.children, key=lambda child: child.total_score / (child.visit_count + 1))
        log_parent_visits = math.log(node.parent.visit_count)
        return max(node.children, key=lambda child: (child.total_score / child.visit_count) +
                                                     self.exploration_weight * math.sqrt(
                                                         log_parent_visits / child.visit_count) if child.visit_count > 0 else float('inf'))

    def best_child(self, node: 'MonteCarloNode') -> 'MonteCarloNode':
        # Select the child node with the highest visit count
        return max(node.children, key=lambda child: child.visit_count)

    def calculate_score(self, board: chess.Board) -> float:
        # Evaluate the utility or score of the given chess board state
        return self.utility.board_value(board)