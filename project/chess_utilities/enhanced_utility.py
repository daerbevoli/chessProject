import chess
from project.chess_utilities.utility import Utility

class EnhancedUtility(Utility):

    def __init__(self) -> None:
        # The value of each piece
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0 # King's value is set to 0 since its capture ends the game.
        }

    def board_value(self, board: chess.Board):
        # returns a score representing the value of the board state.
        value = 0
        for piece_type in self.pieces_values:
            # Add the value for each white piece
            value += len(board.pieces(piece_type=piece_type, color=chess.WHITE)) * self.piece_values[piece_type]
            # Subtract the value for each black piece
            value -= len(board.pieces(piece_type=piece_type, color=chess.BLACK)) * self.piece_values[piece_type]

        return value