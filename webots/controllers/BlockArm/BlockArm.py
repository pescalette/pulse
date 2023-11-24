import ikpy
import json
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy.utils import geometry
from controller import Robot

# Initialize the robot
robot = Robot()

# Load your URDF file
urdf_path = 'BlockArm.urdf'
mask = [False, True, True, False, True, False, True, False, True, False, False, True]
my_chain = Chain.from_urdf_file(urdf_path, active_links_mask=mask)

# Load the arm configuration from the JSON file
f = open('BlockArm.json')
config = json.load(f)
f.close()

position_sensors = []
for sensor_name in config['position_sensors']:
    sensor = robot.getDevice(sensor_name)
    sensor.enable(16)
    position_sensors.append(sensor)

current_joint_positions = [sensor.getValue() for sensor in position_sensors]

# Define the desired new position in XYZ coordinates
new_position = [1, 1, 1]  # Replace with the desired XYZ coordinates

# Perform inverse kinematics to compute the joint angles for the desired new position
new_joint_positions = my_chain.inverse_kinematics(new_position, initial_positions=current_joint_positions)

# Set the new joint positions
for i, new_joint_angle in enumerate(new_joint_positions):
    position_sensors[i].setPosition(new_joint_angle)

# Wait for the robot to reach the new joint positions (optional)
robot.step()

# Here, the robot arm is in the desired new position