import torch
import torch.nn as nn
import random
import time

from replay_buffer import ReplayBuffer
from qnetwork import QNetwork
from env import TrafficEnv
from dqn import select_action, learn_step, scale

GAMMA = 0.95
LR = 1e-3
BATCH = 64
BUFFER_SIZE = 20000
WARMUP = 1000
TARGET_EVERY = 200
EPISODES = 500
EPS_START, EPS_END = 1.0, 0.05

model = QNetwork()
target_net = QNetwork()
target_net.load_state_dict(model.state_dict())
route_files = [f"routes_{kind}_{number}.rou.xml" for kind in ("low", "mid", "high")
                                for number in (1, 2, 3)]
env = TrafficEnv(route_files = route_files, gui=False)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
buffer = ReplayBuffer(BUFFER_SIZE)

counter = 0
results = []

try:
    for episode in range(EPISODES):
        start = time.time()
        epsilon = max(EPS_END, EPS_START - episode / (0.7 * EPISODES))
        state = env.reset()
        done = False
        steps = 0
        total_reward = 0.0

        while not done:
            action = select_action(model=model, state=scale(state), epsilon=epsilon)
            next_state, reward, done = env.step(action=action)
            buffer.add(scale(state), action, reward / 10, scale(next_state), done)
            state = next_state
            steps += 1
            total_reward += reward

            if len(buffer) >= WARMUP:
                learn_step(model, target_net, buffer, optimizer, GAMMA, BATCH)
                counter += 1
                if counter % TARGET_EVERY == 0:
                    target_net.load_state_dict(model.state_dict())

        avg_halting = -total_reward / steps
        results.append(avg_halting)
        print(f"epizod {episode}, kroki: {steps}, epsilon: {epsilon:.2f}, "
              f"sr. stojacych aut: {avg_halting:.2f}, czas: {time.time() - start:.1f} s")

    torch.save(model.state_dict(), "model.pt")

finally:
    env.close()
    with open("results.csv", "w") as f:
        f.write("episode, avg_halting\n")
        for i, r in enumerate(results):
            f.write(f"{i}, {r}\n")

