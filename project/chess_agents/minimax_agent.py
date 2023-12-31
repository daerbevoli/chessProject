from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.utility import Utility
import time



class MinimaxAgent(Agent):

    def __init__(self, utility: Utility, time_limit_move: float, depth: int) -> None:
        super().__init__(utility, time_limit_move)
        self.name = "Minimax_Agent"
        self.author = "S. Roels & S. Baruwal"
        self.depth = depth  # The depth of the minimax search tree

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> int:
        # By using maximizingPlayer, we don't' have to flip the values

        start_time = time.time()

        # check if the maximum depth or game is over
        if depth == 0 or board.is_game_over():
            return self.utility.board_value(board)  # Return the utility value of the board

        # If it's the white player's turn (maximizingPlayer = True), the function looks for
        # moves that maximize the board value.
        if maximizingPlayer:
            maxEval = float('-inf')

            for move in board.legal_moves:
                # Check if the maximum calculation time for this move has been reached
                if time.time() - start_time > self.time_limit_move:
                    break
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval

        else:  # If it's the black player's turn (maximizingPlayer = False), the function looks for moves that
            # minimize the board value.
            minEval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def calculate_move(self, board: chess.Board):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in list(board.legal_moves):
            board.push(move)
            move_value = self.minimax(board, self.depth, alpha, beta, False)
            board.pop()
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move
