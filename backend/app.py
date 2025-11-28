from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
import yaml
import threading
import numpy as np
import torch

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.environment.traffic_environment import TrafficEnvironment
from src.agent.dqn_agent import DQNAgent

# Create Flask app
app = Flask(__name__)
CORS(app)

# GLOBAL SIMULATION STATE
simulation_state = {
    'running': False,
    'env': None,
    'agent': None,
    'config': None,
    'episode': 0,
    'step': 0,
    'episode_reward': 0,
    'metrics': {
        'average_wait_time': 0,
        'total_vehicles': 0,
        'ev_count': 0,
        'ev_wait_time': 0,
        'rewards_history': [],
        'losses_history': []
    }
}

# INITIALIZATION
def initialize_simulation():
    """Initialize the simulation environment and agent"""
    try:
        config_path = os.getenv('CONFIG_PATH', 'config.yaml')
        with open(config_path, 'r') as f:
            simulation_state['config'] = yaml.safe_load(f)
        
        env = TrafficEnvironment(
            net_file=simulation_state['config']['environment']['netfile'],
            route_file=simulation_state['config']['environment']['routefile'],
            use_gui=simulation_state['config']['environment'].get('usegui', False),
            max_steps=simulation_state['config']['environment'].get('maxsteps', 36000),
            delta_time=simulation_state['config']['environment'].get('deltatime', 10)
        )
        
        agent = DQNAgent(
            state_size=env.state_size,
            action_size=env.action_size,
            config=simulation_state['config']['agent']
        )
        
        simulation_state['env'] = env
        simulation_state['agent'] = agent
        
        # Load best model if it exists
        best_model_path = simulation_state['config']['paths'].get('bestmodel')
        if best_model_path and os.path.exists(best_model_path):
            try:
                agent.load(best_model_path)
                app.logger.info(f"Loaded best model from {best_model_path}")
            except Exception as load_error:
                app.logger.warning(f"Could not load best model: {str(load_error)}. Using fresh agent.")
        
        return True
    except Exception as e:
        app.logger.error(f"Failed to initialize simulation: {str(e)}")
        return False

# HEALTH CHECK ENDPOINT
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'T40 Traffic Control Backend',
        'version': '1.0',
        'simulation_initialized': simulation_state['env'] is not None
    })

# INTERSECTIONS API
@app.route('/api/intersections', methods=['GET'])
def get_intersections():
    """Get all intersections with current state"""
    try:
        if simulation_state['env'] is None:
            return jsonify({'error': 'Simulation not initialized'}), 500
        
        env = simulation_state['env']
        intersections = [
            {
                'id': 'center',
                'name': 'Central Intersection',
                'tl_id': env.tl_id,
                'lanes': env.num_lanes,
                'state_size': env.state_size,
                'action_size': env.action_size,
                'current_step': env.current_step,
                'max_steps': env.max_steps
            }
        ]
        return jsonify(intersections), 200
    except Exception as e:
        app.logger.error(f"Error in get_intersections: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/intersections/<intersection_id>/signal', methods=['POST'])
def update_signal(intersection_id):
    """Manually update traffic signal"""
    try:
        if simulation_state['env'] is None:
            return jsonify({'error': 'Simulation not initialized'}), 500
        
        if not simulation_state['running']:
            return jsonify({'error': 'Simulation is not running'}), 400
        
        data = request.get_json()
        action = data.get('action', 0)
        
        env = simulation_state['env']
        next_state, reward, done, info = env.step(action)
        
        simulation_state['step'] += 1
        simulation_state['episode_reward'] += reward
        
        result = {
            'success': True,
            'intersection_id': intersection_id,
            'action': action,
            'reward': float(reward),
            'done': done,
            'info': {k: float(v) if isinstance(v, (int, float, np.number)) else v 
                    for k, v in info.items()}
        }
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"Error in update_signal: {str(e)}")
        return jsonify({'error': str(e)}), 500

# EMERGENCY VEHICLES API
@app.route('/api/ev-status', methods=['GET'])
def get_ev_status():
    """Get all active emergency vehicles"""
    try:
        if simulation_state['env'] is None:
            return jsonify({'error': 'Simulation not initialized'}), 500
        
        # Get EV status from environment
        env = simulation_state['env']
        ev_status = {
            'active_count': getattr(env, 'ev_count', 0),
            'total_wait_time': float(getattr(env, 'ev_wait_time', 0)),
            'emergency_vehicles': []
        }
        
        return jsonify(ev_status), 200
    except Exception as e:
        app.logger.error(f"Error in get_ev_status: {str(e)}")
        return jsonify({'error': str(e)}), 500

