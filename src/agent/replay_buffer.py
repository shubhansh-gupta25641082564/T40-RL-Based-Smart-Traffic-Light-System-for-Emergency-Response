import random
import numpy as np

class ReplayBuffer:
    def __init__(self, buffersize):
        self.buffersize = buffersize
        self.buffer = []

    def push(self, state, action, reward, nextstate, done):
        if len(self.buffer) >= self.buffersize:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, nextstate, done))

    def sample(self, batchsize):
        batch = random.sample(self.buffer, batchsize)
        states, actions, rewards, nextstates, dones = map(np.array, zip(*batch))
        return states, actions, rewards, nextstates, dones

    def __len__(self):
        return len(self.buffer)