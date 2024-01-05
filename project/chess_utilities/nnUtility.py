import chess
import torch
from project.chess_utilities.utility import Utility
from project.chess_utilities.models.models import ChessEvaluationNetwork
from project.chess_utilities.parser import bit_encode


class nnUtility(Utility):
    def __init__(self):
        """
        Initializes the nnUtility class.

        It loads a pre-trained neural network and sets it to evaluation mode.

        Args:
        - None

        Returns:
        - None
        """
        # Initialize the neural network
        self.neural_network = ChessEvaluationNetwork()

        # Load pre-trained weights for the neural network
        model_path = "C:/Users/samee/OneDrive/Desktop/semester 5/Artificial Intelligence/Lab4" \
                     "/chess_framework_student/project/chess_utilities/models/model.pth"
        self.neural_network.load_state_dict(torch.load(model_path))

        # Set the neural network to evaluation mode (no gradient computation)
        self.neural_network.eval()

    def board_value(self, board: chess.Board):
        """
        Computes the evaluation value of a chess board using a pre-trained neural network.

        Args:
        - board (chess.Board): The chess board to be evaluated.

        Returns:
        - float: The scalar evaluation value.
        """
        # Encode the chess board state using bit_encode method
        output = bit_encode(board)

        # Convert the encoded board state to a PyTorch tensor
        input_tensor = torch.tensor(output, dtype=torch.float32).unsqueeze(0)

        # Disable gradient computation during inference
        with torch.no_grad():
            # Pass the input tensor through the neural network
            evaluation = self.neural_network(input_tensor)

        # Return the scalar evaluation value as a Python float
        return evaluation.item()
