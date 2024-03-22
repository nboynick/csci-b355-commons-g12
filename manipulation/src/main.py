#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
limit_switch_a = Limit(brain.three_wire_port.a)
limit_switch_b = Limit(brain.three_wire_port.b)
motor_1 = Motor(Ports.PORT1, True)
motor_2 = Motor(Ports.PORT2, True)
potentiometer_c = PotentiometerV2(brain.three_wire_port.d)
potentiometer_d = PotentiometerV2(brain.three_wire_port.f)
servo_e = Servo(brain.three_wire_port.e)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
#
# 	Project:      Manipulation Demonstration
#	Author:       Creed (Goldencode20), Augie, Nathaniel (nboynick)
#	Created:      2024-03-21
#	Description:  A 2-joint planar robot manipulator that can pick up and move cans.
#
# ------------------------------------------

# Library imports
from vex import *

"""Notes
- Motor 1 is the shoulder motor; motor 2 is the arm motor
- Limit A is the shoulder calibrator; limit b is the arm calibrator
- Shoulder gear ratio: 24:1 + 12:36 (1:3) --> 72 input rotations for 1 output rotation
- Arm gear ratio:
"""

# Begin project code
def get_theta_2():
    # Theta 2 is the angle on the second, outer, arm joint
    pass

def get_theta_1():
    # Theta 1 is the angle on the first, inner, shoulder joint
    pass

def calibration():
    # Motor 1 Calibration
    motor_1.spin(REVERSE)
    while not limit_switch_a.pressing():
        temp = motor_1.temperature(PERCENT)
        if temp > 60:
            motor_1.stop()
    motor_1.stop()
    motor_1.set_position(0, DEGREES)
    motor_2.set_position(0, DEGREES)
    pot_c = potentiometer_c.angle(DEGREES)
    # Motor 2 Calibration
    return (pot_c, 0)

def init():
    motor_1.set_velocity(20, PERCENT)
    motor_2.set_velocity(20, PERCENT)

def calculate_shoulder_rotation_count(output_degree_change):
    return 72 * (output_degree_change/360)

def main():
    # Variables
    potentiometer_c_offset = 0
    potentiometer_d_offset = 0

    # Initialization (Set motor speed, etc.)
    init()

    print("Start:")
    print(potentiometer_c.angle(DEGREES))

    # Calibration of the motor encoders
    potentiometer_c_offset, potentiometer_d_offset = calibration()

    print("Angle:")
    print(potentiometer_c_offset)

    # Move motor 1 to show our understanding
    # motor_1.spin_for(FORWARD, calculate_shoulder_rotation_count(), TURNS, wait=False) # Spin output arm by 30 degrees
    # while motor_1.is_spinning():
    #     temp = motor_1.temperature(PERCENT)
    #     if temp > 60:
    #         motor_1.stop()
    #     print(temp)
    #     wait(50, MSEC)

main()
