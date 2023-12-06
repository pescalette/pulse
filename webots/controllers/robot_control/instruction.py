import numpy as np
import time

class Instruction:
    def __init__(self, name):
        self.name = "Unnamed Instruction"
        self.children = []
    
    # All Instruction subclasses must implement this method
    def execute(self, robot_controller):
        raise NotImplementedError


class Move(Instruction):
    def __init__(self, name=""):
        super().__init__(name)
        self.waypoints = []
        self.current_waypoint_index = 0   # Track the current waypoint index
        self.robot_startup_delay = 0

    def add_waypoint(self, waypoint):
        self.waypoints.append(waypoint)

    def has_reached_waypoint(self, waypoint, current_gps_position):
        distance_threshold = 0.01
        return np.linalg.norm(np.array(waypoint.coords) - np.array(current_gps_position)) < distance_threshold
    
    def is_robot_moving(self, previous_joint_positions, current_joint_positions):
        joint_movement_threshold = 0.001 
        differences = [abs(c - p) for p, c in zip(previous_joint_positions, current_joint_positions)]
        return any(diff > joint_movement_threshold for diff in differences)

    def execute(self, controller):
        if self.current_waypoint_index >= len(self.waypoints):
            return True
        
        waypoint = self.waypoints[self.current_waypoint_index]
        current_gps_position = controller.get_gps_position()

        if self.has_reached_waypoint(waypoint, current_gps_position):
            self.current_waypoint_index += 1  # Move on to next waypoint
            return False  # Return False since the waypoint reached is not necessarily the last waypoint
        
        current_joint_positions = controller.get_current_position()
        # If the robot hasn't yet moved towards the current waypoint, calculate and set target positions
        if not hasattr(self, 'target_joint_positions'):
            self.robot_startup_delay = 5
            target_position = np.array(waypoint.coords)
            self.target_joint_positions = controller.chain.inverse_kinematics(target_position)[:len(controller.motors) + 1]
            # When the IK solution is not feasible (the position is out of range), it might return an empty list or None,
            # handle this case by treating the waypoint as reached and moving on to the next waypoint
            if self.target_joint_positions is None or np.isnan(self.target_joint_positions).any():
                self.current_waypoint_index += 1
                return False
            
            for idx, motor in enumerate(controller.motors):
                motor.device.setPosition(self.target_joint_positions[idx + 1])
        else:
            if self.robot_startup_delay > 0:
                # If the delay is set, decrement it and do not check movement yet
                self.robot_startup_delay -= 1
            else:
                # Check if the robot is still moving towards the previous target
                if not self.is_robot_moving(self.previous_joint_positions, current_joint_positions):
                    # If the robot is not moving, we consider the waypoint unreachable and move on
                    self.current_waypoint_index += 1
                    del self.target_joint_positions
                    return False
            
        # Save the current joint positions for the next execution run
        self.previous_joint_positions = current_joint_positions
        return False 


class Waypoint():
    def __init__(self, coords, speed=None, name=""):
        self.name = name
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.coords = coords
        self.speed = speed

# This runs asynchronously which mimics the interaction of robotiq grippers on a universal robot
class GripperControl(Instruction):
    def __init__(self, action, name=""):
        super().__init__(name)
        self.action = action
    
    def execute(self, controller):
        for motor in controller.gripper_motors:
            position = motor.joint_max if self.action == "close" else motor.joint_min
            motor.device.setPosition(position)
        return True
    
class Sleep(Instruction):
    def __init__(self, time_to_sleep, name=""):
        super().__init__(name)
        self.time_to_sleep = time_to_sleep
        self.start_time = None

    def execute(self, controller):
        current_time = time.monotonic()
        if self.start_time is None:
            self.start_time = current_time
        
        if current_time - self.start_time >= self.time_to_sleep:
            # Sleep duration has passed
            return True 
        return False
    