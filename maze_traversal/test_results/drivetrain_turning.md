# Drivetrain Turning

**Test Description**: We made the robot perform four 90° rotations repeated ten times to be able to
extract an average of how exact the drivetrain rotation function is, and whether it becomes more or
less accurate with a change in speed.

| **Velocity** [%] | **Absolute Angle Difference** [degree] |
| - | - |
| 30 | 0.49175 |
| 50 | 0.6845 |
| 70 | 0.5005 |

**Conclusion**: The accuracy in turning to a specific heading will most likely no be a noticeable
issue at any rotation speeds. Thus, we should set the rotation speed as high as possible.
(Sidenote: At higher speeds, the robot did have to counter-correct its rotation due to overshooting
its goal. This extra step might outweigh any performance gained in making the robot perform the
primary rotation faster.)

# Original Test Data for Reference

```Python
[(90.77, 180.91, 269.82,   0.97, 30),
 (89.20, 180.22, 269.74,   0.81, 30),
 (90.58, 180.42, 270.08, 359.97, 30),
 (90.57, 180.29, 270.15,   0.35, 30),
 (90.82, 180.23, 270.14,   0.43, 30),
 (90.99, 180.34, 270.89,   0.25, 30),
 (90.33, 180.09, 269.58,   0.80, 30),
 (89.41, 179.54, 269.53, 359.10, 30),
 (90.32, 180.68, 269.82, 359.22, 30),
 (90.86, 179.57, 269.14,   0.02, 30)]

[(90.13, 179.12, 269.28, 359.16, 50),
 (89.44, 180.11, 269.32, 359.87, 50),
 (89.78, 180.63, 270.23,   0.72, 50),
 (89.52, 179.42, 269.66, 359.37, 50),
 (90.89, 180.47, 269.56, 359.98, 50),
 (89.03, 180.65, 269.09,   0.57, 50),
 (89.68, 179.90, 269.65,   0.11, 50),
 (90.78, 180.60, 270.21, 359.43, 50),
 (90.50, 180.32, 277.43,   0.14, 50),
 (89.02, 180.32, 269.02, 359.13, 50)]

[(89.41, 180.10, 270.60,   0.52, 70),
 (89.98, 179.16, 270.99,   0.00, 70),
 (89.36, 179.81, 269.04, 359.47, 70),
 (90.05, 180.80, 270.59,   0.77, 70),
 (89.24, 179.98, 269.70, 359.13, 70),
 (89.31, 179.35, 269.70,   0.20, 70),
 (89.86, 179.24, 269.90, 359.34, 70),
 (89.21, 180.54, 270.15,   0.13, 70),
 (89.60, 179.34, 270.41, 359.63, 70),
 (89.65, 180.78, 269.08, 359.12, 70)]
```
