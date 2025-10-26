import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from src.environment.traffic_environment import TrafficEnvironment
from src.agent.dqn_agent import DQNAgent

def load_config(config_path='config.yaml'):
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def train(config):
    """
    Main training loop

    Args:
        config: Configuration dictionary
    """
    # Create directories
    os.makedirs(config['paths']['models_dir'], exist_ok=True)
    os.makedirs(config['paths']['logs_dir'], exist_ok=True)

    # Initialize environment
    env = TrafficEnvironment(
        net_file=config['environment']['net_file'],
        route_file=config['environment']['route_file'],
        use_gui=config['environment']['use_gui'],
        delta_time=config['environment']['delta_time']
    )
    # Initialize agent
    agent = DQNAgent(
        state_size=env.state_size,
        action_size=env.action_size,
        config=config['agent']
    )
    # Training metrics
    episode_rewards = []
    episode_losses = []
    best_reward = -np.inf

    # Training loop
    num_episodes = config['training']['num_episodes']

    print(f"\n{'='*60}")
    print(f"Starting Training: {num_episodes} episodes")
    print(f"{'='*60}\n")

    for episode in range(1, num_episodes + 1):
        # Reset environment
        state = env.reset()
        episode_reward = 0
        episode_loss = []

        # Episode loop
        done = False
        step = 0

        with tqdm(total=config['training']['max_steps_per_episode'],
                  desc=f"Episode {episode}/{num_episodes}",
                  leave=False) as pbar:

            while not done:
                # Select action
                action = agent.select_action(state, training=True)

                # Take step
                next_state, reward, done, info = env.step(action)

                # Store experience
                agent.store_experience(state, action, reward, next_state, done)

                # Train
                loss = agent.train_step()
                episode_loss.append(loss)

                # Update state
                state = next_state
                episode_reward += reward
                step += 1

                # Update progress bar
                pbar.update(env.delta_time)
                pbar.set_postfix({
                    'reward': f'{episode_reward:.2f}',
                    'loss': f'{np.mean(episode_loss):.4f}' if episode_loss else '0',
                    'epsilon': f'{agent.epsilon:.3f}'
                })

        # Episode finished
        episode_rewards.append(episode_reward)
        avg_loss = np.mean(episode_loss) if episode_loss else 0
        episode_losses.append(avg_loss)

        # Decay epsilon
        agent.decay_epsilon()

        # Update target network
        if episode % config['agent']['target_update'] == 0:
            agent.update_target_network()
            print(f"\n  → Target network updated at episode {episode}")

        # Save best model
        if episode_reward > best_reward:
            best_reward = episode_reward
            agent.save(config['paths']['best_model'])
            print(f"\n  ✓ New best model saved! Reward: {best_reward:.2f}")

        # Save checkpoint
        if episode % config['training']['save_interval'] == 0:
            checkpoint_path = os.path.join(
                config['paths']['models_dir'],
                f'checkpoint_ep{episode}.pth'
            )
            agent.save(checkpoint_path)

        # Print episode summary
        print(f"\nEpisode {episode} Summary:")
        print(f"  Reward: {episode_reward:.2f}")
        print(f"  Avg Loss: {avg_loss:.4f}")
        print(f"  Epsilon: {agent.epsilon:.3f}")
        print(f"  Best Reward: {best_reward:.2f}")
        print(f"  Emergency events: {info.get('emergency_count', 0)}")

    # Close environment
    env.close()

    # Save training metrics
    np.save(os.path.join(config['paths']['logs_dir'], 'rewards.npy'),
            episode_rewards)
    np.save(os.path.join(config['paths']['logs_dir'], 'losses.npy'),
            episode_losses)

    # Plot results
    plot_training_results(episode_rewards, episode_losses, config)

    print(f"\n{'='*60}")
    print("Training Complete!")
    print(f"Best Reward: {best_reward:.2f}")
    print(f"{'='*60}\n")

def plot_training_results(rewards, losses, config):
    """Plot training metrics"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot rewards
    ax1.plot(rewards, alpha=0.6, label='Episode Reward')
    window = 20
    if len(rewards) >= window:
        moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        ax1.plot(range(window-1, len(rewards)), moving_avg,
                label=f'Moving Avg ({window} episodes)', linewidth=2)
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Total Reward')
    ax1.set_title('Training Rewards')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot losses
    ax2.plot(losses, alpha=0.6, label='Episode Loss', color='red')
    if len(losses) >= window:
        moving_avg = np.convolve(losses, np.ones(window)/window, mode='valid')
        ax2.plot(range(window-1, len(losses)), moving_avg,
                label=f'Moving Avg ({window} episodes)', linewidth=2, color='darkred')
    ax2.set_xlabel('Episode')
    ax2.set_ylabel('Average Loss')
    ax2.set_title('Training Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_path = os.path.join(config['paths']['logs_dir'], 'training_plot.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Training plot saved to {plot_path}")
    plt.show()

if __name__ == "__main__":
    # Load configuration
    config = load_config('config.yaml')
    # Start training
    train(config)