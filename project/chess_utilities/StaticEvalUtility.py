import chess
import chess.syzygy
from project.chess_utilities.utility import Utility


class MCTSUtility(Utility):
    def __init__(self) -> None:
        # Default weights for each phase
        self.weights = {
            'material': {'opening': 0.8, 'middlegame': 1, 'endgame': 0.8},
            'piece_mobility': {'opening': 1, 'middlegame': 1, 'endgame': 1},
            'king_safety': {'opening': 0.7, 'middlegame': 0.9, 'endgame': 1},
            'pawn_structure': {'opening': 1, 'middlegame': 1, 'endgame': 1},
            'centre_control': {'opening': 1, 'middlegame': 0.7, 'endgame': 0.5},
            'pawn_square_table': {'opening': 1, 'middlegame': 1, 'endgame': 1},
            'pawns_evaluation': {'opening': 1, 'middlegame': 1, 'endgame': 1},
        }

    def board_value(self, board: chess.Board)-> float:
        # Determine the current game phase
        phase = self.determine_game_phase(board)

        # Check if the game is over
        if board.is_game_over():
            return self.evaluate_terminal_position(board)

        # Evaluate based on various criteria with dynamic weights
        material_score = self.evaluate_material_balance(board)

        piece_mobility_score = self.evaluate_piece_mobility(board)

        king_safety_score = self.evaluate_king_safety(board)

        pawn_structure_score = self.evaluate_pawn_structure(board)

        centre_control_score = self.evaluate_center_control(board)

        pawn_square_table_score = self.pawn_square_table_score(board)

        # Combine individual scores with dynamic weights
        total_score = (
                self.weights['material'][phase] * material_score +
                self.weights['piece_mobility'][phase] * piece_mobility_score +
                self.weights['king_safety'][phase] * king_safety_score +
                self.weights['pawn_structure'][phase] * pawn_structure_score +
                self.weights['centre_control'][phase] * centre_control_score +
                self.weights['pawn_square_table'][phase] * pawn_square_table_score
        )
        return total_score

    def determine_game_phase(self, board: chess.Board) -> str:
        # Determine the game phase based on the number of pieces remaining
        total_pieces = len(board.piece_map())
        if total_pieces > 26:
            return 'opening'
        elif 10 < total_pieces <= 26:
            return 'middle game'
        else:
            return 'endgame'

    def evaluate_terminal_position(self, board: chess.Board) -> float:
        # Evaluate terminal positions (e.g., checkmate, stalemate)
        result = board.result()
        if result == '1-0':
            return 1  # White wins
        elif result == '0-1':
            return -1  # Black wins
        elif result == '1/2-1/2':
            return 0.0  # Draw

    def evaluate_material_balance(self, board: chess.Board) -> float:
        PIECE_VALUES = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 20
        }

        white_material = 0
        black_material = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Accumulate material value based on the piece type and color
                piece_value = PIECE_VALUES[piece.piece_type]
                if piece.color == chess.WHITE:
                    white_material += piece_value
                else:
                    black_material += piece_value

        # Calculate material balance (positive if white has an advantage, negative if black has an advantage)
        material_balance = white_material - black_material
        return material_balance

    def evaluate_piece_mobility(self, board):
        white_mobility = 0
        black_mobility = 0

        for square, piece in board.piece_map().items():
            if piece.color == chess.WHITE:
                white_mobility += self.count_effective_moves(board, square, piece)
            elif piece.color == chess.BLACK:
                black_mobility += self.count_effective_moves(board, square, piece)

        return (white_mobility - black_mobility) * 100

    def count_effective_moves(self, board, square, piece):
        important_squares = {chess.C4, chess.C5, chess.D4, chess.D5, chess.E4, chess.E5, chess.F4, chess.F5}
        legal_moves = list(board.legal_moves)

        # Penalize bishops for having many pawns on squares of the same color
        if piece.piece_type == chess.BISHOP:
            pawn_penalty = self.calculate_pawn_penalty(board, square, piece.color)
        else:
            pawn_penalty = 0

        # Penalize knights for being close to the edges
        if piece.piece_type == chess.KNIGHT:
            edge_penalty = self.calculate_edge_penalty(square)
        else:
            edge_penalty = 0

        # Assign higher weights to capturing moves and center control
        effective_moves = [move for move in legal_moves if
                           move.from_square == square and move.to_square in important_squares]
        return len(effective_moves) - pawn_penalty - edge_penalty

    def calculate_pawn_penalty(self, board, square, color):
        # Count the number of pawns on squares of the same color as the bishop
        pawn_penalty = 0
        for pawn_square in board.pieces(chess.PAWN, color):
            if chess.Color(pawn_square) == chess.Color(square):
                pawn_penalty += 1
        return pawn_penalty

    def calculate_edge_penalty(self, square):
        # Penalize knights for being close to the edges
        file_distance = min(square % 8, 7 - square % 8)
        rank_distance = min(square // 8, 7 - square // 8)
        return max(0, 3 - min(file_distance, rank_distance))

    def evaluate_king_safety(self, board: chess.Board) -> float:
        # Evaluate king safety based on factors such as pawn structure in front of the king,
        # open lines towards the king, and the position of enemy pieces
        white_king_safety = self.evaluate_king_safety_for_color(board, chess.WHITE)
        black_king_safety = self.evaluate_king_safety_for_color(board, chess.BLACK)
        return (white_king_safety - black_king_safety) * 100

    def evaluate_king_safety_for_color(self, board: chess.Board, color) -> float:
        king_square = board.king(color)
        pawn_shield_score = self.evaluate_pawn_shield(board, king_square, color)
        open_lines_score = self.evaluate_open_lines(board, king_square, color)
        enemy_pieces_score = self.evaluate_enemy_pieces(board, king_square, color)
        return pawn_shield_score + open_lines_score + enemy_pieces_score

    def evaluate_pawn_shield(self, board: chess.Board, king_square, color) -> float:
        # Evaluate the presence and strength of a pawn shield in front of the king
        pawn_shield_score = 0
        king_rank = king_square // 8

        for file_offset in range(-1, 2):
            file_index = king_square % 8 + file_offset
            if 0 <= file_index <= 7:
                pawn_square = chess.square(file_index, king_rank + 1 if color == chess.WHITE else king_rank - 1)
                if board.piece_at(pawn_square) == chess.PAWN and board.piece_at(pawn_square).color == color:
                    pawn_shield_score += 1

        return pawn_shield_score

    def evaluate_open_lines(self, board: chess.Board, king_square, color) -> float:
        # Evaluate the openness of lines towards the king
        open_lines_score = 0

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # North, South, East, West
            (1, 1), (-1, 1), (1, -1), (-1, -1)  # Northeast, Northwest, Southeast, Southwest
        ]

        for direction in directions:
            line_square = king_square
            while True:
                line_square = chess.square(chess.square_file(line_square) + direction[0],
                                           chess.square_rank(line_square) + direction[1])

                if not 0 <= line_square < 64:
                    break  # Stop if outside the board

                if board.attacks(line_square) & board.attackers(color, line_square):
                    open_lines_score += 1
                else:
                    break  # Stop if no attack along the line

        return open_lines_score

    def evaluate_enemy_pieces(self, board: chess.Board, king_square, color) -> float:
        # Evaluate the proximity and activity of enemy pieces near the king
        enemy_pieces_score = 0

        for square in chess.SquareSet(chess.SQUARES):
            piece = board.piece_at(square)
            if piece and piece.color == 1 - color:  # Opponent's piece
                distance_to_king = max(abs(chess.square_file(square) - chess.square_file(king_square)),
                                       abs(chess.square_rank(square) - chess.square_rank(king_square)))
                enemy_pieces_score += 1 / distance_to_king  # Closer pieces have a higher impact

        return enemy_pieces_score

    def evaluate_pawn_structure(self, board: chess.Board) -> float:
        # Evaluate pawn structure (simple evaluation for illustration)
        white_pawn_structure = self.evaluate_pawn_structure_for_color(board, chess.WHITE)
        black_pawn_structure = self.evaluate_pawn_structure_for_color(board, chess.BLACK)
        return white_pawn_structure - black_pawn_structure

    def evaluate_pawn_structure_for_color(self, board: chess.Board, color) -> float:
        # Evaluate pawn structure for a specific color
        pawn_structure_score = 0

        pawn_chains = 0
        pawn_islands = 0

        for square in chess.SquareSet(chess.SQUARES):
            piece = board.piece_at(square)

            if piece and piece.piece_type == chess.PAWN and piece.color == color:
                pawn_structure_score += 1

                # Check if the pawn is part of a pawn chain
                if board.is_pinned(color, square):
                    pawn_chains += 1

                # Check if the pawn is the leftmost or rightmost in a file
                file_index = chess.square_file(square)
                if file_index == 0 or file_index == 7:
                    pawn_islands += 1

        # Adjust the score based on additional factors (you can customize the weights)
        pawn_structure_score += 0.5 * pawn_chains - 0.2 * pawn_islands

        return pawn_structure_score

    def evaluate_center_control(self, board: chess.Board):
        center_squares = {chess.C4, chess.C5, chess.D4, chess.D5, chess.E4, chess.E5, chess.F4, chess.F5}

        # Consider piece activity and pawn structure in the center
        white_center_activity = sum(1 for square in center_squares if board.piece_at(square) and board.piece_at(
            square).color == chess.WHITE and board.piece_at(square).piece_type in {chess.PAWN, chess.KNIGHT,
                                                                                   chess.BISHOP})
        black_center_activity = sum(1 for square in center_squares if board.piece_at(square) and board.piece_at(
            square).color == chess.BLACK and board.piece_at(square).piece_type in {chess.PAWN, chess.KNIGHT,
                                                                                   chess.BISHOP})

        return white_center_activity - black_center_activity


    def pawn_square_table_score(self, board: chess.Board):
        pawntable = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        knightstable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        bishopstable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        rookstable = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        queenstable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]

        kingstable = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

        pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                               for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                                   for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                                   for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                                 for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KING, chess.BLACK)])

        eval = + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if board.turn:
            return eval
        else:
            return -eval