# METRICS API
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get performance metrics"""
    try:
        metrics = {
            'episode': simulation_state['episode'],
            'step': simulation_state['step'],
            'episode_reward': float(simulation_state['episode_reward']),
            'average_wait_time': float(simulation_state['metrics']['average_wait_time']),
            'total_vehicles': int(simulation_state['metrics']['total_vehicles']),
            'ev_count': int(simulation_state['metrics']['ev_count']),
            'ev_wait_time': float(simulation_state['metrics']['ev_wait_time']),
            'rewards_history': simulation_state['metrics']['rewards_history'][-100:] if simulation_state['metrics']['rewards_history'] else [],
            'losses_history': simulation_state['metrics']['losses_history'][-100:] if simulation_state['metrics']['losses_history'] else []
        }
        return jsonify(metrics), 200
    except Exception as e:
        app.logger.error(f"Error in get_metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500

# SIMULATION CONTROL API
@app.route('/api/simulation/status', methods=['GET'])
def get_status():
    """Get simulation status"""
    try:
        status = {
            'running': simulation_state['running'],
            'initialized': simulation_state['env'] is not None,
            'episode': simulation_state['episode'],
            'step': simulation_state['step'],
            'episode_reward': float(simulation_state['episode_reward']),
            'config': {
                'num_episodes': simulation_state['config']['training']['numepisodes'] if simulation_state['config'] else 0,
                'max_steps': simulation_state['config']['environment']['maxsteps'] if simulation_state['config'] else 0,
            } if simulation_state['config'] else None
        }
        return jsonify(status), 200
    except Exception as e:
        app.logger.error(f"Error in get_status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/init', methods=['POST'])
def init_simulation():
    """Initialize the simulation"""
    try:
        if initialize_simulation():
            return jsonify({'status': 'initialized', 'message': 'Simulation initialized successfully'}), 200
        else:
            return jsonify({'error': 'Failed to initialize simulation'}), 500
    except Exception as e:
        app.logger.error(f"Error in init_simulation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """Start the simulation"""
    try:
        if simulation_state['env'] is None:
            return jsonify({'error': 'Simulation not initialized. Call /api/simulation/init first'}), 400
        
        simulation_state['running'] = True
        simulation_state['step'] = 0
        simulation_state['episode_reward'] = 0
        simulation_state['episode'] += 1
        
        state = simulation_state['env'].reset()
        
        return jsonify({
            'status': 'started',
            'episode': simulation_state['episode'],
            'initial_state_size': len(state) if isinstance(state, (list, np.ndarray)) else 0
        }), 200
    except Exception as e:
        app.logger.error(f"Error in start_simulation: {str(e)}")
        simulation_state['running'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/stop', methods=['POST'])
def stop_simulation():
    """Stop the simulation"""
    try:
        simulation_state['running'] = False
        
        if simulation_state['metrics']['rewards_history'] is None:
            simulation_state['metrics']['rewards_history'] = []
        if simulation_state['metrics']['losses_history'] is None:
            simulation_state['metrics']['losses_history'] = []
        
        simulation_state['metrics']['rewards_history'].append(simulation_state['episode_reward'])
        
        return jsonify({
            'status': 'stopped',
            'episode': simulation_state['episode'],
            'total_reward': float(simulation_state['episode_reward']),
            'total_steps': simulation_state['step']
        }), 200
    except Exception as e:
        app.logger.error(f"Error in stop_simulation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/reset', methods=['POST'])
def reset_simulation():
    """Reset the simulation"""
    try:
        if simulation_state['env'] is None:
            return jsonify({'error': 'Simulation not initialized'}), 500
        
        simulation_state['running'] = False
        simulation_state['episode'] = 0
        simulation_state['step'] = 0
        simulation_state['episode_reward'] = 0
        simulation_state['metrics'] = {
            'average_wait_time': 0,
            'total_vehicles': 0,
            'ev_count': 0,
            'ev_wait_time': 0,
            'rewards_history': [],
            'losses_history': []
        }
        
        return jsonify({'status': 'reset', 'message': 'Simulation reset successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error in reset_simulation: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ERROR HANDLERS
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# REQUEST LOGGING
@app.before_request
def log_request():
    app.logger.debug(f"{request.method} {request.path}")

@app.after_request
def log_response(response):
    app.logger.debug(f"Response: {response.status}")
    return response

# MAIN
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Initialize simulation on startup
    initialize_simulation()
    
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=port,
        debug=debug,
        threaded=True
    )