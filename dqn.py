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

def learn_step(model, target_net, buffer, optimizer, gamma, batch_size):
    states, actions, rewards, next_states, dones = buffer.sample(batch_size)

    q_all = model(states)
    q_taken = q_all.gather(1, actions.unsqueeze(1)).squeeze(1)
    
    with torch.no_grad():
        next_q = target_net(next_states).max(dim=1).values
        goal = rewards + gamma * next_q * (1 - dones)

    loss = nn.functional.mse_loss(q_taken, goal)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()

