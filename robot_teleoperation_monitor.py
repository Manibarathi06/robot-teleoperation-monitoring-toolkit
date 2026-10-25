
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import math
import random
import time
from datetime import datetime
from pathlib import Path


# ---------------------------------------
# PROJECT CONFIGURATION
# ---------------------------------------

WINDOW_TITLE = "Robot Teleoperation Monitoring Toolkit"

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650

ROBOT_SPEED = 3
UPDATE_INTERVAL = 100  # milliseconds

DATA_FOLDER = Path("data")
DATA_FOLDER.mkdir(exist_ok=True)


# ---------------------------------------
# ROBOT SIMULATOR
# ---------------------------------------

class RobotSimulator:

    def __init__(self):

        self.x = 400
        self.y = 300

        self.velocity = 0
        self.direction = 0

        self.sensor_distance = 100
        self.sensor_healthy = True

        self.command = "STOP"

    def move(self, command):

        self.command = command

        if command == "FORWARD":
            self.y -= ROBOT_SPEED
            self.velocity = ROBOT_SPEED

        elif command == "BACKWARD":
            self.y += ROBOT_SPEED
            self.velocity = ROBOT_SPEED

        elif command == "LEFT":
            self.x -= ROBOT_SPEED
            self.velocity = ROBOT_SPEED

        elif command == "RIGHT":
            self.x += ROBOT_SPEED
            self.velocity = ROBOT_SPEED

        elif command == "STOP":
            self.velocity = 0

        # Keep the robot inside the simulation area
        self.x = max(20, min(self.x, 780))
        self.y = max(20, min(self.y, 480))

    def update_sensor(self):

        if self.sensor_healthy:

            self.sensor_distance = random.uniform(20, 150)

        else:

            # Simulate a sensor communication failure
            self.sensor_distance = None


# ---------------------------------------
# TELEOPERATION MONITORING APPLICATION
# ---------------------------------------

