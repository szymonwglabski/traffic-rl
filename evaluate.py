from env import TrafficEnv

def evaluate(policy, cfg="sim.sumocfg", gui=False, route_file=None):
    env = TrafficEnv(cfg=cfg, gui=gui, route_file=route_file)
    state = env.reset()
    total, steps, done = 0, 0, False
    while not done:
        action = policy(state, steps)
        state, reward, done = env.step(action)
        total += reward
        steps += 1
    env.close()
    return total, -total/steps

if __name__ == "__main__":
    import random

    def mean_over(policy, kind):
        vals = [evaluate(policy, route_file=f"routes_{kind}_{s}.rou.xml")[1]
                for s in (4, 5, 6)]
        return sum(vals) / len(vals)

    policies = {
        "stałe 10s": lambda state, t: (t // 2) % 2,
        "stałe 20s": lambda state, t: (t // 4) % 2,
        "stałe 40s": lambda state, t: (t // 8) % 2,
        "losowy": lambda state, t: random.choice([0, 1])
    }
    for kind in ("low", "mid", "high"):
        for name, pol in policies.items():
            print(kind, name, round(mean_over(pol, kind), 2))