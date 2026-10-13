# Reuse Decisions

Repository inspection date: October 10, 2026. These decisions are based on source inspection and author documentation, not a local hardware demonstration.

## 1. Selected building blocks

| Component | Choice | Reason | Work still required |
| --- | --- | --- | --- |
| Slide pulse generation | [FastAccelStepper](https://github.com/gin66/FastAccelStepper) | ESP32 support, position targets, speed and acceleration settings; MIT license | Driver selection, calibration, homing, limit handling, and retargeting validation |
| Panel servo output | [ESP32Servo](https://github.com/madhephaestus/ESP32Servo) | Arduino-compatible servo control; README states LGPL-2.1-or-later | Neutral and pulse calibration, angle limits, loaded motion validation, and shared peripheral checks |
| Gazebo integration | [gz_ros2_control](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html) | Official ROS 2 Jazzy and Gazebo Harmonic integration | Two-axis model, controller configuration, and realistic motion limits |
| Simulated joint motion | [joint_trajectory_controller](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/userdoc.html) | Standard joint trajectory interface | Configure joint and state interfaces, adapters, and target timing |

Pin tested library and board-core versions. Existing library examples show individual capabilities; they do not prove the combined keeper firmware is compatible or fast enough.

## 2. Reference goalkeeper projects

| Repository | Useful part | Verified limitation |
| --- | --- | --- |
| [chayanforyou/Robokeeper-Firmware](https://github.com/chayanforyou/Robokeeper-Firmware) | Compact ESP32 receiver and servo mechanism | Current firmware maps inputs to only 0, 90, or 180 degrees; no slide control; Android APK is supplied without App source in the repository |
| [ketaro-m/foosball_robot](https://github.com/ketaro-m/foosball_robot) | Linear and rotary stepper conversion, homing, and multi-axis wiring | ROS 1 Melodic and L6470-specific; table-rod rotation differs from keeper tilt; an array access can exceed the six-axis array bounds |
| [CSE-ICE-22/GoalKeeper](https://github.com/CSE-ICE-22/GoalKeeper) | ROS 2 camera bring-up and red-ball 3D detection | Public tree lacks the described EKF, servo-driver node, and MCU firmware |
| [nanmu42/robo-playground](https://github.com/nanmu42/robo-playground) | Feedback-aware keeper control and recentering | Bound to a DJI RoboMaster EP wheeled platform; different mechanics |
| [Gautham-S0117/Orien-Robotic-Goalkeeper](https://github.com/Gautham-S0117/Orien-Robotic-Goalkeeper) | HSV vision and goal-line prediction reference | Arduino controller file is empty; Python sends left/right/stop rather than absolute positions |
| [oguzhan-gun/robokeeper-stereo-vision](https://github.com/oguzhan-gun/robokeeper-stereo-vision) | Demonstration of stereo prediction concepts | Repository explicitly omits implementation source code |

The recommended implementation combines the selected motor libraries with this project's interfaces. It does not copy an entire reference goalkeeper repository. Before copying third-party implementation, check the applicable license: the compact ESP32 and foosball repositories did not include a clear top-level license during inspection. The CSE detector package declares Apache-2.0 locally; that declaration should not be assumed to cover every repository component.

## 3. Commercial reference

The [RobotKeeper product page](https://www.robokeeper.cn/cn/products/football/) describes vision, interception prediction, and rotating or sliding blocking mechanisms. It does not establish that each standard product combines both independent axes. Its industrial actuator scale and advertised performance are design context, not measurements for this prototype.

## 4. Project-specific work

The team must implement the carriage-plus-tilt geometry, target-to-pose planner, ROS 2 interfaces, serial session behavior, homing and stop logic, calibration, and experimental evaluation. These are the project's integration tasks and must be reported separately from the capabilities of reused libraries.
