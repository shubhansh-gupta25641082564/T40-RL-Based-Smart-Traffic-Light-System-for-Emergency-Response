import random
import numpy as np
from collections import deque

class ReplayBuffer:
    """
    Experience replay buffer for DQN
    """

    def __init__(self, capacity=10000):
        """
        Initialize replay buffer

        Args:
            capacity: Maximum number of experiences to store
        """
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """
        Add experience to buffer

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode ended
        """
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        """
        Sample batch of experiences

        Args:
            batch_size: Number of experiences to sample
        Returns:
            Tuple of batched experiences
        """
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards, dtype=np.float32),
            np.array(next_states),
            np.array(dones, dtype=np.uint8)
        )

    def __len__(self):
        """Return current size of buffer"""
        return len(self.buffer)