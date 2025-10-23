import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_routes(output_file, num_vehicles=1000, num_emergency=10):
    """
    Generate vehicle routes for simulation
    
    Args:
        output_file: Path to save route file
        num_vehicles: Number of civilian vehicles
        num_emergency: Number of emergency vehicles
    """
    
    # Create root element
    routes = ET.Element('routes')
    
    # Define vehicle types
    # Civilian vehicle type
    civilian_vtype = ET.SubElement(routes, 'vType')
    civilian_vtype.set('id', 'civilian')
    civilian_vtype.set('accel', '2.6')
    civilian_vtype.set('decel', '4.5')
    civilian_vtype.set('sigma', '0.5')
    civilian_vtype.set('length', '5')
    civilian_vtype.set('maxSpeed', '13.89')
    civilian_vtype.set('color', '0,1,0')  # Green
    
    # Emergency vehicle type
    ev_vtype = ET.SubElement(routes, 'vType')
    ev_vtype.set('id', 'emergency')
    ev_vtype.set('vClass', 'emergency')
    ev_vtype.set('accel', '3.5')
    ev_vtype.set('decel', '5.0')
    ev_vtype.set('sigma', '0')
    ev_vtype.set('length', '7')
    ev_vtype.set('maxSpeed', '20')
    ev_vtype.set('color', '1,0,0')  # Red
    ev_vtype.set('guiShape', 'emergency')
    
    # Add blue light device for emergency vehicles
    ev_param = ET.SubElement(ev_vtype, 'param')
    ev_param.set('key', 'has.bluelight.device')
    ev_param.set('value', 'true')
    
    # Define possible routes
    routes_list = [
        ['N_C', 'C_S'],  # North to South
        ['S_C', 'C_N'],  # South to North
        ['E_C', 'C_W'],  # East to West
        ['W_C', 'C_E'],  # West to East
        ['N_C', 'C_E'],  # North to East (right turn)
        ['N_C', 'C_W'],  # North to West (left turn)
        ['S_C', 'C_E'],  # South to East (left turn)
        ['S_C', 'C_W'],  # South to West (right turn)
        ['E_C', 'C_N'],  # East to North (left turn)
        ['E_C', 'C_S'],  # East to South (right turn)
        ['W_C', 'C_N'],  # West to North (right turn)
        ['W_C', 'C_S'],  # West to South (left turn)
    ]
    
    # Generate civilian vehicles
    for i in range(num_vehicles):
        vehicle = ET.SubElement(routes, 'vehicle')
        vehicle.set('id', f'civilian_{i}')
        vehicle.set('type', 'civilian')
        vehicle.set('depart', str(random.uniform(0, 3600)))  # Random departure in 1 hour
        
        # Select random route
        route_edges = random.choice(routes_list)
        route = ET.SubElement(vehicle, 'route')
        route.set('edges', ' '.join(route_edges))
    
    # Generate emergency vehicles
    for i in range(num_emergency):
        vehicle = ET.SubElement(routes, 'vehicle')
        vehicle.set('id', f'emergency_{i}')
        vehicle.set('type', 'emergency')
        vehicle.set('depart', str(random.uniform(100, 3500)))  # Spaced out
        
        # Prefer straight routes for emergency vehicles
        straight_routes = routes_list[:4]
        route_edges = random.choice(straight_routes)
        route = ET.SubElement(vehicle, 'route')
        route.set('edges', ' '.join(route_edges))
    
    # Pretty print XML
    xml_str = minidom.parseString(ET.tostring(routes)).toprettyxml(indent="   ")
    
    # Save to file
    with open(output_file, 'w') as f:
        f.write(xml_str)
    
    print(f"✓ Generated {num_vehicles} civilian and {num_emergency} emergency vehicles")
    print(f"✓ Routes saved to: {output_file}")

if __name__ == "__main__":
    import os
    os.makedirs('data/networks', exist_ok=True)
    generate_routes('data/networks/intersection.rou.xml', 
                   num_vehicles=1000, 
                   num_emergency=20)