class RobotMonitoringApp:

    def __init__(self, root):

        self.root = root

        self.root.title(WINDOW_TITLE)
        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.robot = RobotSimulator()

        self.recording = False
        self.csv_file = None
        self.csv_writer = None

        self.session_start = None

        self.last_sensor_time = time.time()

        self.create_interface()

        self.root.bind("<KeyPress>", self.handle_keypress)
        self.root.bind("<KeyRelease>", self.handle_keyrelease)

        self.update_application()

    # -----------------------------------
    # CREATE GUI
    # -----------------------------------

    def create_interface(self):

        title = tk.Label(
            self.root,
            text="Robot Teleoperation Monitoring Toolkit",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        main_frame = tk.Frame(self.root)

        main_frame.pack(fill="both", expand=True)

        # Robot simulation area

        self.canvas = tk.Canvas(
            main_frame,
            width=800,
            height=500,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray"
        )

        self.canvas.pack(side="left", padx=10, pady=10)

        # Monitoring panel

        panel = tk.Frame(main_frame)

        panel.pack(side="right", padx=15, fill="y")

        tk.Label(
            panel,
            text="Robot Monitoring",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.position_label = tk.Label(panel)

        self.position_label.pack(pady=5)

        self.velocity_label = tk.Label(panel)

        self.velocity_label.pack(pady=5)

        self.command_label = tk.Label(panel)

        self.command_label.pack(pady=5)

        self.sensor_label = tk.Label(panel)

        self.sensor_label.pack(pady=5)

        self.status_label = tk.Label(
            panel,
            text="Status: READY",
            font=("Arial", 12, "bold"),
            fg="green"
        )

        self.status_label.pack(pady=10)

        # Recording controls

        tk.Button(
            panel,
            text="Start Recording",
            command=self.start_recording,
            width=20
        ).pack(pady=5)

        tk.Button(
            panel,
            text="Stop Recording",
            command=self.stop_recording,
            width=20
        ).pack(pady=5)

        # Simulate sensor failure

        tk.Button(
            panel,
            text="Toggle Sensor Failure",
            command=self.toggle_sensor_failure,
            width=20
        ).pack(pady=10)

        tk.Label(
            panel,
            text="Keyboard Controls:\n\n"
                 "W = Forward\n"
                 "S = Backward\n"
                 "A = Left\n"
                 "D = Right\n"
                 "Space = Stop",
            justify="left"
        ).pack(pady=20)

    # -----------------------------------
    # KEYBOARD CONTROL
    # -----------------------------------

    def handle_keypress(self, event):

        key = event.keysym.lower()

        if key == "w":
            self.robot.move("FORWARD")

        elif key == "s":
            self.robot.move("BACKWARD")

        elif key == "a":
            self.robot.move("LEFT")

        elif key == "d":
            self.robot.move("RIGHT")

        elif key == "space":
            self.robot.move("STOP")

    def handle_keyrelease(self, event):

        key = event.keysym.lower()

        if key in ["w", "s", "a", "d"]:

            self.robot.move("STOP")

    # -----------------------------------
    # SENSOR FAILURE SIMULATION
    # -----------------------------------

    def toggle_sensor_failure(self):

        self.robot.sensor_healthy = (
            not self.robot.sensor_healthy
        )

        if self.robot.sensor_healthy:

            self.last_sensor_time = time.time()

            messagebox.showinfo(
                "Sensor Status",
                "Sensor communication restored."
            )

        else:

            messagebox.showwarning(
                "Sensor Status",
                "Sensor failure simulated."
            )

    # -----------------------------------
    # DATA RECORDING
    # -----------------------------------

    def start_recording(self):

        if self.recording:

            return

        filename = (
            DATA_FOLDER /
            f"session_{datetime.now():%Y%m%d_%H%M%S}.csv"
        )

        self.csv_file = open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        )

        self.csv_writer = csv.writer(self.csv_file)

        self.csv_writer.writerow([
            "timestamp",
            "robot_x",
            "robot_y",
            "velocity",
            "command",
            "sensor_distance",
            "sensor_status"
        ])

        self.recording = True

        self.session_start = time.time()

        self.status_label.config(
            text="Status: RECORDING",
            fg="blue"
        )

    def stop_recording(self):

        if not self.recording:

            return

        self.recording = False

        self.csv_file.close()

        self.csv_file = None
        self.csv_writer = None

        self.status_label.config(
            text="Status: READY",
            fg="green"
        )

        messagebox.showinfo(
            "Recording Complete",
            "Robot session saved in the data folder."
        )

    def save_data(self):

        if not self.recording:

            return

        timestamp = datetime.now().isoformat()

        sensor_status = (
            "HEALTHY"
            if self.robot.sensor_healthy
            else "FAILED"
        )

        sensor_distance = (
            self.robot.sensor_distance
            if self.robot.sensor_distance is not None
            else "N/A"
        )

        self.csv_writer.writerow([
            timestamp,
            self.robot.x,
            self.robot.y,
            self.robot.velocity,
            self.robot.command,
            sensor_distance,
            sensor_status
        ])

        self.csv_file.flush()

    # -----------------------------------
    # ROBOT DISPLAY
    # -----------------------------------

    def draw_robot(self):

        self.canvas.delete("all")

        # Draw the robot

        x = self.robot.x
        y = self.robot.y

        self.canvas.create_oval(
            x - 20,
            y - 20,
            x + 20,
            y + 20,
            fill="royalblue"
        )

        self.canvas.create_text(
            x,
            y,
            text="R",
            fill="white",
            font=("Arial", 14, "bold")
        )

        # Display current command

        self.canvas.create_text(
            100,
            30,
            text=f"Command: {self.robot.command}",
            font=("Arial", 14)
        )

    # -----------------------------------
    # MONITORING
    # -----------------------------------

    def update_monitoring(self):

        self.position_label.config(
            text=(
                f"Position:\n"
                f"X = {self.robot.x:.1f}\n"
                f"Y = {self.robot.y:.1f}"
            )
        )

        self.velocity_label.config(
            text=f"Velocity: {self.robot.velocity}"
        )

        self.command_label.config(
            text=f"Command: {self.robot.command}"
        )

        if self.robot.sensor_healthy:

            self.sensor_label.config(
                text=(
                    f"Sensor: HEALTHY\n"
                    f"Distance: "
                    f"{self.robot.sensor_distance:.1f}"
                ),
                fg="green"
            )

            self.status_label.config(
                text="Status: OPERATIONAL",
                fg="green"
            )

        else:

            self.sensor_label.config(
                text="Sensor: FAILED",
                fg="red"
            )

            self.status_label.config(
                text="Status: SENSOR FAILURE",
                fg="red"
            )

    # -----------------------------------
    # MAIN APPLICATION LOOP
    # -----------------------------------

    def update_application(self):

        self.robot.update_sensor()

        self.draw_robot()

        self.update_monitoring()

        self.save_data()

        self.root.after(
            UPDATE_INTERVAL,
            self.update_application
        )


# ---------------------------------------
# START APPLICATION
# ---------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = RobotMonitoringApp(root)

    root.mainloop()
