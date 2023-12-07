import json
import ikpy
from ikpy.chain import Chain
import numpy as np
from transforms3d import _gohlketransforms as transformations
from transforms3d.euler import mat2euler
from controller import Robot
from enum import Enum
import time
import server

class State(Enum):
    PAUSED = 0
    PLAYING = 1
    PROGRAM = 2
    STOPPED = 3


class RobotController:
    def __init__(self, robot_name):
        # Load configuration and initialize robot
        self.robot = Robot()
        self.robot_name = robot_name
        self.timestep = int(self.robot.getBasicTimeStep())
        self.state = State.PLAYING
        self.initialize_robot()
        server.run_in_thread()
    
    # Set up sensors and actuators based on the configuration
    def initialize_robot(self):
        # Create chain from URDF file and mask
        with open(f"{self.robot_name}.json") as f:
            config = json.load(f)
        urdf_path = f"{self.robot_name}.urdf"
        active_links_mask = config['active_links_mask']
        self.chain = Chain.from_urdf_file(urdf_path, active_links_mask=active_links_mask)

        self.gps = self.robot.getDevice('gps')
        self.gps.enable(self.timestep)

        self.imu = self.robot.getDevice('imu')
        self.imu.enable(self.timestep)

        # Initialize sensors and actuators lists
        self.position_sensors = []
        self.motors = []
        self.gripper_motors = []
        
        # Set up the sensors
        for sensor_name in config['position_sensors']:
            sensor = self.robot.getDevice(sensor_name)
            sensor.enable(self.timestep)
            self.position_sensors.append(sensor)

        # Set up the motors
        for motor_info in config['motors']:
            motor = Motor(
                name=motor_info["name"], 
                device=self.robot.getDevice(motor_info["name"]), 
                motor_joint_max=motor_info.get("motor_joint_max"),  
                motor_joint_min=motor_info.get("motor_joint_min")   
            )
            self.motors.append(motor)

        # Set up the gripper motors
        for motor_info in config['gripper_motors']:
            motor = Motor(
                name=motor_info["name"], 
                device=self.robot.getDevice(motor_info["name"]), 
                motor_joint_max=motor_info.get("motor_joint_max"),  
                motor_joint_min=motor_info.get("motor_joint_min")   
            )
            self.gripper_motors.append(motor)

    def get_current_position(self):
        # Get the current joint positions from the sensors
        return [sensor.getValue() for sensor in self.position_sensors]
    
    def get_gps_position(self):
        if self.gps is None:
            print("GPS device not initialized")
            return None
        
        # Run one simulation step to ensure sensors are updated
        self.robot.step(self.timestep)
        
        return self.gps.getValues()

    def get_orientation_quaternion(self):
        if self.imu is None:
            print("Inertial Unit not initialized")
            return None
        self.robot.step(self.timestep)
        return self.imu.getQuaternion()
    
    def get_orientation_matrix(self):
        orientation = self.get_orientation_quaternion()
        if orientation is not None:
            # Get a 4x4 transformation matrix from quaternion
            rotation_matrix_4x4 = transformations.quaternion_matrix(orientation)
            # Extract the upper-left 3x3 rotation matrix
            rotation_matrix_3x3 = rotation_matrix_4x4[:3, :3]
            return rotation_matrix_3x3
        return None

    def play(self):
        self.state = State.PLAYING

    def pause(self):
        self.state = State.PAUSED
        
    def step_simulation(self):
        # Check the state and act accordingly
        if self.state == State.PLAYING:
            # Simulation steps forward only if not paused
            return self.robot.step(self.timestep)
        elif self.state == State.PAUSED:
            pass
        elif self.state == State.PROGRAM:
            pass
        elif self.state == State.STOPPED:
            pass

    def move_motor(self, motor, direction, angle_increment=0.1):
        direction_multiplier = 1 if direction == 'positive' else -1

        # Retrieve the current position of the motor
        current_position = motor.device.getTargetPosition()
        # Calculate the new target position
        new_position = current_position + (angle_increment * direction_multiplier)

        # Command the motor to move to the new position
        motor.device.setPosition(new_position)

    def serialize_position(self):
        motor_positions = {}
        for motor in self.motors:
            motor_positions[motor.name] = motor.device.getTargetPosition()

        return json.dumps(motor_positions)
    
    def send_serialized_waypoint(self, message):
        server.send_message(message)




class Motor:
    def __init__(self, name, device, motor_joint_max, motor_joint_min):
        self.name = name
        self.device = device
        self.joint_max = motor_joint_max
        self.joint_min = motor_joint_min
        
    def get_motor_limits(self):
        return self.joint_min, self.joint_max
