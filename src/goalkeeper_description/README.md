# Goalkeeper Description

Status: proposed module; ROS 2 package files and model are not implemented.

Create a two-axis keeper model with slide_joint translating along +Y and tilt_joint rotating about +X. Define the rail, carriage, supported pivot, panel geometry, collisions, inertial properties, and calibrated limits.

Keep physical dimensions separate from the full-size field in the existing world. Reuse the same panel footprint in the planner and simulation.

See the [architecture](../../docs/architecture.md) and [coordinate conventions](../../docs/interfaces.md).
