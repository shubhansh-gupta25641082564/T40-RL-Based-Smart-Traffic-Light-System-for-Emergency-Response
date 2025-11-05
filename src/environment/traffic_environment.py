import os
import sys
import traci
import numpy as np

class TrafficEnvironment:
    def __init__(self, net_file, route_file, use_gui=False, max_steps=3600000, delta_time=1000):
        self.net_file = net_file
        self.route_file = route_file
        self.use_gui = use_gui
        self.max_steps = max_steps
        self.delta_time = delta_time
        self.tl_id = "C"
        self.num_lanes = 12
        self.state_size = self.num_lanes * 2
        self.action_size = 2
        self.current_step = 0
        self.total_waiting_time = 0

    def start(self):
        sumo_binary = "sumo-gui" if self.use_gui else "sumo"
        sumo_cmd = [
            sumo_binary,
            "-n", self.net_file,
            "-r", self.route_file,
            "--step-length", "0.001",
            "--waiting-time-memory", "10000",
            "--time-to-teleport", "-1",
            "--no-warnings", "true",
            "--no-step-log", "true",
        ]
        traci.start(sumo_cmd)
        traci.trafficlight.setPhaseDuration(self.tl_id, 1000)
        self.current_step = 0

    def reset(self):
        if traci.isLoaded():
            traci.close()
        self.start()
        for _ in range(5):
            traci.simulationStep()
        self.total_waiting_time = 0
        return self.get_state()

    def get_state(self):
        state = []
        incoming_lanes = [
            "N_C_0", "N_C_1", "N_C_2",
            "S_C_0", "S_C_1", "S_C_2",
            "E_C_0", "E_C_1", "E_C_2",
            "W_C_0", "W_C_1", "W_C_2",
        ]
        for lane in incoming_lanes:
            queue_length = traci.lane.getLastStepHaltingNumber(lane)
            vehicle_ids = traci.lane.getLastStepVehicleIDs(lane)
            waiting_time = (
                sum([traci.vehicle.getWaitingTime(vid) for vid in vehicle_ids]) / len(vehicle_ids) if vehicle_ids else 0
            )
            state.extend([queue_length, waiting_time])
        return np.array(state, dtype=np.float32)

    def check_emergency_vehicles(self):
        emergency_present = False
        ev_direction = None
        all_vehicles = traci.vehicle.getIDList()
        for vid in all_vehicles:
            if "emergency" in vid:
                edge_id = traci.vehicle.getRoadID(vid)
                if edge_id in ["N_C", "S_C", "E_C", "W_C"]:
                    position = traci.vehicle.getLanePosition(vid)
                    lane_length = traci.lane.getLength(traci.vehicle.getLaneID(vid))
                    distance_to_junction = lane_length - position
                    if distance_to_junction < 100:
                        emergency_present = True
                        ev_direction = edge_id[0]
                        break
        return emergency_present, ev_direction

    def step(self, action):
        emergency_present, ev_direction = self.check_emergency_vehicles()
        if emergency_present:
            action = 0 if ev_direction in ["N", "S"] else 1
        traci.trafficlight.setPhase(self.tl_id, 0 if action == 0 else 2)
        for _ in range(self.delta_time):
            traci.simulationStep()
            self.current_step += 1
        next_state = self.get_state()
        reward = self.calculate_reward(emergency_present)
        done = self.current_step >= self.max_steps or traci.simulation.getMinExpectedNumber() == 0
        info = {"emergency_present": emergency_present,
                "total_waiting_time": self.total_waiting_time,
                "vehicles_in_network": traci.vehicle.getIDCount()}
        return next_state, reward, done, info

    def calculate_reward(self, emergency_present=False):
        all_vehicles = traci.vehicle.getIDList()
        current_waiting_time = sum([traci.vehicle.getWaitingTime(vid) for vid in all_vehicles])
        reward = -current_waiting_time
        if emergency_present:
            for vid in all_vehicles:
                if "emergency" in vid and traci.vehicle.getSpeed(vid) > 5:
                    reward += 100
        self.total_waiting_time = current_waiting_time
        return reward

    def close(self):
        if traci.isLoaded(): traci.close()