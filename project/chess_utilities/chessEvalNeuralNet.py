import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
from project.chess_utilities.models.models import ChessEvaluationNetwork
from project.chess_utilities.training import train, test

if __name__ == "__main__":
    # Load training data
    X_train = torch.tensor(np.load("./data/training/positions.npy")).to(torch.float32)
    y_train = torch.tensor(np.load("./data/training/results.npy")).to(torch.float32)
    print("Training data loaded")

    # Load testing data
    X_test = torch.tensor(np.load("./data/testing/positions.npy")).to(torch.float32)
    y_test = torch.tensor(np.load("./data/testing/results.npy")).to(torch.float32)
    print("Testing data loaded")

    # Create training dataset and dataloader
    train_dataset = TensorDataset(X_train, y_train)
    batch_size = 512
    shuffle = True
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)

    # Create testing dataset and dataloader
    test_dataset = TensorDataset(X_test, y_test)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle)

    # Instantiate the model
    model = ChessEvaluationNetwork()

    # Choose an optimizer (Adam is a commonly used optimizer)
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
