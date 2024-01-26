import os

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
        self.neural_network = ChessEvaluationNetwork(num_channels=12, num_additional_info=6)

        # Directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Load pre-trained weights for the neural network
        model_path = os.path.join(current_dir, 'models', 'model.pth')
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
        """
        # Encode the chess board state using bit_encode method
        bit_encoded_board, additional_info = bit_encode(board)  # bit_encode now returns additional_info too

        # Convert the encoded board state to a PyTorch tensor
        input_tensor = torch.tensor(bit_encoded_board, dtype=torch.float32).unsqueeze(0)
        input_tensor = input_tensor.view(-1, 12, 8, 8)  # Reshape to the correct shape: [batch_size, channels, height, width]

        # Process the additional_info (You might need to convert it to a tensor and/or reshape it)
        additional_info_tensor = torch.tensor(additional_info, dtype=torch.float32).unsqueeze(0)

        # Disable gradient computation during inference
        with torch.no_grad():
            # Pass the input tensor and additional_info_tensor through the neural network
            evaluation = self.neural_network(input_tensor, additional_info_tensor)

        # Return the scalar evaluation value as a Python float
        return evaluation.item()