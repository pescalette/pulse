import ikpy
import json
from ikpy.chain import Chain
import numpy as np
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())# Open arm config
with open('BlockArm.json') as f:
    config = json.load(f)

# Create chain from URDF file and mask
urdf_path = 'BlockArm.urdf'
active_links_mask = config['active_links_mask']
my_chain = Chain.from_urdf_file(urdf_path, active_links_mask=active_links_mask)

# Initialize sensors and actuators lists
position_sensors = []
motors = []

# Set up the sensors
for sensor_name in config['position_sensors']:
    sensor = robot.getDevice(sensor_name)
    sensor.enable(timestep)
    position_sensors.append(sensor)

# Set up the motors
for motor_name in config['motors']:
    motor = robot.getDevice(motor_name)
    motors.append(motor)

# Get the current positions from the sensors
current_joint_positions = [sensor.getValue() for sensor in position_sensors]
waypoints = [{ 'coordinates': [0, 0, 0], }]
for target_position in waypoints:
    # Define the target position for the end-effector (x, y, z)
    new_position = target_position['coordinates']
    target_position = np.array(new_position)

    # Define an orientation for the end-effector (identity matrix assumuming no change in orientation)
    target_orientation = np.eye(3)

    # Perform inverse kinematics to compute the joint angles for the desired new position and orientation
    new_joint_positions = my_chain.inverse_kinematics(target_position=target_position, target_orientation=target_orientation)

    # Set the new joint positions on the motors
    for idx, motor in enumerate(motors):
        motor.setPosition(new_joint_positions[idx + 1])

    # Step simulation to start moving the arm
    robot.step(timestep)