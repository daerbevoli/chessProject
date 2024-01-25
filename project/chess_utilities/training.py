import torch
import torch.nn as nn
from torch.utils.data import DataLoader


def train(model, optimizer: torch.optim.Optimizer, train_data: DataLoader):
    """
    Train the neural network model using the specified optimizer and training data.

    Args:
    - model (torch.nn.Module): The neural network model to be trained.
    - optimizer (torch.optim.Optimizer): The optimizer used for gradient descent.
    - train_data (torch.utils.data.DataLoader): DataLoader containing training data.

    Returns:
    - None
    """
    # Training loop
    num_epochs = 10
    criterion = nn.MSELoss()
    for epoch in range(num_epochs):
        loss = 0
        for data in train_data:
            games, additional_info,  values = data[0], data[1], data[2]

            # Forward pass
            outputs = model(games, additional_info)

            # Compute the loss
            loss = criterion(outputs.view(-1), values)

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')



def test(model, test_data: DataLoader):
    """
    Train the neural network model using the specified optimizer and training data.

    Args:
    - model (torch.nn.Module): The neural network model to be trained.
    - optimizer (torch.optim.Optimizer): The optimizer used for gradient descent.
    - train_data (torch.utils.data.DataLoader): DataLoader containing training data.

    Returns:
    - None
    """
    # Evaluation loop
    model.eval()  # Set the model to evaluation mode

    criterion = nn.MSELoss()
    total_loss = 0
    num_samples = 0

    with torch.no_grad():  # Disable gradient computation during evaluation
        for data in test_data:
            games, additional_info, values = data[0], data[1], data[2]

            # Forward pass
            outputs = model(games, additional_info)

            # Compute the loss
            loss = criterion(outputs.view(-1), values)

            total_loss += loss.item()
            num_samples += len(values)

    average_loss = total_loss / num_samples
    print(f'Average Test Loss: {average_loss}')
