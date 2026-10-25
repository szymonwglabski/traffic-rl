import sys
import torch

from qnetwork import QNetwork
from dqn import select_action, scale
from evaluate import evaluate

RUN = sys.argv[1]
ROUTE = "routes_high_4.rou.xml"

model = QNetwork()
model.load_state_dict(torch.load(f"model_{RUN}.pt"))
model.eval()

fixed = lambda state, t: (t//2) % 2
agent = lambda state, t: select_action(model, scale(state), 0.0)

print("stałe światła 10s: ", evaluate(fixed, route_file=ROUTE, gui=True))
print("agent DQN: ", evaluate(agent, route_file=ROUTE, gui=True))