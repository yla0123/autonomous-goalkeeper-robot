# ESP32 Keeper Firmware

Status: design placeholder. This directory does not contain flashable firmware.

Implement one Arduino-compatible ESP32 application that receives absolute slide and tilt targets over USB serial. Use FastAccelStepper for STEP/DIR pulse generation and ESP32Servo for panel tilt output.

Required components:

- A bounded, non-blocking line parser for the [serial protocol](../../docs/interfaces.md).
- Explicit DISARMED, HOMING, READY, MOVING, and FAULT states.
- Slide homing with a travel limit, timeout, and switch backoff.
- Mechanical travel and tilt checks before accepting motion.
- Expiry and valid-command watchdog handling.
- Status with estimated slide position and commanded tilt angle.
- A latched hardware-stop input and explicit recovery.

Select pins after choosing the board and driver. Validate voltage levels, shared timer/PWM resources, direction reversal, and both axes operating together. Keep pulse generation running while serial data is parsed. Firmware must reject hardware motion until required calibration is complete.

See the [architecture](../../docs/architecture.md) and [example configuration](../../config/keeper.example.yaml).
