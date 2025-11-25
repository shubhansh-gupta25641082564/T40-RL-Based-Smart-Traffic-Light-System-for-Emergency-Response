import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, statesize, actionsize, hiddensize=128):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(statesize, hiddensize)
        self.fc2 = nn.Linear(hiddensize, hiddensize)
        self.fc3 = nn.Linear(hiddensize, actionsize)

    def forward(self, x):
        print("[Net] Forward pass with input:", x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        print("[Net] Output:", x)
        return x