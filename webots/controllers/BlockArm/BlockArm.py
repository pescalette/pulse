import os
import sys

# Current script directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))
# Path to the 'controllers' folder
controllers_directory = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Add 'controllers' directory to sys.path
if controllers_directory not in sys.path:
    sys.path.append(controllers_directory)

from robot_control import instruction, _controller
from collections import deque

controller = _controller.RobotController('BlockArm')
execution_queue = deque()

move_instruction_1 = instruction.Move("move1")
waypoints_1 = [{ 'coordinates': [1, 0, 0],  }, { 'coordinates': [0, 1, 0],  }]
for waypoint in waypoints_1:
    wp_options = {'coords': waypoint['coordinates']}
    if 'speed' in waypoint:
        wp_options['speed'] = waypoint['speed']
    wp = instruction.Waypoint(**wp_options)

    move_instruction_1.add_waypoint(wp)

execution_queue.append(move_instruction_1)

for i in range(2):
    move_instruction_2 = instruction.Move("move2")
    waypoints_2 = [{ 'coordinates': [1, 0, 0],  }, { 'coordinates': [0, 0, 1],  }]
    for waypoint in waypoints_2:
        wp_options = {'coords': waypoint['coordinates']}
        if 'speed' in waypoint:
            wp_options['speed'] = waypoint['speed']
        wp = instruction.Waypoint(**wp_options)

        move_instruction_2.add_waypoint(wp)

    execution_queue.append(move_instruction_2)



while execution_queue:
    instruction = execution_queue.popleft()
    instruction_complete = instruction.execute(controller)
    if not instruction_complete:
        execution_queue.appendleft(instruction)
    controller.step_simulation()
    execution_queue.append(instruction)
