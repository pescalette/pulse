import json
import ikpy
from ikpy.chain import Chain
import numpy as np
from controller import Robot
from enum import Enum

class State(Enum):
    PAUSED = 0
    PLAYING = 1


class RobotController:
    def __init__(self, robot_name):
        # Load configuration and initialize robot
        self.robot = Robot()
        self.robot_name = robot_name
        self.timestep = int(self.robot.getBasicTimeStep())
        self.state = State.PLAYING
        self.initialize_robot()
    
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
        # Get the current positions from the sensors
        return [sensor.getValue() for sensor in self.position_sensors]
    
    def get_gps_position(self):
        return self.gps.getValues()

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

class Motor:
    def __init__(self, name, device, motor_joint_max, motor_joint_min):
        self.name = name
        self.device = device
        self.joint_max = motor_joint_max
        self.joint_min = motor_joint_min
        
    def get_motor_limits(self):
        return self.joint_min, self.joint_max
