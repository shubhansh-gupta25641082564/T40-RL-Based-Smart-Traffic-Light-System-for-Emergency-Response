import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import torch
from tqdm import tqdm
from src.environment.traffic_environment import TrafficEnvironment
from src.agent.dqn_agent import DQNAgent

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def train(config):
    os.makedirs(config["paths"]["modelsdir"], exist_ok=True)
    os.makedirs(config["paths"]["logsdir"], exist_ok=True)
    env = TrafficEnvironment(
        net_file=config["environment"]["netfile"],
        route_file=config["environment"]["routefile"],
        use_gui=config["environment"]["usegui"],
        max_steps=config["environment"]["maxsteps"],
        delta_time=config["environment"]["deltatime"]
    )
    agent = DQNAgent(
        state_size=env.state_size,
        action_size=env.action_size,
        config=config['agent']
    )

    best_reward = float("-inf")
    episoderewards, episodelosses = [], []
    for episode in tqdm(range(1, config["training"]["numepisodes"] + 1)):
        print(f"\nStarting episode {episode}")
        state = env.reset()
        done = False
        episode_reward, episode_loss = 0, 0
        step_count = 0
        while not done:
            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            agent.buffer.push(state, action, reward, next_state, done)
            episode_reward += reward
            episode_loss += agent.train_step()
            state = next_state
            step_count += 1
            if step_count % 500 == 0:
                print(f"Episode {episode}, Step {step_count}, Reward {reward}, Vehicles: {info['vehicles_in_network']}")
        print(f"Episode {episode} finished, Reward: {episode_reward}\n")
        agent.decay_epsilon()
        episoderewards.append(episode_reward)
        episodelosses.append(episode_loss)
        if episode % config["agent"]["targetupdate"] == 0:
            agent.update_target_network()
        if episode_reward > best_reward:
            best_reward = episode_reward
            agent.save(config["paths"]["bestmodel"])
        if episode % config["training"]["saveinterval"] == 0:
            savepath = os.path.join(config["paths"]["modelsdir"], f"checkpoint_{episode}.pth")
            agent.save(savepath)
    np.save(os.path.join(config["paths"]["logsdir"], "rewards.npy"), episoderewards)
    np.save(os.path.join(config["paths"]["logsdir"], "losses.npy"), episodelosses)
    env.close()

def plot_training_logs(logsdir):
    reward_file = os.path.join(logsdir, "rewards.npy")
    loss_file = os.path.join(logsdir, "losses.npy")

    rewards = np.load(reward_file)
    losses = np.load(loss_file)

    plt.figure(figsize=(12,4))

    plt.subplot(1,2,1)
    plt.plot(rewards)
    plt.title("Reward per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Reward")

    plt.subplot(1,2,2)
    plt.plot(losses)
    plt.title("Loss per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Loss (Total per Episode)")

    plt.tight_layout()
    plt.savefig(os.path.join(logsdir, "training_plot.png"))
    plt.show()

if __name__ == "__main__":
    config = load_config("config.yaml")
    train(config)
    plot_training_logs(config["paths"]["logsdir"])