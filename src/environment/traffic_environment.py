import os
import sys
import traci
import numpy as np
import xml.etree.ElementTree as ET

class TrafficEnvironment:
    def __init__(self, netfile, routefile, usegui=False, maxsteps=7200, deltatime=10):
        self.netfile = netfile
        self.routefile = routefile
        self.usegui = usegui
        self.maxsteps = maxsteps
        self.deltatime = deltatime

        # All traffic light IDs
        self.tls_ids = self._get_tls_ids_from_network(netfile)

        # Per-tl incoming lanes
        self.tl_incoming_lanes = self._get_incoming_lanes_all_tls(netfile)

        # Per-tl number of phases (actions)
        self.tl_num_phases = {tls: self._get_num_phases(netfile, tls) for tls in self.tls_ids}

        # State: for each lane 2 features (queue + wait), for all incoming lanes of all tls
        self.n_tls = len(self.tls_ids)
        self.lane_counts = [len(lanes) for lanes in self.tl_incoming_lanes.values()]
        self.statesize = sum(lc*2 for lc in self.lane_counts)
        self.actionsize = sum(self.tl_num_phases.values()) # not used; actions handled as per-tl array

        self.currentstep = 0
        self.totalwaitingtime = 0

    def _get_tls_ids_from_network(self, netfile):
        tree = ET.parse(netfile)
        root = tree.getroot()
        return [tl.get('id') for tl in root.findall('tlLogic')]

    def _get_incoming_lanes_all_tls(self, netfile):
        tree = ET.parse(netfile)
        root = tree.getroot()
        lanes_mapping = {}
        for junction in root.findall("junction"):
            if junction.get("type") == "traffic_light":
                inc_lanes = junction.get("incLanes").split()
                lanes_mapping[junction.get("id")] = inc_lanes
        return lanes_mapping

    def _get_num_phases(self, netfile, tls_id):
        tree = ET.parse(netfile)
        for node in tree.findall("tlLogic"):
            if node.attrib["id"] == tls_id:
                return len(node.findall("phase"))
        return 2  # fallback/safe

    def start(self):
        sumo_binary = "sumo-gui" if self.usegui else "sumo"
        sumo_cmd = [
            sumo_binary, "-n", self.netfile, "-r", self.routefile,
            "--step-length", "0.001", "--waiting-time-memory", "10000",
            "--time-to-teleport", "-1", "--no-step-log", "true"
        ]
        traci.start(sumo_cmd)
        self.currentstep = 0

    def reset(self):
        if traci.isLoaded():
            traci.close()
        self.start()
        for _ in range(5):
            traci.simulationStep()
        self.totalwaitingtime = 0
        return self.get_state()

    def get_state(self):
        state = []
        for tls_id in self.tls_ids:
            for lane in self.tl_incoming_lanes[tls_id]:
                try:
                    q = traci.lane.getLastStepHaltingNumber(lane)
                    vids = traci.lane.getLastStepVehicleIDs(lane)
                    w = np.mean([traci.vehicle.getWaitingTime(vid) for vid in vids]) if vids else 0
                except Exception as e:
                    q, w = 0, 0
                state.extend([q, w])
        state = np.array(state, dtype=np.float32)
        return state

    def step(self, action):
        assert len(action) == len(self.tls_ids), f"Action must have one phase per intersection: {len(action)} vs {len(self.tls_ids)}"
        for i, tls in enumerate(self.tls_ids):
            num_phases = self.tl_num_phases[tls]
            valid_phase = int(action[i]) % num_phases
            traci.trafficlight.setPhase(tls, valid_phase)
        for _ in range(self.deltatime):
            traci.simulationStep()
            self.currentstep += 1

        next_state = self.get_state()
        reward = self.calculate_reward()
        done = self.currentstep >= self.maxsteps or traci.simulation.getMinExpectedNumber() <= 0
        info = dict(totalwaitingtime=self.totalwaitingtime, vehiclesinnetwork=traci.vehicle.getIDCount())
        print(f"[STEP] Reward: {reward}, Done: {done}, Info: {info}")
        return next_state, reward, done, info

    def calculate_reward(self):
        reward = 0.0
        all_vehicles = traci.vehicle.getIDList()
        current_wait = sum(traci.vehicle.getWaitingTime(vid) for vid in all_vehicles)
        emvs = [vid for vid in all_vehicles if "emergency" in vid]
        normal_vs = [vid for vid in all_vehicles if "emergency" not in vid]
        emv_wait = sum(traci.vehicle.getWaitingTime(vid) for vid in emvs)
        civilian_wait = sum(traci.vehicle.getWaitingTime(vid) for vid in normal_vs)
        reward = - civilian_wait - 10 * emv_wait  # EMV wait time much more heavily penalized!
        self.totalwaitingtime = current_wait
        print(f"[REWARD] Civilian wait {civilian_wait:.2f}, EMV wait {emv_wait:.2f}, Reward {reward:.2f}")
        return reward

    def close(self):
        if traci.isLoaded():
            traci.close()