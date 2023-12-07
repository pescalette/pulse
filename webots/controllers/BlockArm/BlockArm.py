import os
import sys
import time

# Current script directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))
# Path to the 'controllers' folder
controllers_directory = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Add 'controllers' directory to sys.path
if controllers_directory not in sys.path:
    sys.path.append(controllers_directory)

from robot_control import instruction, _controller, gui
from collections import deque

controller = _controller.RobotController('BlockArm')
execution_queue = deque()

gui = gui.RobotGUI(controller)
gui.start_thread()

move_instruction_1 = instruction.Move("move1")
waypoints_1 = [{ 'coordinates': [.4, .4, .4],  }, { 'coordinates': [.2, .2, .2],  }, { 'coordinates': [.25, .25, .25],  }, { 'coordinates': [.25, .25, .4],  }]
for waypoint in waypoints_1:
    wp_options = {'coords': waypoint['coordinates']}
    if 'speed' in waypoint:
        wp_options['speed'] = waypoint['speed']
    wp = instruction.Waypoint(**wp_options)

    move_instruction_1.add_waypoint(wp)

execution_queue.append(move_instruction_1)

gc_1 = instruction.GripperControl('close')
execution_queue.append(gc_1)

sleep_1 = instruction.Sleep(1)
execution_queue.append(sleep_1)


while controller.robot.step(controller.timestep) != -1:
    while execution_queue and controller.state == _controller.State.PLAYING:
        instruction = execution_queue.popleft()
        instruction_complete = instruction.execute(controller)
        if not instruction_complete:
            execution_queue.appendleft(instruction)
        controller.step_simulation()
    time.sleep(0.001)
    gui.window.update_idletasks()
    gui.window.update()
