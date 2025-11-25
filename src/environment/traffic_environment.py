import os
import sys
import traci
import numpy as np

class TrafficEnvironment:
    def __init__(self, netfile, routefile, usegui=False, maxsteps=7200, deltatime=10):
        print("[Env] Initializing TrafficEnvironment...")
        self.netfile = netfile
        self.routefile = routefile
        self.usegui = usegui
        self.maxsteps = maxsteps
        self.deltatime = deltatime
        self.tlid = "C"
        self.currentstep = 0
        self.totalwaitingtime = 0

        # Assume lanes by naming convention: modify if different
        self.incominglanes = [
            "NC0", "NC1", "NC2", "SC0", "SC1", "SC2",
            "EC0", "EC1", "EC2", "WC0", "WC1", "WC2", "NC3", "SC3", "EC3", "WC3"
        ]
        self.statesize = len(self.incominglanes)*2  # queue length + waiting time per lane
        self.actionsize = 2  # [NS green, EW green]
        print(f"[Env] State size: {self.statesize}, Action size: {self.actionsize}")

    def start(self):
        sumoBinary = "sumo-gui" if self.usegui else "sumo"
        sumoCmd = [
            sumoBinary, "-n", self.netfile, "-r", self.routefile,
            "--step-length", "0.001", "--waiting-time-memory", "10000",
            "--time-to-teleport", "-1", "--no-step-log", "true"
        ]
        print(f"[Env] Starting SUMO with: {' '.join(sumoCmd)}")
        traci.start(sumoCmd)
        traci.trafficlight.setPhaseDuration(self.tlid, 1000)
        self.currentstep = 0

    def reset(self):
        print("[Env] Resetting simulation...")
        if traci.isLoaded():
            traci.close()
        self.start()
        for _ in range(5):
            traci.simulationStep()
        self.totalwaitingtime = 0
        print("[Env] Environment reset complete.")
        return self.get_state()

    def get_state(self):
        print("[Env] Fetching state...")
        state = []
        for lane in self.incominglanes:
            queuelength = traci.lane.getLastStepHaltingNumber(lane)
            vehicleids = traci.lane.getLastStepVehicleIDs(lane)
            waitingtime = sum(traci.vehicle.getWaitingTime(vid) for vid in vehicleids)
            state.extend([queuelength, waitingtime])
        print("[Env] Current state:", state)
        return np.array(state, dtype=np.float32)

    def check_emergency_vehicles(self):
        emergencypresent = False
        evdirection = None
        allvehicles = traci.vehicle.getIDList()
        for vid in allvehicles:
            if "emergency" in vid:
                edgeid = traci.vehicle.getRoadID(vid)
                if edgeid in ["NC", "SC", "EC", "WC"]:
                    position = traci.vehicle.getLanePosition(vid)
                    lanelength = traci.lane.getLength(traci.vehicle.getLaneID(vid))
                    distancetojunction = lanelength - position
                    if distancetojunction < 100:
                        emergencypresent = True
                        evdirection = edgeid[0]  # N/S/E/W
                        print("[Env] Emergency vehicle detected in direction:", evdirection)
                        break
        return emergencypresent, evdirection

    def step(self, action):
        emergencypresent, evdirection = self.check_emergency_vehicles()
        if emergencypresent:
            # Prioritize action according to direction
            action = 0 if evdirection in ["N", "S"] else 1
            print("[Env] Overriding action, emergency priority:", action)
        traci.trafficlight.setPhase(self.tlid, 0 if action == 0 else 2) # Example, NS=0, EW=2
        for _ in range(self.deltatime):
            traci.simulationStep()
            self.currentstep += 1
        next_state = self.get_state()
        reward = self.calculate_reward(emergencypresent)
        done = self.currentstep >= self.maxsteps or traci.simulation.getMinExpectedNumber() == 0
        info = {
            "emergencypresent": emergencypresent,
            "totalwaitingtime": self.totalwaitingtime,
            "vehiclesinnetwork": traci.vehicle.getIDCount()
        }
        print(f"[Env] Step info: action={action}, reward={reward}, done={done}, info={info}")
        return next_state, reward, done, info

    def calculate_reward(self, emergencypresent=False):
        allvehicles = traci.vehicle.getIDList()
        currentwaitingtime = sum(traci.vehicle.getWaitingTime(vid) for vid in allvehicles)
        reward = -currentwaitingtime
        if emergencypresent:
            for vid in allvehicles:
                if "emergency" in vid and traci.vehicle.getSpeed(vid) > 5:
                    reward += 200
        self.totalwaitingtime = currentwaitingtime
        print(f"[Env] Calculated reward: {reward}")
        return reward

    def close(self):
        print("[Env] Closing simulation...")
        if traci.isLoaded():
            traci.close()