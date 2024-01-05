import torch
from torch import optim
from torch.utils.data import TensorDataset, DataLoader
from training import train, test
import numpy as np

from project.chess_utilities.models.models import ChessEvaluationNetwork

if __name__ == "__main__":
    # Initialize data

    # Training
    X_train = torch.tensor(np.load("C:/Users/samee/OneDrive/Desktop/semester 5/Artificial Intelligence"
                                   "/Lab4/chess_framework_student/project/chess_utilities/data/training/positions.npy")).to(
        torch.float32)
    y_train = torch.tensor(np.load("C:/Users/samee/OneDrive/Desktop/semester 5/Artificial Intelligence"
                                   "/Lab4/chess_framework_student/project/chess_utilities/data/training/results.npy")).to(
        torch.float32)
    print("Training data loaded")

    # Testing
    X_test = torch.tensor(np.load("C:/Users/samee/OneDrive/Desktop/semester 5/Artificial Intelligence"
                                  "/Lab4/chess_framework_student/project/chess_utilities/data/testing/positions.npy")).to(
        torch.float32)
    y_test = torch.tensor(np.load("C:/Users/samee/OneDrive/Desktop/semester 5/Artificial Intelligence"
                                  "/Lab4/chess_framework_student/project/chess_utilities/data/testing/results.npy")).to(
        torch.float32)
    print("Testing data loaded")

    # Create a TensorDataset from the two tensors
    train_dataset = TensorDataset(X_train, y_train)

    # Create a DataLoader from the dataset
    batch_size = 512
    shuffle = True
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)

    # Create a TensorDataset from the two tensors
    test_dataset = TensorDataset(X_test, y_test)

    # Create a DataLoader from the dataset
    batch_size = 512
    shuffle = True
    test_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)

    # Instantiate the model
    model = ChessEvaluationNetwork()

    # Choose an optimizer (Adam is a commonly used optimizer)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Training starts")

    train(model, optimizer, train_dataloader)

    print("Training complete")

    print()

    print("Testing starts")

    test(model, test_dataloader)

    print("testing complete")

    # Save the model
    torch.save(model.state_dict(), "C:/Users/samee/OneDrive/Desktop/semester 5/Artificial Intelligence"
                                   "/Lab4/chess_framework_student/project/chess_utilities/models/model.pth")
