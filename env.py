import traci


class TrafficEnv:
    def __init__(self, cfg="sim.sumocfg", tls_id="B1", gui=False,
                 green_phases=(0,2), yellow_time=3, step_len=5):
        self.cfg = cfg
        self.tls_id = tls_id
        self.gui = gui
        self.green_phases = green_phases
        self.yellow_time = yellow_time
        self.step_len = step_len
        self.current = 0
        self.started = False