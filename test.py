import traci

traci.start(["sumo-gui", "-c", "sim.sumocfg"])

tls_id = "B1"

logic = traci.trafficlight.getAllProgramLogics(tls_id)[0]
for i, p in enumerate(logic.phases):
    print(i, p.duration, p.state)

links = traci.trafficlight.getControlledLinks("B1")
for i, l in enumerate(links):
    print(i, l)

for step in range(300):
    traci.simulationStep()
    if step % 20 == 0:
        print(step,
              "aut:", traci.vehicle.getIDCount(),
              "swiatla:", traci.trafficlight.getRedYellowGreenState(tls_id))
    if step == 100:
        traci.trafficlight.setPhase(tls_id, 2)

traci.close()