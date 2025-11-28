import os
import yaml
import numpy as np
from src.environment.traffic_environment import TrafficEnvironment
from src.agent.dqn_agent import DQNAgent

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def evaluate(config, model_path, num_episodes=125, use_gui=False):
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
        print(f"\n==== Evaluation Episode {ep+1} ====")
        state = env.reset()
        done = False
        ep_reward = 0
        step_count = 0
        while not done:
            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            ep_reward += reward
            step_count += 1
            print(f"Step {step_count}: Action={action}, Reward={reward:.2f}, Emergency={info['emergency_present']}, Waiting={info['total_waiting_time']:.2f}, Vehicles={info['vehicles_in_network']}")
            state = next_state
        print(f"Episode {ep+1} finished. Total Reward: {ep_reward:.2f}, Steps: {step_count}, Remaining Vehicles: {info['vehicles_in_network']}")
        rewards.append(ep_reward)
    print(f"\n--- Evaluation Summary ---")
    print("Episode Rewards:", rewards)
    print("Mean Reward:", np.mean(rewards))
    env.close()

if __name__ == "__main__":
    config = load_config("config.yaml")
    evaluate(config, config["paths"]["bestmodel"])