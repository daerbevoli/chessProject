import torch
import torch.nn as nn
import torch.nn.functional as F

board_input_size = 774


class ChessEvaluationNetwork(nn.Module):
    """
    This is a chess evaluation network that takes in a bitboard encoded (see parser) chess board of size 774
    and outputs a single scalar evaluation value.
    The network is a simple feedforward network consisting of three fully connected layers
    and ReLU activation function between them.
    """
    """
    def __init__(self):
        super(ChessEvaluationNetwork, self).__init__()
        self.fc1 = nn.Linear(board_input_size, 256)
        #self.relu1 = nn.ReLU()
        self.relu1 = nn.LeakyReLU()
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
    """
    # maybe a implementation of convolution layers
    """
    This is a chess evaluation network using a Convolutional Neural Network (CNN) architecture.
    It takes in a bitboard encoded chess board reshaped to a 3D grid
    and outputs a single scalar evaluation value.
    """

    def __init__(self, num_channels, num_additional_info=6):
        super(ChessEvaluationNetwork, self).__init__()
        self.conv1 = nn.Conv2d(num_channels, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1_additional = nn.Linear(num_additional_info, 64)  # Fully connected layer for additional info
        self.fc1 = nn.Linear(32 * 8 * 8 + 64, 128)  # Adjust input features to include additional info
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x, additional_info):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 32 * 8 * 8)
        additional_info = F.relu(self.fc1_additional(additional_info))  # Process additional info
        x = torch.cat((x, additional_info), dim=1)  # Concatenate conv output and additional info
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x