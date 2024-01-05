import torch
import torch.nn as nn

board_input_size = 774


class ChessEvaluationNetwork(nn.Module):
    """
    This is a chess evaluation network that takes in a bitboard encoded (see parser) chess board of size 774
    and outputs a single scalar evaluation value.
    The network is a simple feedforward network consisting of three fully connected layers
    and ReLU activation function between them.
    """

    def __init__(self):
        super(ChessEvaluationNetwork, self).__init__()
        self.fc1 = nn.Linear(board_input_size, 256)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(256, 128)
        self.relu2 = nn.Tanh()
        self.fc3 = nn.Linear(128, 1)  # Output layer with one node for evaluation score

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

# maybe a implementation of convolution layers
