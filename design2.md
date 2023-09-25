# Pulse Preliminary Design

## Blockly Code Execution Explanation

In this pseudo-code, we have a RobotArm class that represents the robot arm. It provides methods to perform the actions described in the Move, Waypoint, Speed Control, Acceleration Control, and Gripper Control blocks. The example usage demonstrates how these methods can be called to execute the desired actions.

```Python
class RobotArm:
    def __init__(self):
        self.position = (0, 0, 0)
        self.gripper_width = 0
        self.speed = 1.0
        self.acceleration = 0.5
        self.safety_enabled = True

    def move_to(self, waypoint, movement_type):
        # Execute motion planning to reach the waypoint
        if self.safety_enabled:
            if self.check_collision(waypoint):
                print("Collision detected. Halting motion.")
                return

        # Move the robot arm to the specified waypoint
        if movement_type == "linear":
            print(f"Moving linearly to {waypoint}")
            self.position = waypoint
        else:
            print(f"Moving in a circular path to {waypoint}")
            # Execute circular motion logic

        # Monitor and adjust the position in real-time (not shown here)

    def adjust_speed(self, speed):
        # Adjust the robot arm's movement speed
        self.speed = speed
        print(f"Speed adjusted to {speed}")

    def adjust_acceleration(self, acceleration):
        # Adjust the robot arm's acceleration
        self.acceleration = acceleration
        print(f"Acceleration adjusted to {acceleration}")

    def control_gripper(self, action, gripper_width=None):
        # Control the gripper based on user-defined settings
        if action == "open":
            self.gripper_width = 1.0  # Fully open
        elif action == "close":
            self.gripper_width = 0.0  # Fully closed
        elif action == "adjust":
            self.gripper_width = gripper_width  # Adjust to a specific width
        else:
            print("Invalid gripper action.")

    def check_collision(self, waypoint):
        # Check for collisions with obstacles in the environment (not shown here)
        return False


# Example usage:
robot = RobotArm()

waypoints = [(1, 0, 0), (2, 0, 0), (3, 0, 0)]
movement_type = "linear"
speed = 0.8
acceleration = 0.3
gripper_action = "open"

for waypoint in waypoints:
    robot.move_to(waypoint, movement_type)
    robot.adjust_speed(speed)
    robot.adjust_acceleration(acceleration)

# Control the gripper
robot.control_gripper(gripper_action)

# End the program
```

## Recursive Blockly Use Case

Recursion can be used to accomplish repetitive tasks with a simple building block structure. For example, a "Pick and Place" function that picks an object from one waypoint, moves to another, and places it there. Then, you can use recursion to repeat this action a specified number of times or until a certain condition is met. This way, you can build complex programs by stacking these basic building blocks.

The previous example can be better handled with a loop but there are some things better left with recursion. An example of something where recursion would shine is in the path finding functions in motion planning. The robots environment could be represented as a grid with obstacles and then fed through a recursive function to determine a safe path to then calculate further specificities such as joint angles and speeds.

## Data Interaction

The robot's control library is parsed to python to execute actions. Waypoints, speed, acceleration, and gripper settings are passed as arguments to functions, enabling dynamic control and easy and accessible interfacing to most simulators or hardware environments.

## Testing on a Simulator

Before deploying the Python code on a real robot, it's essential to test it in a simulator environment. The simulator software (e.g., Gazebo, Webots) will replicate the robot's behavior based on the Python code, allowing for thorough testing and debugging.

By translating the Blockly designs into Python code, we provide a practical way to control the robot's movements and actions while maintaining flexibility and control over the robot's behavior.
