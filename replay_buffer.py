import random
from collections import deque
import torch


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, n):
        batch = random.sample(self.buffer, n)
        state, action, reward, next_state, done = zip(*batch)
        state = torch.tensor(state, dtype=torch.float32)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float32)
        next_state = torch.tensor(next_state, dtype=torch.float32)
        done = torch.tensor(done, dtype=torch.float32)
        return state, action, reward, next_state, done

    def __len__(self):
            return len(self.buffer)

if __name__ == "__main__":
    buf = ReplayBuffer(capacity=100)
    for i in range(150):
        buf.add([i] * 6, i % 2, -float(i), [i + 1] * 6, i == 149)

    print(len(buf))
    s, a, r, s2, d = buf.sample(8)
    print(s.shape, s.dtype)
    print(a.shape, a.dtype)
    print(r.shape, s2.shape, d.shape)
    print(s[:, 0])
