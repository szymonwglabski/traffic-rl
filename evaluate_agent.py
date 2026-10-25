import torch
import sys

from qnetwork import QNetwork
from dqn import select_action, scale
from evaluate import evaluate

model = QNetwork()
RUN = sys.argv[1] if len(sys.argv) > 1 else "run1"
model.load_state_dict(torch.load(f"model_{RUN}.pt"))
model.eval()

agent = lambda state, t: select_action(model, scale(state), 0.0)

for kind in ("low", "mid", "high"):
    vals = [evaluate(agent, route_file=f"routes_{kind}_{s}.rou.xml")[1]
            for s in (4, 5, 6)]
    print(kind, round(sum(vals) / len(vals), 2))