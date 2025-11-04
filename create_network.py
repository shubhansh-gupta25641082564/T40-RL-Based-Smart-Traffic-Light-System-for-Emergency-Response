# this is an alternate way to create the network using sumolib instead of netedit

import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_3x3_grid_network(output_file, grid_spacing=500):
    """
    Create a complete 3x3 grid intersection network
    with proper SUMO junction types
    """
    
    # Create root network element
    net = ET.Element('net', {
        'version': '1.20',
        'junctionCornerDetail': '5',
        'limitTurnSpeed': '5.50',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/net_file.xsd'
    })
    
    # Location/boundary
    boundary = grid_spacing * 1.5
    location = ET.SubElement(net, 'location', {
        'netOffset': '0.00,0.00',
        'convBoundary': f'{-boundary},{-boundary},{boundary},{boundary}',
        'origBoundary': '10000000000.00,10000000000.00,-10000000000.00,-10000000000.00',
        'projParameter': '!'
    })
    
    # 9 center junctions (traffic lights)
    centers = {
        'C_00': {'x': -grid_spacing, 'y': grid_spacing},    
        'C_10': {'x': 0, 'y': grid_spacing},                
        'C_20': {'x': grid_spacing, 'y': grid_spacing},     
        'C_01': {'x': -grid_spacing, 'y': 0},               
        'C_11': {'x': 0, 'y': 0},                           
        'C_21': {'x': grid_spacing, 'y': 0},                
        'C_02': {'x': -grid_spacing, 'y': -grid_spacing},   
        'C_12': {'x': 0, 'y': -grid_spacing},               
        'C_22': {'x': grid_spacing, 'y': -grid_spacing},    
    }
    
    # External junctions (entry/exit points) - use 'priority' type
    dummy_junctions = {
        # Top entries
        'N_00': {'x': -grid_spacing, 'y': grid_spacing + 400},
        'N_10': {'x': 0, 'y': grid_spacing + 400},
        'N_20': {'x': grid_spacing, 'y': grid_spacing + 400},
        # Bottom exits
        'S_00': {'x': -grid_spacing, 'y': -grid_spacing - 400},
        'S_10': {'x': 0, 'y': -grid_spacing - 400},
        'S_20': {'x': grid_spacing, 'y': -grid_spacing - 400},
        # Left entries
        'W_00': {'x': -grid_spacing - 400, 'y': grid_spacing},
        'W_01': {'x': -grid_spacing - 400, 'y': 0},
        'W_02': {'x': -grid_spacing - 400, 'y': -grid_spacing},
        # Right exits
        'E_00': {'x': grid_spacing + 400, 'y': grid_spacing},
        'E_01': {'x': grid_spacing + 400, 'y': 0},
        'E_02': {'x': grid_spacing + 400, 'y': -grid_spacing},
    }
    
    # Add all TRAFFIC LIGHT junctions to XML
    for junc_id, coords in centers.items():
        ET.SubElement(net, 'junction', {
            'id': junc_id,
            'type': 'traffic_light',  # ✅ CORRECT TYPE
            'x': str(coords['x']),
            'y': str(coords['y']),
            'incLanes': '',
            'intLanes': '',
            'shape': ''
        })
    
    # Add PRIORITY junctions (entry/exit) to XML
    for junc_id, coords in dummy_junctions.items():
        ET.SubElement(net, 'junction', {
            'id': junc_id,
            'type': 'priority',  # ✅ CORRECT TYPE (not 'uncontrolled')
            'x': str(coords['x']),
            'y': str(coords['y']),
            'incLanes': '',
            'intLanes': '',
            'shape': ''
        })
    
    # Create edges connecting junctions
    edge_counter = 0
    all_edges = []
    
    # Horizontal edges (East-West)
    horizontal_pairs = [
        # Top row
        [('W_00', 'C_00'), ('C_00', 'C_10'), ('C_10', 'C_20'), ('C_20', 'E_00')],
        # Middle row
        [('W_01', 'C_01'), ('C_01', 'C_11'), ('C_11', 'C_21'), ('C_21', 'E_01')],
        # Bottom row
        [('W_02', 'C_02'), ('C_02', 'C_12'), ('C_12', 'C_22'), ('C_22', 'E_02')],
    ]
    
    # Vertical edges (North-South)
    vertical_pairs = [
        # Left column
        [('N_00', 'C_00'), ('C_00', 'C_01'), ('C_01', 'C_02'), ('C_02', 'S_00')],
        # Center column
        [('N_10', 'C_10'), ('C_10', 'C_11'), ('C_11', 'C_12'), ('C_12', 'S_10')],
        # Right column
        [('N_20', 'C_20'), ('C_20', 'C_21'), ('C_21', 'C_22'), ('C_22', 'S_20')],
    ]
    
    # Add horizontal edges
    for row in horizontal_pairs:
        for (from_junc, to_junc) in row:
            edge_id = f"E_{edge_counter}"
            all_edges.append((edge_id, from_junc, to_junc))
            edge_counter += 1
    
    # Add vertical edges
    for col in vertical_pairs:
        for (from_junc, to_junc) in col:
            edge_id = f"E_{edge_counter}"
            all_edges.append((edge_id, from_junc, to_junc))
            edge_counter += 1
    
    # Write edges to XML
    for edge_id, from_junc, to_junc in all_edges:
        edge = ET.SubElement(net, 'edge', {
            'id': edge_id,
            'from': from_junc,
            'to': to_junc,
            'priority': '-1'
        })
        
        # Add 4 lanes per edge
        for lane_idx in range(4):
            ET.SubElement(edge, 'lane', {
                'id': f"{edge_id}_{lane_idx}",
                'index': str(lane_idx),
                'speed': '13.89',
                'length': '100.00',
                'shape': '0,0 100,0'
            })
    
    # Pretty print XML
    xml_string = minidom.parseString(ET.tostring(net)).toprettyxml(indent='  ')
    xml_string = '\n'.join([line for line in xml_string.split('\n') if line.strip()])
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(xml_string)
    
    # Print summary
    print("\n" + "="*60)
    print("✓ 3x3 Grid Network Created Successfully!")
    print("="*60)
    print(f"File: {output_file}")
    print(f"Traffic Light Junctions: {len(centers)}")
    print(f"Priority Junctions (Entry/Exit): {len(dummy_junctions)}")
    print(f"Total Junctions: {len(centers) + len(dummy_junctions)}")
    print(f"Total Edges: {len(all_edges)}")
    print(f"Lanes per Edge: 4")
    print("="*60 + "\n")

if __name__ == "__main__":
    import os
    
    os.makedirs('data/networks', exist_ok=True)
    create_3x3_grid_network(
        output_file='data/networks/intersection_3x3.net.xml',
        grid_spacing=500
    )