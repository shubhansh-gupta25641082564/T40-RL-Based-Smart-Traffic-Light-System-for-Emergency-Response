import torch
import numpy as np
from src.agent.neural_network import DQN
from src.agent.replay_buffer import ReplayBuffer

class DQNAgent:
    def __init__(self, statesize, tl_num_phases, config):
        self.statesize = statesize
        self.tl_num_phases = tl_num_phases    # dict: {tls_id: num_phases}
        self.n_tls = len(self.tl_num_phases)
        self.buffer = ReplayBuffer(config['buffersize'])
        self.gamma = config['gamma']
        self.lr = config['learningrate']
        self.batchsize = config['batchsize']
        self.epsilon = config['epsilonstart']
        self.epsmin = config['epsilonmin']
        self.epsdecay = config['epsilondecay']
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policynet = DQN(statesize, sum(self.tl_num_phases.values())).to(self.device)
        self.targetnet = DQN(statesize, sum(self.tl_num_phases.values())).to(self.device)
        self.optimizer = torch.optim.Adam(self.policynet.parameters(), lr=self.lr)
        self.updatetargetnetwork()

    def selectaction(self, state):
        # Returns an array: one valid phase per tl
        if np.random.rand() < self.epsilon:
            action = np.array([
                np.random.randint(self.tl_num_phases[tl])
                for tl in self.tl_num_phases
            ])
            return action
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            out = self.policynet(state).cpu().numpy().flatten()
        # For each intersection, choose the phase with max Q among its slots
        actions = []
        idx = 0
        for tl in self.tl_num_phases:
            nump = self.tl_num_phases[tl]
            best = np.argmax(out[idx:idx+nump])
            actions.append(best)
            idx += nump
        action = np.array(actions)
        return action

    def trainstep(self):
        if len(self.buffer) < self.batchsize:
            return 0.0
        states, actions, rewards, nextstates, dones = self.buffer.sample(self.batchsize)
        states = torch.FloatTensor(states).to(self.device)
        # For DQN, your action space is a vector (one phase per tl)
        # We'll flatten actions for each sample
        # Convert each multi-action (array) to single integer per phase (per-tl)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        nextstates = torch.FloatTensor(nextstates).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        q_pred_batch = []
        q_target_batch = []
        for i in range(self.batchsize):
            q_all = self.policynet(states[i].unsqueeze(0)).view(-1)
            next_q_all = self.targetnet(nextstates[i].unsqueeze(0)).view(-1)
            idx = 0
            q_pred = 0
            q_target = 0
            for j, tl in enumerate(self.tl_num_phases):
                nump = self.tl_num_phases[tl]
                a = int(actions[i][j]) % nump
                q_pred += q_all[idx + a]
                next_a = torch.argmax(next_q_all[idx:idx+nump]).item()
                q_target += rewards[i] + (1 - dones[i]) * self.gamma * next_q_all[idx + next_a]
                idx += nump
            q_pred_batch.append(q_pred)
            q_target_batch.append(q_target)
        q_pred_tensor = torch.stack(q_pred_batch)
        q_target_tensor = torch.stack(q_target_batch)
        loss = torch.nn.functional.mse_loss(q_pred_tensor, q_target_tensor)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policynet.parameters(), 1.0)
        self.optimizer.step()
        return loss.item()

    def updatetargetnetwork(self):
        self.targetnet.load_state_dict(self.policynet.state_dict())

    def decayepsilon(self):
        self.epsilon = max(self.epsmin, self.epsilon * self.epsdecay)

    def save(self, filepath):
        torch.save({
            "policynet": self.policynet.state_dict(),
            "targetnet": self.targetnet.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon,
        }, filepath)

    def load(self, filepath):
        checkpoint = torch.load(filepath, map_location=self.device)
        self.policynet.load_state_dict(checkpoint["policynet"])
        self.targetnet.load_state_dict(checkpoint["targetnet"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.epsilon = checkpoint["epsilon"]