import tkinter as tk
from threading import Thread
import math


class RobotGUI:
    def __init__(self, controller):
        self.window = None
        self.gui_thread = None
        self.controller = controller

    def start(self):
        # Create a new window
        self.window = tk.Tk()
        self.window.title("Robot Controller")

        motor_button_frame = tk.Frame(self.window)
        motor_button_frame.pack(side="left")

        for motor in self.controller.motors:
            label = tk.Label(motor_button_frame, text=motor.name)
            label.pack()

            button_positive = tk.Button(motor_button_frame, text="+")
            button_positive.bind("<ButtonPress>", lambda event, motor=motor: self.controller.move_motor(motor, "positive"))
            button_positive.pack()

            button_negative = tk.Button(motor_button_frame, text="-")
            button_negative.bind("<ButtonPress>", lambda event, motor=motor: self.controller.move_motor(motor, "negative"))
            button_negative.pack()

        # For stats display
        stats_frame = tk.Frame(self.window)
        stats_frame.pack(side="right")

        self.position_display = tk.Label(stats_frame, text="Position XYZ: ")
        self.position_display.pack()

        self.joint_positions_display = tk.Label(stats_frame, text="Joint Positions: ")
        self.joint_positions_display.pack()

        self.runtime_display = tk.Label(stats_frame, text="Runtime: ")
        self.runtime_display.pack()

        # Waypoint button below all stats data
        self.create_waypoint_button = tk.Button(stats_frame, text="Create Waypoint", command=self.create_waypoint)
        self.create_waypoint_button.pack()

        # Keep the window on top of others
        self.window.attributes('-topmost', True)

        # Update the stats for the first time and schedule subsequent updates
        self.update_stats()

        # Start GUI updating loop
        self.update_gui() 

        # Start the GUI event loop
        self.window.mainloop()

    def start_thread(self):
        self.gui_thread = Thread(target=self.start)
        self.gui_thread.start()

    def update_stats(self):
        # Update stats in the GUI, retrieve data from the controller
        self.position_display.config(text=f"Position XYZ: ({', '.join(map(str, self.controller.get_gps_position()))})")
        joint_positions = self.controller.get_current_position()
        self.joint_positions_display.config(text=f"Joint Positions: ({', '.join(f'{pos:.2f}' for pos in joint_positions)})")
    
    def create_waypoint(self):
        # Serialize current position to json and update the related field
        serialized_waypoint = self.controller.serialize_position()
        # send waypoint to server

    def update_gui(self):
        self.update_stats()
      
        self.window.update_idletasks()
        self.window.update()
      
        # Schedule the next update
        self.window.after(100, self.update_gui)

