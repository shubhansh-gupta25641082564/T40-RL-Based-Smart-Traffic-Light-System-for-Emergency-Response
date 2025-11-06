import numpy as np
import matplotlib.pyplot as plt
import os

# Paths to logs
logdir = "data/logs"
reward_file = os.path.join(logdir, "rewards.npy")
loss_file = os.path.join(logdir, "losses.npy")

# Load arrays
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
plt.savefig(os.path.join(logdir, "training_plot_separate.png"))
plt.show()