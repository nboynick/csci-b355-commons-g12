# Drivetrain Drift

| **Velocity** [%] | **Initial Angle** [deg] | **Final Angle** [deg] | **min/max Angle Difference** [deg] | **Final Angle Difference** [deg] |
| - | - | - | - | - |
| 15 | 20 | 20.29 | 18.79/20.62 | 0.29 |
| 15 | 20 | 25.73 | 19.28/26.84 | 5.73 |
| 15 | 19.99 | 23.34 | 18.49/23.17 | 3.35 |
| 30 | 19.99 | 14.76 | 14.26/20.19 | -5.23 |
| 30 | 20 | 15.48 | 15.12/20.86 | -4.52 |
| 30 | 20 | 24.24 | 19.34/24.29 | 4.24 |
| 50 | 20 | 11.57 | 8.14/20 | -8.43 |
| 50 | 19.99 | 8.11 | 8.11/19.99 | 11.9 |
| 50 | 20 | 30.3 | 19.7/30.52 | 10.3 |
| 70 | 20 | 24.03 | 17.59/24.7 | 4.03 |
| 70 | 20 | 30.68 | 19.18/33.54 | 10.68 |
| 70 | 19.99 | 32.51 | 15.7/32.2 | 12.52 |

**Preliminary Conclusion**: Even with using individual motors on each wheel, and avoiding any type
of gearing, our robot still drifts. However, the drift in this project/test does not seem to be
limited in a certain direction, thus, we conclude that the original drift problem we had in
previous projects is resolved and these current inaccuracies are simply a result of inaccuracies in
our machinery.

| **Velocity** [%] | 15 | 30 | 50 | 70 |
| - | - | - | - | - |
| **Avg. Abs. Angle Diff.** [degree] | 3.12 | 4.66 | 10.21 | 9.08 |

**Secondary Conclusion**: The amount by which the robot drifts does not seem to follow a linear
increase (, but rather somthing closer to exponential). There might be a decline in drift at higher
speeds to the inner inertia of the robot, however I would at the moment attribute that to measuring
inconsitencies. (This might be worth looking into in the future if we are having speed or drifting
issues.)
