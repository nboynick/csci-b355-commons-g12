#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
limit_switch_a = Limit(brain.three_wire_port.a)
limit_switch_b = Limit(brain.three_wire_port.b)
motor_1 = Motor(Ports.PORT1, False)
motor_2 = Motor(Ports.PORT2, False)
potentiometer_c = PotentiometerV2(brain.three_wire_port.c)
potentiometer_d = PotentiometerV2(brain.three_wire_port.d)
servo_e = Servo(brain.three_wire_port.e)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
#
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
#
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
def get_theta_2():
    # Theta 2 is the angle on the second, outer, arm joint
    pass

def get_theta_1():
    # Theta 1 is the angle on the first, inner, shoulder joint
    pass

def calibration():
    pass

def main():
    pass
