import random
import torch
import torch.nn as nn


def select_action(model, state, epsilon):
    if random.random() < epsilon:
        return random.choice((0, 1))
    
    with torch.no_grad():
        s = torch.tensor([state], dtype=torch.float32)
        q = model(s)
        return q.argmax(dim=1).item()

if __name__ == "__main__":
    from qnetwork import QNetwork
    model = QNetwork()
    s = [0, 0, 0, 0, 1, 0]
    print([select_action(model, s, 0.0) for _ in range(10)])
    print([select_action(model, s, 1.0) for _ in range(10)])