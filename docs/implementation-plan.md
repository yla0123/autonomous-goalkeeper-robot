# Implementation Plan

## 1. Repository layout

The repository includes a local Python planner demo. ROS 2 package metadata, nodes, robot description, and firmware remain to be implemented.

```text
autonomous-goalkeeper-robot/
|-- readme.md
|-- docs/
|   |-- robot-design.md
|   |-- architecture.md
|   |-- interfaces.md
|   |-- implementation-plan.md
|   `-- reuse-decisions.md
|-- config/
|   |-- keeper.design.json
|   `-- keeper.example.yaml
|-- examples/
|   |-- shot_001.json
|   `-- shot_001_action_path.csv
|-- run_keeper.py
|-- firmware/
|   `-- esp32_keeper/README.md
`-- src/
    |-- goalkeeper_sim/             Existing static world and package scaffold
    |-- goalkeeper_description/     Proposed two-axis model
    |-- goalkeeper_interfaces/      Proposed custom messages
    |-- goalkeeper_control/         Local planner demo; ROS 2 nodes and adapters proposed
    |-- goalkeeper_perception/      Proposed detector, tracker, and predictor
    `-- goalkeeper_bringup/         Proposed launch and mode configuration
```

## 2. Stages and acceptance checks

| Stage | Work | Acceptance check |
| --- | --- | --- |
| 1. Geometry and interface | Review the initial design values in `docs/robot-design.md`; replace them with measured prototype dimensions | Known crossing coordinates map to the expected blocking pose and clear the frame |
| 2. Local planning baseline | Use the Python dry run to inspect coverage and reachability under the example limits | Reachable and unreachable target cases are correctly reported before connecting hardware |
| 3. Single-axis motion | Select and assemble the slide and servo; implement explicit homing and manual commands | Both axes reach repeated targets; limits, stop, and homing timeout are exercised |
| 4. Two-axis manual control | Implement KeeperCommand, serial bridge, and MCU status | Position and tilt commands work together; malformed, expired, and disconnected commands stop correctly |
| 5. Matching simulation | Add two-axis URDF/SDF and Gazebo control adapter | The same high-level target drives the chosen backend; units and joint signs agree |
| 6. Perception baseline | Fix the camera, calibrate its transform, detect a colored ball, estimate velocity | Position estimates are compared with known locations and report invalid data when the ball is lost |
| 7. Autonomous interception | Connect the crossing predictor to the planner | Reachable and unreachable shots are separated; the keeper arrives before the ball in controlled trials |
| 8. Evaluation | Repeat a defined set of shots and record timing, positions, and outcomes | Report trial count, conditions, failures, positioning error, and save rate |

Hardware procurement and fabrication time are separate from software effort. Do not use commercial product performance as the prototype acceptance threshold.

## 3. Proposed implementation files

| Module | Files to implement later | Main work |
| --- | --- | --- |
| goalkeeper_description | urdf/keeper.urdf.xacro; model configuration | slide_joint along +Y; tilt_joint about +X; collision geometry and limits |
| goalkeeper_interfaces | msg/BallState.msg; msg/InterceptTarget.msg; msg/KeeperCommand.msg; msg/KeeperStatus.msg | Register message definitions and their dependencies |
| goalkeeper_control | local Python planning demo; manual_target_node.py; command_arbiter_node.py; interception_planner_node.py; serial_bridge_node.py; simulation_adapter_node.py | The demo maps crossing coordinates to a candidate pose; ROS 2 nodes and hardware adapters remain to be implemented |
| goalkeeper_perception | ball_detector_node.py; tracker_node.py; crossing_predictor_node.py | Detection, transform into goal_frame, velocity estimation, and crossing prediction |
| goalkeeper_bringup | manual_sim.launch.py; manual_hardware.launch.py; autonomous_sim.launch.py; autonomous_hardware.launch.py | Load consistent configuration and exactly one execution backend |
| firmware/esp32_keeper | ESP32 application and dependency manifest | Serial parser, states, slide motion, servo output, limits, and status |
| goalkeeper_sim | Spawn configuration, ball and camera models, world resource installation | Extend the current static scene; install resources for package-based launch |

The local planner demo is available through `python3 run_keeper.py demo` (or `py run_keeper.py demo` on Windows with Python installed). The planned ROS 2 and firmware files are not available to run in the current branch.

## 4. Integration choices

- Use a fixed camera for the first prototype to simplify coordinate calibration.
- Begin with colored-ball detection and a linear low-shot baseline. Add a learned detector or gravity-aware trajectory model only when the experiment requires it.
- Use USB serial for initial MCU communication. If ROS 2 runs under WSL2, validate USB passthrough and reconnect behavior before integration. [Microsoft USB guidance](https://learn.microsoft.com/en-us/windows/wsl/connect-usb)
- Keep pulse generation on the MCU. Use ROS 2 for target generation and system coordination.
- Use identical units, joint names, target validity rules, and panel geometry in simulation and hardware.
- Add full ros2_control hardware integration after the simple bridge is validated, if it provides a clear project benefit.

## 5. Essential measurements

| Measurement | Purpose |
| --- | --- |
| Slide displacement against commanded steps | Establish millimeters per step and detect lost motion |
| Panel angle against PWM command | Calibrate neutral angle, scale, sign, and loaded response |
| Loaded motion and settling time | Set achievable target deadlines |
| Host-send to MCU-receive delay | Determine a transport margin for expiring commands |
| Observation timestamp to command acceptance | Identify vision and scheduling latency |
| Time to reach the selected blocking pose | Check whether prediction is early enough |
| Saves divided by attempted valid shots | Evaluate the complete system under stated conditions |

Keep command acceptance, arrival, ball detection, and a successful save as separate outcomes. Simulated joint feedback and step-based hardware estimates must be labeled separately.
