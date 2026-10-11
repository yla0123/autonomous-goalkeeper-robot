# Goalkeeper Bringup

Status: proposed module; launch files and ROS 2 package files are not implemented.

Provide manual_sim, manual_hardware, autonomous_sim, and autonomous_hardware launch modes. Each mode must select one command source and one execution backend, load consistent configuration, and start disarmed.

Hardware modes must reject missing calibration or an unselected serial port. Changing a mode must stop and disarm before handing over control. Hardware actuation is disabled in the [example configuration](../../config/keeper.example.yaml).

See the [implementation plan](../../docs/implementation-plan.md).
