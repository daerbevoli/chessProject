#!/usr/bin/python3
from project.chess_utilities.example_utility import ExampleUtility
from project.chess_agents.example_agent import ExampleAgent
from project.chess_agents.MonteCarloAgent import MonteCarloChessAgent
import chess
import chess.engine
import chess.pgn
from project.chess_utilities.nnUtility import nnUtility

""" An agent plays a game against the stockfish engine """
def play_stockfish():
    
    time_limit = 5.0
        
    # Setup
    board = chess.Board()
    # Define agent here
    white_player = MonteCarloChessAgent(nnUtility(), 5.0, 1.0)
    # Enter your path here:
    black_player = chess.engine.SimpleEngine.popen_uci("C:/Users/samee/OneDrive/Desktop/stockfish/stockfish.exe")
    # Determine the skill level of Stockfish:
    black_player.configure({"Skill Level": 1})
    limit = chess.engine.Limit(time=time_limit)

    running = True
    turn_white_player = True

    # Game loop
    while running:
        move = None

        if turn_white_player:
            # White plays a random move
            move = white_player.calculate_move(board)
            turn_white_player = False
            print("White plays")
        else:
            # Stockfish plays a move
            move = black_player.play(board, limit).move
            turn_white_player = True
            print("Black plays")

        board.push(move)
        print(board)
        print("----------------------------------------")
        
        # Check if a player has won
        if board.is_checkmate():
            running = False
            if turn_white_player:
                print("Stockfish wins!")
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
            print("Draw by fivefold repitition!")
        elif board.is_seventyfive_moves():
            running = False
            print("Draw by 75-moves rule")

    black_player.quit()
    return board

def main():
    play_stockfish()

if __name__ == "__main__":
    main()
