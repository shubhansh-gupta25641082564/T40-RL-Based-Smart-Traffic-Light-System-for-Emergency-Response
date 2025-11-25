import random
import numpy as np

class ReplayBuffer:
    def __init__(self, buffersize):
        print(f"[Buffer] Initializing ReplayBuffer with size: {buffersize}")
        self.buffer = []
        self.buffersize = buffersize

    def push(self, state, action, reward, nextstate, done):
        if len(self.buffer) >= self.buffersize:
            self.buffer.pop(0)
        self.buffer.append((state, action, reward, nextstate, done))
        print(f"[Buffer] New Experience added! Current size: {len(self.buffer)}")

    def sample(self, batchsize):
        batch = random.sample(self.buffer, batchsize)
        states, actions, rewards, nextstates, dones = map(np.array, zip(*batch))
        print(f"[Buffer] Sampled batch of size {batchsize}")
        return states, actions, rewards, nextstates, dones

    def __len__(self):
        return len(self.buffer)