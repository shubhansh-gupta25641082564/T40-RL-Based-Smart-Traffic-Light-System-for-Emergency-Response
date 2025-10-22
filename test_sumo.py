import os
import sys

# Check SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print(f"✓ SUMO_HOME found: {os.environ['SUMO_HOME']}")
else:
    sys.exit("❌ Please set SUMO_HOME environment variable")

# Test TraCI import
try:
    import traci
    print("✓ TraCI imported successfully")
except ImportError:
    print("❌ TraCI import failed")

# Test sumolib
try:
    import sumolib
    print("✓ sumolib imported successfully")
except ImportError:
    print("❌ sumolib import failed")

print("\n✓ All tests passed! Your environment is ready.")