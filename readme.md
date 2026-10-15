# MIE1075 Project: Autonomous Goalkeeper Robot

This project models a goalkeeper for penalty-kick experiments using a regulation 7.32 m x 2.44 m goal and a generic 1.90 m-tall human-shaped keeper. The robot keeps the original two motions: sideways movement and left/right tilt.

The goal opening and 11 m penalty distance follow [IFAB Law 1](https://theifab.com/laws/latest/the-field-of-play/). Keeper height, arm span, mass, pivot, and motion limits are simulation assumptions.

![Regulation goal and adult goalkeeper scale](docs/images/goalkeeper-scale.svg)

## Current implementation

| Component | Current state |
| --- | --- |
| Planning geometry | Regulation goal; adult-sized head, torso, arms, gloves, legs, and feet |
| Local Python planner | Computes a blocking pose, checks reachability and swept clearance, and exports its movement path |
| Gazebo robot model | Generated from the same body-part dimensions; slide_joint along +Y and tilt_joint about +X |
| Gazebo scene | Regulation inside opening, white goal members, penalty mark, and initial football |
| Shooter | ROS 2 source generates targets inside the configured goal with the configured flight time |
| Simulation launch | Starts the world and spawns the keeper; planned-motion execution is not connected |
| Perception and ROS control | Proposed interfaces; ball tracking, crossing prediction, and execution adapter are not implemented |

## Local planning demo

Python 3 and its standard library are sufficient:

```text
python3 run_keeper.py demo
python3 run_keeper.py demo --path-csv action_path.csv
python3 run_keeper.py plan --y-m 1.30 --z-m 1.40 --arrival-time-s 0.55 --elapsed-s 0.10
```

On Windows with an installed Python launcher, use `py` in place of `python3`. The built-in demo needs no example-data folder. Its coordinate is the ball centre at the goal plane, not the ball's current location.

The 0.55 s flight time and 0.10 s processing/communication budget remain assumptions. After a 0.02 s settling reserve, the model allows 0.43 s for axis motion. Speed limits have not been increased to guarantee saves across the larger goal.

The output includes reachability, a slide/tilt target, action-path checkpoints, and an optional CSV. Serial output is a preview only; this program does not connect to a robot.

## Geometry and validation

`config/keeper.design.json` is the shared geometry source. After changing it:

```text
python3 tools/generate_geometry.py
python3 tests/test_regulation_geometry.py -v
```

The keeper is a rigid human-shaped body. Its 1.90 m body is mounted with 0.05 m foot clearance and a 1.00 m pivot; its upright crown is at 1.95 m. The planner uses the occupied body parts, rather than treating the whole arm-span rectangle as solid. Individual limb control and jumping are outside the model.

## Gazebo preview

The intended environment is Ubuntu 24.04, ROS 2 Jazzy, and Gazebo Harmonic. With the ROS/Gazebo dependencies installed, build from this repository root:

```text
colcon build --base-paths src
source install/setup.bash
ros2 launch goalkeeper_sim simulation.launch.py
```

This launches the scene and creates the keeper model. It does not execute a planned interception. Gazebo/ROS runtime behaviour has not been verified on this Windows development machine.

## Documents

| Document | Contents |
| --- | --- |
| [Robot design](docs/robot-design.md) | Regulation dimensions, adult keeper assumptions, timing, and action-path commands |
| [Architecture](docs/architecture.md) | Data flow, planning, and execution boundaries |
| [Interfaces](docs/interfaces.md) | Coordinate frames, proposed ROS messages, and optional controller protocol |
| [Implementation plan](docs/implementation-plan.md) | Remaining integration work and acceptance checks |
| [Reuse decisions](docs/reuse-decisions.md) | Simulation libraries and reference repositories |

The next integration milestone is to feed a known crossing coordinate into the planner, execute the resulting joint path in Gazebo, and evaluate ball contact before adding camera-based prediction.
