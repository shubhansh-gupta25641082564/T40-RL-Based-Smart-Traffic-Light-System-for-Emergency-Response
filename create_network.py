import os
import sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Set SUMO_HOME")

import sumolib

# Create nodes
net = sumolib.net.Net()

# Define node positions
nodes = {
    'N': (0, 500),
    'S': (0, -500),
    'E': (500, 0),
    'W': (-500, 0),
    'C': (0, 0)  # Center junction
}

# Create network file content
net_content = '''<?xml version="1.16" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <location netOffset="0.00,0.00" convBoundary="-500.00,-500.00,500.00,500.00"/>
    
    <edge id="N_C" from="N" to="C" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="C_N" from="C" to="N" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="S_C" from="S" to="C" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="C_S" from="C" to="S" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="E_C" from="E" to="C" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="C_E" from="C" to="E" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="W_C" from="W" to="C" priority="-1" numLanes="4" speed="13.89"/>
    <edge id="C_W" from="C" to="W" priority="-1" numLanes="4" speed="13.89"/>
    
    <junction id="N" type="priority" x="0.00" y="500.00"/>
    <junction id="S" type="priority" x="0.00" y="-500.00"/>
    <junction id="E" type="priority" x="500.00" y="0.00"/>
    <junction id="W" type="priority" x="-500.00" y="0.00"/>
    <junction id="C" type="traffic_light" x="0.00" y="0.00"/>
</net>'''

# Save network
os.makedirs('data/networks', exist_ok=True)
with open('data/networks/intersection.net.xml', 'w') as f:
    f.write(net_content)

print("✓ Network created: data/networks/intersection.net.xml")