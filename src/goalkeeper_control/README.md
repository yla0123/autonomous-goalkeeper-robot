# Goalkeeper Control

Status: a local, hardware-disabled Python planning demo exists. ROS 2 executable nodes and package metadata are not implemented.

Implement the manual target node, command arbiter, interception planner, USB serial bridge, and simulation adapter described in the [implementation plan](../../docs/implementation-plan.md).

Run `python3 run_keeper.py demo` from the repository root to convert the sample ball crossing point and arrival time into a candidate slide position and tilt angle. The planner checks travel limits, timing, panel coverage, and conservative swept clearance. Its serial output is a preview only. No serial device is opened, and no physical motor is controlled.

The ROS 2 arbiter, simulation adapter, serial bridge, and MCU firmware remain planned work.

See the [architecture](../../docs/architecture.md) and [interface specification](../../docs/interfaces.md).
