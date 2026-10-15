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

    def _get_state(self):
        halting = [traci.lane.getLastStepHaltingNumber(l) for l in self.lanes]
        phase = [0] * len(self.green_phases)
        phase[self.current] = 1
        return halting + phase

    def reset(self):
        if self.started:
            traci.close()
        binary = "sumo-gui" if self.gui else "sumo"
        traci.start([binary, "-c", self.cfg, "--no-warnings", "true"])
        self.started = True

        self.lanes = sorted(set(traci.trafficlight.getControlledLanes(self.tls_id)))
        self.current = 0
        traci.trafficlight.setPhase(self.tls_id, self.green_phases[0])
        traci.trafficlight.setPhaseDuration(self.tls_id, 1000)
        return self._get_state()

    def step(self, action):
        if action != self.current:
            yellow = self.green_phases[self.current] + 1
            traci.trafficlight.setPhaseDuration(self.tls_id, yellow)
            traci.trafficlight.setPhaseDuration(self.tls_id, self.yellow_time)
            for _ in range(self.yellow_time):
                traci.simulationStep()
            traci.trafficlight.setPhase(self.tls_id, self.green_phases[action])
            self.current = action

        traci.trafficlight.setPhaseDuration(self.tls_id, 1000)
        for _ in range(self.step_len):
            traci.simulationStep()

        state = self._get_state()
        reward = -sum(state[:len(self.lanes)])
        done = traci.simulation.getMinExpectedNumber() == 0
        return state, reward, done

    def close(self):
        if self.started:
            traci.close()
            self.started = False