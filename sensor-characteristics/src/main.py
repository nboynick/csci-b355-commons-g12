# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Creed, Augie, Nathaniel                                      #
# 	Created:      1/27/2024, 4:47:56 PM                                        #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_motor = Motor(Ports.PORT1, True)
right_motor = Motor(Ports.PORT5, False)
"""Notes on the Motors
- Due to the gears leading to an inversion of the drive direction, it is in fact the left motor that
  has to spin in inverse to go forwards.
"""
drivetrain = SmartDrive(left_motor, right_motor, brain_inertial, 219.44, 320, 40, MM, 1.6666666666666667)
bumper_right = Bumper(brain.three_wire_port.b)
bumper_left = Bumper(brain.three_wire_port.a)
distance = Distance(Ports.PORT8)
optical = Optical(Ports.PORT3)
optical_servo = Servo(brain.three_wire_port.g)
potentiometer = PotentiometerV2(brain.three_wire_port.h)
"""Notes on Potentiometer:
- The angles function needs "DEGREES" as an explicit argument. If not it returns the value as a
  percentage, unlike what the documentatino claims.
- Angles are calculated based on the "safe" area of the potentiometer. I.e., the angle 0 degrees
  corresponds to the first rotation marking on the potentiometer. This means, that "straigh forward"
  is actually only 150 degrees (not 180).
"""

# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# Calibrating the Drivetrain
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
calibrate_drivetrain()

### PROJECT SPECIFIC CODE BELOW HERE ###############################################################
### 1: Active Directionality Sensing
def find_light_source(reset_position=True, verbose=False):
    """Finds the direction of the strongest light source.

    The function cycles through all the possible servo motor positions for the optical sensor
    searching addon on the SquareBot, and returns the rotation degree for the strongest light level
    that was found.

    @param reset_position:bool Optional argument to rotate the servo (and the attached optical
                               sensor) back in the direction of the strongest lightsource that was
                               found. Default: True.
    @param verbose:bool Optional argument to turn on verbose variable printing for debugging
                        purposes. This will print the information to the console, and not the VEX
                        brain's screen. Default: False
    @return:int The degree rotation of the strongest lightsource found. This considers 0 degrees to
                be straight in front of the robot, negative degrees to be facing (in the forward
                driving direction of the robot) towards the left, and positive degrees to be facing
                towards the right.
    """
    position_values = {}
    for i in range(-50, 51, 1):
        optical_servo.set_position(value=i, units=DEGREES)
        wait(duration=100, units=MSEC)
        brightness = optical.brightness()
        position_values[i] = brightness
    if verbose: print(position_values)
    max_position = [key for key,value in position_values.items()
                    if value == max(position_values.values())][0]
    if verbose: print(max_position)
    if reset_position: optical_servo.set_position(max_position);wait(100,MSEC)
    return (max_position * -1)
# brain.screen.print(find_light_source())
# brain.screen.new_line()

### 2: Accuracy Measurement


### 3: Phototaxis

### 4: Color Track

### DELETED BAD CODE
# max_position = 0
# brightest_so_far = 0
# for key,value in position_values.items():
#     if value > brightest_so_far:
#         max_position = key
#         brightest_so_far = value