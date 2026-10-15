import random
from env import TrafficEnv

env = TrafficEnv(gui=True)
state = env.reset()
print("stan poczatkowy:", state)

total = 0
done = False

while not done:
    action = random.choice([0, 1])
    state, reward, done = env.step(action)
    total += reward

print("suma nagrod:", total)
env.close()