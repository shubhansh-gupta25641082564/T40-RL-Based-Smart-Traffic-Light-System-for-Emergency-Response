import os
import sys
import traci
import numpy as np
class TrafficEnvironment:
    """
    Gym-style environment for traffic signal control
    """
    
    def __init__(self, net_file, route_file, use_gui=False, 
                 max_steps=3600, delta_time=2, step_length=0.001):
        """
        Initialize traffic environment
        
        Args:
            net_file: Path to SUMO network file
            route_file: Path to SUMO route file
            use_gui: Whether to use SUMO GUI
            max_steps: Maximum simulation steps
            delta_time: Time between RL decisions (seconds)
            step_length: SUMO simulation step length (seconds)
        """
        self.net_file = net_file
        self.route_file = route_file
        self.use_gui = use_gui
        self.max_steps = max_steps
        self.delta_time = delta_time
        self.step_length = step_length
        
        # Traffic light ID (from network)
        self.tl_id = 'C'  # Center junction
        
        # Define traffic light phases
        # Phase 0: North-South green
        # Phase 1: East-West green
        self.phases = [
            traci.trafficlight.Phase(30, "GGGGrrrrGGGGrrrr"),  # NS green
            traci.trafficlight.Phase(3,  "yyyyrrrryyyyrrrr"),  # NS yellow
            traci.trafficlight.Phase(30, "rrrrGGGGrrrrGGGG"),  # EW green
            traci.trafficlight.Phase(3,  "rrrryyyyrrrryyyy"),  # EW yellow
        ]
        
        # State and action spaces
        self.num_lanes = 12  # 3 incoming lanes × 4 directions
        self.state_size = self.num_lanes * 2  # Queue length + waiting time per lane
        self.action_size = 2  # Phase 0 or Phase 2 (NS or EW green)
        
        # Tracking
        self.current_step = 0
        self.total_waiting_time = 0
        self.emergency_vehicles = []
        
    def start(self):
        """Start SUMO simulation"""
        sumo_binary = 'sumo-gui' if self.use_gui else 'sumo'
        sumo_cmd = [
            sumo_binary,
            '-n', self.net_file,
            '-r', self.route_file,
            '--step-length', str(self.step_length),
            '--waiting-time-memory', '10000',
            '--time-to-teleport', '-1',
            '--no-warnings', 'true',
            '--no-step-log', 'true'
        ]
        
        traci.start(sumo_cmd)
        
        # Initialize traffic light
        # traci.trafficlight.setProgram(self.tl_id, 'custom')
        traci.trafficlight.setPhaseDuration(self.tl_id, 1000)  # Manual control
        
        self.current_step = 0
        print("✓ SUMO simulation started")
        
    def reset(self):
        """Reset environment to initial state"""
        if traci.isLoaded():
            traci.close()
        self.start()
        
        # Run few steps to initialize
        for _ in range(5):
            traci.simulationStep()
        
        return self.get_state()
    
    def get_state(self):
        """
        Get current state of traffic system
        
        Returns:
            numpy array of shape (state_size,)
        """
        state = []
        
        # Get incoming lanes for each direction
        incoming_lanes = [
            'N_C_0', 'N_C_1', 'N_C_2',  # North
            'S_C_0', 'S_C_1', 'S_C_2',  # South
            'E_C_0', 'E_C_1', 'E_C_2',  # East
            'W_C_0', 'W_C_1', 'W_C_2',  # West
        ]
        
        for lane in incoming_lanes:
            # Queue length (number of halted vehicles)
            queue_length = traci.lane.getLastStepHaltingNumber(lane)
            
            # Average waiting time
            vehicle_ids = traci.lane.getLastStepVehicleIDs(lane)
            if len(vehicle_ids) > 0:
                waiting_time = sum([traci.vehicle.getWaitingTime(vid) 
                                   for vid in vehicle_ids]) / len(vehicle_ids)
            else:
                waiting_time = 0
            
            state.extend([queue_length, waiting_time])
        
        return np.array(state, dtype=np.float32)
    
    def check_emergency_vehicles(self):
        """Check for emergency vehicles near intersection"""
        emergency_present = False
        ev_direction = None
        
        # Get all vehicles in simulation
        all_vehicles = traci.vehicle.getIDList()
        
        for vid in all_vehicles:
            if 'emergency' in vid:
                # Get vehicle's edge
                edge_id = traci.vehicle.getRoadID(vid)
                
                # Check if approaching intersection
                if edge_id in ['N_C', 'S_C', 'E_C', 'W_C']:
                    # Get distance to junction
                    position = traci.vehicle.getLanePosition(vid)
                    lane_length = traci.lane.getLength(traci.vehicle.getLaneID(vid))
                    distance_to_junction = lane_length - position
                    
                    # If within 100m of junction
                    if distance_to_junction < 100:
                        emergency_present = True
                        ev_direction = edge_id[0]  # N, S, E, or W
                        break
        
        return emergency_present, ev_direction
    
    def step(self, action):
        """
        Execute action and return next state
        
        Args:
            action: 0 for NS green, 1 for EW green
            
        Returns:
            next_state, reward, done, info
        """
        # Check for emergency vehicles
        emergency_present, ev_direction = self.check_emergency_vehicles()
        
        # Override action if emergency vehicle detected
        if emergency_present:
            if ev_direction in ['N', 'S']:
                action = 0  # NS green
            else:
                action = 1  # EW green
        
        # Set traffic light phase
        if action == 0:
            traci.trafficlight.setPhase(self.tl_id, 0)  # NS green
        else:
            traci.trafficlight.setPhase(self.tl_id, 2)  # EW green
        
        # Run simulation for delta_time steps
        for _ in range(int(self.delta_time / self.step_length)):
            traci.simulationStep()
            self.current_step += 1
        
        # Get next state
        next_state = self.get_state()
        
        # Calculate reward
        reward = self.calculate_reward(emergency_present)
        
        # Check if done
        done = self.current_step >= self.max_steps or traci.simulation.getMinExpectedNumber() == 0
        
        # Additional info
        info = {
            'emergency_present': emergency_present,
            'total_waiting_time': self.total_waiting_time,
            'vehicles_in_network': traci.vehicle.getIDCount()
        }
        
        return next_state, reward, done, info
    
    def calculate_reward(self, emergency_present=False):
        """
        Calculate reward based on traffic state
        
        Returns:
            reward (float)
        """
        # Get all vehicles
        all_vehicles = traci.vehicle.getIDList()
        
        # Calculate total waiting time
        current_waiting_time = sum([traci.vehicle.getWaitingTime(vid) 
                                   for vid in all_vehicles])
        
        # Reward is negative of waiting time change
        reward = -(current_waiting_time - self.total_waiting_time)
        
        # Bonus for emergency vehicle clearance
        if emergency_present:
            # Check if emergency vehicles are moving
            for vid in all_vehicles:
                if 'emergency' in vid:
                    speed = traci.vehicle.getSpeed(vid)
                    if speed > 5:  # Moving at decent speed
                        reward += 100  # Large bonus
        
        self.total_waiting_time = current_waiting_time
        
        return reward
    
    def close(self):
        """Close simulation"""
        if traci.isLoaded():
            traci.close()
        print("✓ Simulation closed")

# Test the environment
if __name__ == "__main__":
    env = TrafficEnvironment(
        net_file='data/networks/intersection.net.xml',
        route_file='data/networks/intersection.rou.xml',
        use_gui=True,
        step_length=0.001
    )
    
    print("Testing environment...")
    state = env.reset()
    print(f"Initial state shape: {state.shape}")
    
    for i in range(10000):
        action = np.random.randint(0, 2)
        next_state, reward, done, info = env.step(action)
        print(f"Step {i}: Action={action}, Reward={reward:.2f}, Done={done}")

        if done and info['vehicles_in_network'] == 0:
            print("✓ Test completed successfully")
            break
    
    env.close()