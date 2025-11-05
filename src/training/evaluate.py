import os
import yaml
import numpy as np
from src.environment.traffic_environment import TrafficEnvironment
from src.agent.dqn_agent import DQNAgent

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def evaluate(config, model_path, num_episodes=10, use_gui=True):
    env = TrafficEnvironment(
        net_file=config["environment"]["netfile"],
        route_file=config["environment"]["routefile"],
        use_gui=use_gui,
        max_steps=config["environment"]["maxsteps"],
        delta_time=config["environment"]["deltatime"]
    )
    agent = DQNAgent(
        state_size=env.state_size,
        action_size=env.action_size,
        config=config["agent"]
    )
    agent.load(model_path)
    rewards = []
    for ep in range(num_episodes):
        state = env.reset()
        done = False
        ep_reward = 0
        while not done:
            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            ep_reward += reward
            state = next_state
        rewards.append(ep_reward)
    print("Mean Reward:", np.mean(rewards))
    env.close()

if __name__ == "__main__":
    config = load_config("config.yaml")
    evaluate(config, config["paths"]["bestmodel"])