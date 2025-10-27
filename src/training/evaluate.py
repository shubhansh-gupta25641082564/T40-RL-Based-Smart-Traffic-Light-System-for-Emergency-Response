import os
import sys
import yaml
import numpy as np
from tqdm import tqdm

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from src.environment.traffic_environment import TrafficEnvironment
from src.agent.dqn_agent import DQNAgent

def evaluate(config, model_path, num_episodes=10, use_gui=True):
    """
    Evaluate trained model

    Args:
        config: Configuration dictionary
        model_path: Path to trained model
        num_episodes: Number of evaluation episodes
        use_gui: Whether to visualize
    """
    # Initialize environment
    env = TrafficEnvironment(
        net_file=config['environment']['net_file'],
        route_file=config['environment']['route_file'],
        use_gui=use_gui,
        delta_time=config['environment']['delta_time']
    )

    # Initialize agent
    agent = DQNAgent(
        state_size=env.state_size,
        action_size=env.action_size,
        config=config['agent']
    )

    # Load model
    agent.load(model_path)
    agent.epsilon = 0  # No exploration during evaluation

    # Evaluation metrics
    episode_rewards = []
    emergency_response_times = []
    average_waiting_times = []

    print(f"\n{'='*60}")
    print(f"Evaluating Model: {num_episodes} episodes")
    print(f"{'='*60}\n")

    for episode in range(1, num_episodes + 1):
        state = env.reset()
        episode_reward = 0
        done = False

        ev_detected_time = None
        ev_cleared_time = None

        print(f"Episode {episode}/{num_episodes}")

        while not done:
            # Select action (exploitation only)
            action = agent.select_action(state, training=False)

            # Take step
            next_state, reward, done, info = env.step(action)

            # Track emergency vehicles
            if info['emergency_present'] and ev_detected_time is None:
                ev_detected_time = env.current_step
                print(f"  → Emergency vehicle detected at step {ev_detected_time}")

            if ev_detected_time and not info['emergency_present'] and ev_cleared_time is None:
                ev_cleared_time = env.current_step
                response_time = ev_cleared_time - ev_detected_time
                emergency_response_times.append(response_time)
                print(f"  ✓ Emergency vehicle cleared in {response_time} seconds")

            state = next_state
            episode_reward += reward

        episode_rewards.append(episode_reward)
        avg_waiting = info['total_waiting_time'] / max(info['vehicles_in_network'], 1)
        average_waiting_times.append(avg_waiting)

        print(f"  Reward: {episode_reward:.2f}")
        print(f"  Avg Waiting Time: {avg_waiting:.2f}s")
        print()

    env.close()

    # Print summary
    print(f"\n{'='*60}")
    print("Evaluation Summary")
    print(f"{'='*60}")
    print(f"Average Reward: {np.mean(episode_rewards):.2f} ± {np.std(episode_rewards):.2f}")
    print(f"Average Waiting Time: {np.mean(average_waiting_times):.2f}s")
    if emergency_response_times:
        print(f"Avg Emergency Response Time: {np.mean(emergency_response_times):.2f}s")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    config_path = 'config.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    model_path = config['paths']['best_model']

    evaluate(config, model_path, num_episodes=10, use_gui=False)