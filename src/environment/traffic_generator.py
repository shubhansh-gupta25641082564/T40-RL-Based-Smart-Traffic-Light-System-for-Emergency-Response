import random
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os


def load_routes_from_json(paths_file):
    """
    Load all possible routes from all_vehicle_paths.json.

    JSON structure:
    {
      "sourceEdge -> destEdge": [
        ["edge1", "edge2", ...],
        ["edge1", "edge5", ...],
        ...
      ],
      ...
    }

    We flatten this into a simple list of edge sequences.
    """
    with open(paths_file, "r") as f:
        data = json.load(f)

    routes_list = []
    for _, path_variants in data.items():
        for edges in path_variants:
            # Ensure it's a non-empty list
            if isinstance(edges, list) and len(edges) > 0:
                routes_list.append(tuple(edges))

    if not routes_list:
        raise ValueError("No routes found in all_vehicle_paths.json")

    return routes_list


def generate_routes(
    output_file,
    network_file,
    paths_file="all_vehicle_paths.json",
    num_vehicles=10000,
    num_emergency=2000,
):
    # 1. Build routes_list from all_vehicle_paths.json
    routes_list = load_routes_from_json(paths_file)

    # 2. Root element
    routes = ET.Element("routes")

    # 3. Vehicle types
    civilian_vtype = ET.SubElement(routes, "vType")
    civilian_vtype.set("id", "civilian")
    civilian_vtype.set("accel", "2.6")
    civilian_vtype.set("decel", "4.5")
    civilian_vtype.set("sigma", "0.5")
    civilian_vtype.set("length", "5")
    civilian_vtype.set("maxSpeed", "13.89")
    civilian_vtype.set("color", "0,1,0")  # Green

    emergency_vtype = ET.SubElement(routes, "vType")
    emergency_vtype.set("id", "emergency")
    emergency_vtype.set("vClass", "emergency")
    emergency_vtype.set("accel", "3.5")
    emergency_vtype.set("decel", "5.0")
    emergency_vtype.set("sigma", "0")
    emergency_vtype.set("length", "7")
    emergency_vtype.set("maxSpeed", "20")
    emergency_vtype.set("color", "1,0,0")  # Red
    emergency_vtype.set("guiShape", "emergency")

    ev_param = ET.SubElement(emergency_vtype, "param")
    ev_param.set("key", "has.bluelight.device")
    ev_param.set("value", "true")

    # 4. Depart time strategy (based on total demand and network scale)
    # Total vehicles = num_vehicles + num_emergency
    # Use 0–7200s for civilians, 0–3600s for emergency to prioritize them.
    civilian_depart_start = 0.0
    civilian_depart_end = 7200.0

    emergency_depart_start = 100.0
    emergency_depart_end = 7100.0

    all_vehicles = []

    # 5. Civilian vehicles
    for i in range(num_vehicles):
        depart_time = random.uniform(civilian_depart_start, civilian_depart_end)
        route_edges = random.choice(routes_list)
        all_vehicles.append(
            {
                "id": f"civilian_{i}",
                "type": "civilian",
                "depart": depart_time,
                "edges": route_edges,
            }
        )

    # 6. Emergency vehicles
    for i in range(num_emergency):
        depart_time = random.uniform(emergency_depart_start, emergency_depart_end)
        route_edges = random.choice(routes_list)
        all_vehicles.append(
            {
                "id": f"emergency_{i}",
                "type": "emergency",
                "depart": depart_time,
                "edges": route_edges,
            }
        )

    # 7. Sort by depart time
    all_vehicles.sort(key=lambda v: v["depart"])

    # 8. Write vehicles and routes to XML
    for v in all_vehicles:
        vehicle = ET.SubElement(routes, "vehicle")
        vehicle.set("id", v["id"])
        vehicle.set("type", v["type"])
        vehicle.set("depart", f"{v['depart']:.2f}")

        route = ET.SubElement(vehicle, "route")
        route.set("edges", " ".join(v["edges"]))

    # 9. Pretty-print XML
    xml_str = minidom.parseString(ET.tostring(routes)).toprettyxml(indent=" ")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        f.write(xml_str)

    print(f"✓ Generated {num_vehicles} civilian and {num_emergency} emergency vehicles")
    print(f"✓ Total vehicles: {len(all_vehicles)}")
    print(f"✓ Routes saved to: {output_file}")
    print(f"✓ Possible routes found in JSON: {len(routes_list)}")
    print(
        f"✓ Depart times -> civilians: [{civilian_depart_start}, {civilian_depart_end}], "
        f"emergency: [{emergency_depart_start}, {emergency_depart_end}]"
    )


if __name__ == "__main__":
    generate_routes(
        output_file="C:\\Users\\shubh\\Documents\\T40-RL-Based-Smart-Traffic-Light-System-for-Emergency-Response\\data\\networks\\intersection.rou.xml",
        network_file="C:\\Users\\shubh\\Documents\\T40-RL-Based-Smart-Traffic-Light-System-for-Emergency-Response\\data\\networks\\intersection.net.xml",
        paths_file="C:\\Users\\shubh\\Documents\\T40-RL-Based-Smart-Traffic-Light-System-for-Emergency-Response\\all_vehicle_paths.json",
        num_vehicles=10000,
        num_emergency=2000,
    )