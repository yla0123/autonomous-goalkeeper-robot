# Initial Robot Design

Status: a concrete small-prototype design baseline for simulation and planning. Dimensions and axis capabilities are assumptions for an initial build; they are not measured hardware performance or a parts list.

## 1. What the robot does

The first software input is the ball-center coordinate where the ball is predicted to cross the goal plane, plus the predicted time from the kick to that crossing. The planner chooses a carriage position and panel angle that cover that point and fit the remaining motion time.

This coordinate is not necessarily the ball's current observed position. A current field coordinate `(x, y, z)` needs a velocity estimate and a crossing-time prediction before it can be used by this planner. The first planner accepts `(0, y, z)` in `goal_frame`, where `x = 0` is the goal plane.

The planner output is an actuator target `(slide_m, tilt_rad)`. It is a position command for the robot, not another ball coordinate. An unreachable shot produces no movement command.

## 2. Mechanical baseline

| Item | Initial value | Design intent |
| --- | ---: | --- |
| Goal opening | 1.50 m wide x 1.00 m high | Small indoor prototype, not a regulation-size goal |
| Slide travel | -0.50 m to +0.50 m | One-meter usable lateral rail travel, centered at zero |
| Carriage plus moving assembly | 1.50 kg | Approximate mass used for early force estimates |
| Keeper panel | 0.30 m wide x 0.65 m long x 0.015 m thick | Lightweight blocking surface |
| Panel mass | 0.35 kg | Placeholder pending panel material and weighing |
| Tilt pivot height | 0.15 m above floor | Pivot at the lower edge of the upright panel |
| Tilt range | -45 deg to +45 deg | Left/right tipping in the goal plane |
| Ball radius | 0.11 m | Approximate full-size soccer-ball geometry for the planner |
| Minimum projected ball-panel overlap | 0.05 m | Require a 50 mm intersection in the planner's 2D footprint model |

The carriage rides on a fixed horizontal rail. A stepper motor drives the carriage through a belt or lead screw. A separate servo tilts the panel around a supported shaft parallel to the shot direction. The shaft and bearings carry panel loads; the servo provides rotation torque. Use a soft, lightweight panel for early low-speed trials and provide end switches and a physical drive stop.

## 3. Coordinate and command data

Use meters, radians, and seconds in the planner. Positive `y` follows the existing `goal_frame` convention. Positive panel angle follows the right-hand rotation about +X already described in the [interface specification](interfaces.md).

Example predicted shot input:

```json
{
  "frame_id": "goal_frame",
  "flight_time_from_kick_s": 0.55,
  "elapsed_since_kick_s": 0.10,
  "crossing_point_m": {"x": 0.0, "y": 0.55, "z": 0.65},
  "robot_state": {
    "slide_m": 0.0,
    "tilt_rad": 0.0,
    "slide_velocity_mps": 0.0,
    "tilt_velocity_radps": 0.0
  }
}
```

The crossing coordinate is the ball center at the goal plane. The planner expands the panel's blocking footprint by the ball radius, requires at least 50 mm of projected overlap, then searches candidate slide and tilt targets. It also checks axis travel and whether the panel's swept path clears the goal frame.

## 4. Timing requirement

The initial timing case uses the assumptions supplied for this project:

| Timing item | Value | Status |
| --- | ---: | --- |
| Ball flight from kick to goal plane | 0.55 s | Example shot assumption |
| Detection, prediction, and communication | 0.10 s | Budget assumption to measure later |
| Time remaining after processing | 0.45 s | 0.55 s - 0.10 s |
| Arrival and settling reserve | 0.02 s | Initial design margin; verify experimentally |
| Maximum planned axis motion window | 0.43 s | 0.45 s - 0.02 s |

The axes move at the same time. The initial software limits are 2.0 m/s and 12 m/s^2 for the slide, and 4.0 rad/s and 20 rad/s^2 for tilt. Under a rest-to-rest trapezoidal model, moving the slide the full 0.50 m from center requires about 0.417 s at its limits. A 45-degree tilt requires about 0.396 s at its limits. These are calculated lower bounds from assumed limits, not demonstrated movement times. A target can still be unreachable because of panel-frame collision, initial movement, load, tracking error, or an incorrect speed assumption.

The planner starts both axes as soon as the coordinate is available, uses the fastest profile allowed by its configured speed and acceleration, and holds the blocking pose until the predicted ball arrival. For the included sample crossing point `(0, 0.55, 0.65) m`, the design model selects approximately `slide = +0.18 m`, `tilt = -17 deg`. It reaches this pose about 0.245 s after movement starts, at about 0.345 s after the kick, then holds until the ball reaches the goal plane at 0.55 s. This is a modeled path, not measured robot performance.

The [sample action path](../examples/shot_001_action_path.csv) lists the pose at selected times. The CLI also includes action-path checkpoints in its JSON output. The path assumes both axes start at rest and follows an ideal acceleration-limited profile.

For the assumed 1.50 kg moving assembly, 12 m/s^2 slide acceleration corresponds to 18 N of ideal inertial force before friction and drivetrain losses. This value helps size a later prototype; it does not select a motor. Measure loaded slide and tilt motion before relying on the 0.43-second motion window.

## 5. Software mapping

The local planner is a hardware-disabled Python dry run:

1. Read a predicted goal-plane crossing coordinate and the robot's current estimated pose.
2. Reject invalid coordinates and shots outside the opening.
3. Search slide and tilt combinations for panel coverage and swept frame clearance.
4. Estimate each axis's rest-to-rest movement time and compare the slower axis with the motion deadline.
5. Return an absolute slide position and tilt angle only when the candidate is reachable.
6. Show a protocol-v2 serial line preview for inspection; it is never transmitted.

Run the included example from this repository root:

```text
python3 run_keeper.py demo
```

Plan a different predicted crossing point directly:

```text
python3 run_keeper.py plan --y-m 0.55 --z-m 0.65 --arrival-time-s 0.55 --elapsed-s 0.10
```

Or copy and edit [the example shot](../examples/shot_001.json), then pass it with `--input path/to/shot.json`.

## 6. What remains unselected

The design deliberately does not name a stepper, servo, driver, rail, power supply, or ESP32 board revision. Select them after measuring actual moving mass, panel balance, rail friction, loaded tilt torque, current draw, and full-stroke response. Add position sensors if absolute feedback is required: step counts estimate carriage position, and a hobby servo's PWM command does not measure panel angle.

The Python planner does not detect a ball, infer its velocity, create a ROS 2 message, or actuate the hardware. Those are later integration stages in the [implementation plan](implementation-plan.md). The commercial RobotKeeper's advertised performance is outside this prototype's stated design target.
