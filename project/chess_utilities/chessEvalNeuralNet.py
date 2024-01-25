import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
from project.chess_utilities.models.models import ChessEvaluationNetwork
from project.chess_utilities.training import train, test
import os

if __name__ == "__main__":
    # Directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Load training data
    X_train = torch.tensor(np.load(os.path.join(current_dir, 'data', 'training', 'positions.npy'))).to(torch.float32)
    y_train = torch.tensor(np.load(os.path.join(current_dir, 'data', 'training', 'results.npy'))).to(torch.float32)
    # DEBUG
    print("Training data loaded, Shape of X_train:", X_train.shape)

    # Load testing data
    X_test = torch.tensor(np.load(os.path.join(current_dir, 'data', 'testing', 'positions.npy'))).to(torch.float32)
    y_test = torch.tensor(np.load(os.path.join(current_dir, 'data', 'testing', 'results.npy'))).to(torch.float32)

    # Load additional info for training and testing
    additional_info_train = torch.tensor(np.load(os.path.join(current_dir, 'data', 'training', 'additional_info.npy'))).to(torch.float32)
    additional_info_test = torch.tensor(np.load(os.path.join(current_dir, 'data', 'testing', 'additional_info.npy'))).to(torch.float32)

    # Create training dataset and dataloader
    # HYPERPARAMETER: Batch size
    train_dataset = TensorDataset(X_train, additional_info_train, y_train)
    batch_size = 1024
    shuffle = True
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)

    # Create testing dataset and dataloader
    test_dataset = TensorDataset(X_test, additional_info_test, y_test)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle)

    # Instantiate the model
    model = ChessEvaluationNetwork(num_channels=12, num_additional_info=6)

    # Choose an optimizer (Adam is a commonly used optimizer)
    # HYPERPARAMETER: Learning rate
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Training starts")
    train(model, optimizer, train_dataloader)
    print("Training complete\n")

    print("Testing starts")
    test(model, test_dataloader)
    print("Testing complete")

    # Save the model
    model_path = "./models/model.pth"
    torch.save(model.state_dict(), model_path)
