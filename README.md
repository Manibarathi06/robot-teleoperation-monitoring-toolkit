# Robot Teleoperation Monitoring Toolkit

A desktop robot teleoperation simulator and monitoring tool built with Python's standard-library Tkinter GUI. It visualizes a simulated robot, reports its position and sensor state, and can record monitoring data to CSV. It does not connect to or control physical robot hardware.

## Requirements

- Python 3
- Tkinter (usually included with Python; some Linux distributions package it separately)

No third-party Python packages are required.

## Run

From the project directory:

```bash
python robot_teleoperation_monitor.py
```

## Controls

- `W`: move forward
- `S`: move backward
- `A`: move left
- `D`: move right
- `Space`: stop

Releasing a movement key also stops the simulated robot. Use the buttons in the monitoring panel to start or stop CSV recording and to simulate a sensor failure.

## Session recordings

Recordings are written to `data/` as timestamped CSV files. Each row contains a timestamp, robot position, velocity, command, sensor distance, and sensor status. The `data/` directory is created automatically when the application runs.

## Project file

- `robot_teleoperation_monitor.py`: application entry point and simulator implementation.
