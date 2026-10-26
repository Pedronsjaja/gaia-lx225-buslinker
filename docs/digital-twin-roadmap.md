# LX-225 → ROS 2 → virtual joint: research roadmap

Status: **Planned integration**, documented 2026-10-26. The existing Python bench remains unchanged.

## Existing evidence

servo_testbench.py implements packet framing/checksums, replies, position/voltage/temperature queries and bounded command checks. ServoState carries position_time_s sampled with time.monotonic after the position reply. Voltage and temperature follow sequentially. velocity_dps is estimated; torque/current are not measured.
bench_tools.py records raw CSV and graphs. Tests use simulated serial responses. These capabilities do not imply a ROS 2 hardware interface or validated Digital Twin.

## Incremental route

1. Define joint name, servo ID, zero, sign, transmission and physical limits; values remain UNKNOWN until identified.
2. Build a virtual-only ROS 2/Gazebo joint and specify observed state independently of commands.
3. Add a read-only Python ROS adapter with a single serial owner, radians, explicit validity and source timestamps.
4. Measure acquisition interval and application transport on a controlled setup; separate host monotonic time, ROS time and simulator time.
5. Compare physical feedback to a virtual mirror (digital shadow). Record alignment and divergence; copying samples does not validate dynamics.
6. Evaluate ros2_control integration only after requirements are known: compiled ActuatorInterface/SystemInterface or reviewed process bridge, lifecycle/error handling and bounded IO.
7. Add supervised physical commands only after assembly-specific safety acceptance. Bidirectional operation must be validated before a Digital Twin claim.
8. Consider Isaac Sim/OpenUSD only for a specific experiment that benefits from them.

## Mapping and measurement

For direct coupling: joint_rad = sign × (servo_deg − zero_deg) × pi/180. For a transmission, document the ratio and apply it consistently.
Log run/sequence IDs, source and sink time, clock domain, quality, command IDs and separate observed state. Preserve raw data and identify REAL/SIMULATED/ESTIMATED channels.
Error and RMSE use time-aligned valid physical/virtual samples in radians. Rate, latency and jitter need named measurement boundaries. Cross-host one-way latency needs synchronized clocks and uncertainty; otherwise report RTT.
Application sequence gaps are not automatically network packet loss.

## Gates and limits

No physical test was performed for this roadmap. Confirm exact servo/board, supply, wiring, fixture, load, temperature/voltage limits, operator and independent stopping means before motion.
Internal servo limits are not mechanical collision limits. Stop packets are not certified emergency stops.
Hardware feedback is not external metrological ground truth. Expected performance: NOT_MEASURED.

## Sources and study

- [ros2_control component guide](https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/writing_new_hardware_component.html)
- [ROS 2 Jazzy QoS source](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Concepts/Intermediate/About-Quality-of-Service-Settings.rst)
- [Gazebo/ROS pairing](https://gazebosim.org/docs/harmonic/ros_installation/)
- [Existing driver interface](gaia_lx225.md) and [datasheets](datasheets/README.md)
- [Mechanical identification contract](https://github.com/Pedronsjaja/gaia-humanoid-structure/blob/main/docs/modelo-gaia.md)

Study clocks, serial blocking IO, unit conversion and controller lifecycle. First technical task: one observed virtual joint with a reproducible command test.
