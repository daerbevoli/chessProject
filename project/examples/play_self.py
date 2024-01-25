#!/usr/bin/python3
import chess
import chess.svg
from project.chess_utilities.example_utility import ExampleUtility
from project.chess_agents.example_agent import ExampleAgent

from project.chess_utilities.enhanced_utility import EnhancedUtility
from project.chess_utilities.nonNNEval import MCTSUtility
from project.chess_utilities.nnUtility import nnUtility
from project.chess_agents.MonteCarloAgent import MonteCarloChessAgent

#from project.chess_utilities.nnUtility import nnUtility

""" Two agents play against eachother until the game is finished """
def play_self():
    # Setup a clean board
    board = chess.Board()
    # Create the white and black agent
    white_player = MonteCarloChessAgent(5.0, 1.1415)
    white_player.name = "White Player"
    black_player = ExampleAgent(ExampleUtility(), 1.0)
    black_player.name = "Black Player"

    running = True
    turn_white_player = True
    counter = 0

    # Game loop
    while running:
        counter += 1
        move = None

        if turn_white_player:
            move = white_player.calculate_move(board)
            turn_white_player = False
            print("White plays")
        else:
            move = black_player.calculate_move(board)
            turn_white_player = True
            print("Black plays")

        # The move is played and the board is printed
        board.push(move)
        print(board)
        print("counter: ", counter)
        print("----------------------------------------")
        

        # Check if a player has won
        if board.is_checkmate():
            running = False
            if turn_white_player:
                print("{} wins!".format(black_player.name))
            else:
                print("{} wins!".format(white_player.name))

        # Check for draws
        if board.is_stalemate():
            running = False
            print("Draw by stalemate")
        elif board.is_insufficient_material():
            running = False
            print("Draw by insufficient material")
        elif board.is_fivefold_repetition():
            running = False
            print("Draw by fivefold repetition!")
        elif board.is_seventyfive_moves():
            running = False
            print("Draw by 75-moves rule")
        

def main():
    play_self()


if __name__ == "__main__":
    main()
