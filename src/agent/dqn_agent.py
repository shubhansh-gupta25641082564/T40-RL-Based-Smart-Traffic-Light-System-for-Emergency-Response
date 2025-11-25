import torch
import numpy as np
from neural_network import DQN
from replay_buffer import ReplayBuffer

class DQNAgent:
    def __init__(self, statesize, actionsize, config):
        print(f"[Agent] Initializing DQNAgent with state size {statesize}, action size {actionsize}")
        self.statesize = statesize
        self.actionsize = actionsize
        self.buffer = ReplayBuffer(config['buffersize'])
        self.gamma = config['gamma']
        self.lr = config['learningrate']
        self.batchsize = config['batchsize']
        self.epsilon = config['epsilonstart']
        self.epsmin = config['epsilonmin']
        self.epsdecay = config['epsilondecay']
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policynet = DQN(statesize, actionsize).to(self.device)
        self.targetnet = DQN(statesize, actionsize).to(self.device)
        self.optimizer = torch.optim.Adam(self.policynet.parameters(), lr=self.lr)
        self.update_target_network()

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            action = np.random.randint(self.actionsize)
            print(f"[Agent] Random action selected (exploration): {action}")
            return action
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            qvalues = self.policynet(state)
            action = qvalues.argmax().item()
            print(f"[Agent] Action selected by policy network: {action}")
        return action

    def train_step(self):
        if len(self.buffer) < self.batchsize:
            print(f"[Agent] Not enough samples in buffer to train. Buffer size: {len(self.buffer)}")
            return 0
        states, actions, rewards, nextstates, dones = self.buffer.sample(self.batchsize)
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        nextstates = torch.FloatTensor(nextstates).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        qvalues = self.policynet(states).gather(1, actions)
        with torch.no_grad():
            max_next_q = self.targetnet(nextstates).max(1)[0].unsqueeze(1)
            target_q = rewards + self.gamma * max_next_q * (1 - dones)
        loss = torch.nn.functional.mse_loss(qvalues, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policynet.parameters(), 1.0)
        self.optimizer.step()
        print(f"[Agent] Training step complete. Loss: {loss.item()}")
        return loss.item()

    def update_target_network(self):
        self.targetnet.load_state_dict(self.policynet.state_dict())
        print("[Agent] Target network updated.")

    def decay_epsilon(self):
        old_epsilon = self.epsilon
        self.epsilon = max(self.epsmin, self.epsilon * self.epsdecay)
        print(f"[Agent] Epsilon decayed from {old_epsilon} to {self.epsilon}")

    def save(self, filepath):
        print(f"[Agent] Saving model to {filepath}")
        torch.save({
            "policynet": self.policynet.state_dict(),
            "targetnet": self.targetnet.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon
        }, filepath)

    def load(self, filepath):
        print(f"[Agent] Loading model from {filepath}")
        checkpoint = torch.load(filepath, map_location=self.device)
        self.policynet.load_state_dict(checkpoint["policynet"])
        self.targetnet.load_state_dict(checkpoint["targetnet"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.epsilon = checkpoint["epsilon"]