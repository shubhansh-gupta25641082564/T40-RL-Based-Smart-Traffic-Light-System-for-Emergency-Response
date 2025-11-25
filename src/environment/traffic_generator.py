import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_routes(output_file, num_vehicles=10000, num_emergency=2000):
    """
    Generate vehicle routes for simulation

    Args:
        output_file: Path to save route file
        num_vehicles: Number of civilian vehicles
        num_emergency: Number of emergency vehicles
    """
    routes = ET.Element('routes')

    # Vehicle types
    civilian_vtype = ET.SubElement(routes, 'vType')
    civilian_vtype.set('id', 'civilian')
    civilian_vtype.set('accel', '2.6')
    civilian_vtype.set('decel', '4.5')
    civilian_vtype.set('sigma', '0.5')
    civilian_vtype.set('length', '5')
    civilian_vtype.set('maxSpeed', '13.89')
    civilian_vtype.set('color', '0,1,0')  # Green

    emergency_vtype = ET.SubElement(routes, 'vType')
    emergency_vtype.set('id', 'emergency')
    emergency_vtype.set('vClass', 'emergency')
    emergency_vtype.set('accel', '3.5')
    emergency_vtype.set('decel', '5.0')
    emergency_vtype.set('sigma', '0')
    emergency_vtype.set('length', '7')
    emergency_vtype.set('maxSpeed', '20')
    emergency_vtype.set('color', '1,0,0')  # Red
    emergency_vtype.set('guiShape', 'emergency')
    ev_param = ET.SubElement(emergency_vtype, 'param')
    ev_param.set('key', 'has.bluelight.device')
    ev_param.set('value', 'true')

    # Define all valid start-to-end routes:
    # Each is a pair [INCOMING_EDGE, OUTGOING_EDGE]
    routes_list = [
        ['N2C', 'C2E'],
        ['N2C', 'C2W'],
        ['N2C', 'C2S'],
        ['E2C', 'C2N'],
        ['E2C', 'C2W'],
        ['E2C', 'C2S'],
        ['W2C', 'C2N'],
        ['W2C', 'C2E'],
        ['W2C', 'C2S'],
        ['S2C', 'C2N'],
        ['S2C', 'C2E'],
        ['S2C', 'C2W'],
    ]

    all_vehicles = []

    # Civilian vehicles: Random route
    for i in range(num_vehicles):
        depart_time = random.uniform(0, 7200)
        route_edges = random.choice(routes_list)
        all_vehicles.append({
            "id": f"civilian_{i}",
            "type": "civilian",
            "depart": depart_time,
            "edges": route_edges
        })

    for i in range(num_emergency):
        depart_time = random.uniform(100, 7100)
        route_edges = random.choice(routes_list)
        all_vehicles.append({
            "id": f"emergency_{i}",
            "type": "emergency",
            "depart": depart_time,
            "edges": route_edges
        })

    # SORT List by depart!
    all_vehicles.sort(key=lambda v: v["depart"])
    
    # Write vehicles to XML
    for v in all_vehicles:
        vehicle = ET.SubElement(routes, 'vehicle')
        vehicle.set('id', v['id'])
        vehicle.set('type', v['type'])
        vehicle.set('depart', str(v['depart']))
        route = ET.SubElement(vehicle, 'route')
        route.set('edges', ' '.join(v['edges']))

    xml_str = minidom.parseString(ET.tostring(routes)).toprettyxml(indent="   ")
    with open(output_file, 'w') as f:
        f.write(xml_str)

    print(f"✓ Generated {num_vehicles} civilian and {num_emergency} emergency vehicles")
    print(f"✓ Routes saved to: {output_file}")

if __name__ == "__main__":
    import os
    os.makedirs('data/networks', exist_ok=True)
    generate_routes('data/networks/intersection.rou.xml', num_vehicles=10000, num_emergency=2000)