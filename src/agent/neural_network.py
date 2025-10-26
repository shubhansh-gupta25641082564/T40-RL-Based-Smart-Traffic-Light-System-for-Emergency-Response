import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    """
    Deep Q-Network for traffic signal control
    """

    def __init__(self, state_size, action_size, hidden_size=128):
        """
        Initialize DQN

        Args:
            state_size: Dimension of state space
            action_size: Number of possible actions
            hidden_size: Size of hidden layers
        """
        super(DQN, self).__init__()
        
        # Input layer
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.bn1 = nn.LayerNorm(hidden_size)
        
        # Hidden layers
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.LayerNorm(hidden_size)

        self.fc3 = nn.Linear(hidden_size, hidden_size // 2)
        self.bn3 = nn.LayerNorm(hidden_size // 2)

        # Output layer
        self.fc4 = nn.Linear(hidden_size // 2, action_size)
        
        # Dropout for regularization
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        """
        Forward pass

        Args:
            x: Input state tensor
        Returns:
            Q-values for each action
        """
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)

        x = F.relu(self.bn3(self.fc3(x)))
        x = self.fc4(x)  # No activation on output

        return x

# Test the network
if __name__ == "__main__":
    state_size = 24  # From environment
    action_size = 2  # NS or EW green

    model = DQN(state_size, action_size)
    print(model)

    # Test forward pass
    dummy_state = torch.randn(32, state_size)  # Batch of 32
    q_values = model(dummy_state)
    print(f"\nOutput shape: {q_values.shape}")
    print(f"Q-values sample: {q_values[0]}")