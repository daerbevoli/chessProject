import chess
from project.chess_agents.minimax_agent import MinimaxAgent  # Import your MinimaxAgent
from project.chess_utilities.utility import Utility  # Import your Utility

class ImprovedUciEngine:
    def __init__(self, name: str, author: str, agent: MinimaxAgent) -> None:
        self.name = name
        self.author = author
        self.agent = agent

    def engine_operation(self):
        # Create a clean chess board
        board = chess.Board()

        # Continuously receive and process UCI commands
        while True:
            input_val = input().split(' ')

            # Processing different UCI commands
            if input_val[0] == "uci":
                self.__uci()
            elif input_val[0] == "isready":
                print("readyok")
            elif input_val[0] == "ucinewgame":
                board = chess.Board()
            elif input_val[0] == "position":
                board = self.__set_position(input_val)
            elif input_val[0] == "go":
                print("bestmove {}".format(self.agent.calculate_move(board)))
            elif input_val[0] == "quit":
                break

    def __set_position(self, input_val):
        """
        Sets the position on the board based on UCI commands.
        """
        if input_val[1] == "startpos":
            board = chess.Board()
            moves = input_val[3:]
        else:  # Fen string input
            fen = ' '.join(input_val[1:7])
            board = chess.Board(fen)
            moves = input_val[7:]

        for move in moves:
            board.push_uci(move)
        return board

    def __uci(self):
        """
        Sends UCI initialization info.
        """
        print(f"id name {self.name}")
        print(f"id author {self.author}")
        # Additional UCI options can be added here
        print("uciok")

if __name__ == "__main__":
    # Example usage
    utility = Utility()  # Instantiate your Utility
    agent = MinimaxAgent(utility, 5.0, 3)  # Instantiate your MinimaxAgent with desired parameters
    engine = ImprovedUciEngine("Enhanced Uci Engine", "S R", agent)
    engine.engine_operation()
