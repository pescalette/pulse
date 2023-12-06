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

sleep_1 = instruction.Sleep(1)
execution_queue.append(sleep_1)

gc_1 = instruction.GripperControl('close')
execution_queue.append(gc_1)

sleep_2 = instruction.Sleep(1)
execution_queue.append(sleep_2)

gc_2 = instruction.GripperControl('open')
execution_queue.append(gc_2)

gui = gui.RobotGUI()
gui.start_thread()

while execution_queue:
    instruction = execution_queue.popleft()
    instruction_complete = instruction.execute(controller)
    if not instruction_complete:
        execution_queue.appendleft(instruction)
    controller.step_simulation()
    time.sleep(0.001)
    execution_queue.append(instruction)
