from env import TrafficEnv

def evaluate(policy, cfg="sim.sumocfg", gui=False):
    env = TrafficEnv(cfg=cfg, gui=gui)
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

    fixed = lambda state, t: (t // 8) % 2
    rand = lambda state, t: random.choice([0, 1])

    print("stale swiatla:", evaluate(fixed))
    print("losowy agent:", evaluate(rand))