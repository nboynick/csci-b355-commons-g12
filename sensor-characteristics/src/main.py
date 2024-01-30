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
def find_light_source(reset_position=False, verbose=False):
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
"""Notes to ourselves for this assignment part:
- Providing a light source at specific (known) locations/angles, then moving the optical sensor in
  that direction, and using the potentiometer to get the angle -> the servo can move to a specific
  location but can't give feedback of where it is
- Then using multiple different methods for the optical sensor check which one provides the best
  results (using root-mean-square error with the location found from the find_light_source function
  and our previous control angle)
- Since we already know what angle the servo motor is rotated towards after finding a light source,
  then why do we need to get readout from the potentiometer?
"""
def get_control_angles(specified_angles=None, angle_count=1, return_dict=False, verbose=False):
    """Get potentiometer values for testing angles.
    
    @param specified_angles:list[int] A list of specified servo angles for which to return the
                                      potentiometer readings. Default: None.
    @param angle_count:int Number of angles for which to go through the checking process. This only
                           has an effect if no angles to check are specified, i.e., the manual
                           angle finding method is being used. Default: 1.
    @param return_dict:{int,float} Change the returned output to returning a dictionary of
                                   {angle_count,angle_degree}.
    @param verbose:bool Print extra degbugging information to the console (not the VEX brain).
    @return [(int,float)] Return a list of tuples of the angle counts and the measured rotation
                          degree.
    """
    csp = 0 # current servo position
    optical_servo.set_position(0, DEGREES)
    pa = {} # potentiometer angles
    if specified_angles == None: # Check the potentiometer manually
        for cac in range(1, angle_count+1, 1): # cac = current angle count
            brain.screen.clear_screen;brain.screen.set_cursor(1,1)
            brain.screen.print("Adjust to %s angle." % str(cac))
            brain.screen.new_line()
            brain.screen.print("Then use checkmark button to confirm.")
            brain.screen.new_line()
            brain.screen.print("Use left/right buttons to adjust optical\nsensor orientation.")
            brain.screen.new_line()
            while True:
                if brain.buttonLeft.pressing:
                    csp = csp-1 if csp > (-50) else csp
                    optical_servo.set_position(csp, DEGREES)
                elif brain.buttonRight.pressing:
                    csp = csp+1 if csp < 50 else csp
                    optical_servo.set_position(csp, DEGREES)
                elif brain.buttonCheck.pressing:
                    pv = potentiometer.angle(DEGREES) # potentiometer value
                    pa[cac] = pv # save the potentiometer value for the current angle
                    if verbose: print("Current Angle:%s\nPot. Value:%s" % (cac,pv))
                    break
            brain.screen.print("Value recorded.")
            brain.screen.new_line()
    else: # Check the potentiometer for a set of preset angles
        for angle in specified_angles:
            optical_servo.set_position(angle)
            pv = potentiometer.angle(DEGREES) # potentiometer value
            pa[angle] = pv
    if return_dict: return pa
    output = [] # return output as a list of tuples (angle_index, measured_angle_degree)
    for key,value in pa.items():
        output.append((key,value))
    return output

def calculate_rms_error(angle_count=6, verbose=False, use_servo_angle=False):
    """Calculate the Squared Error in using light-source for angle retrieval.
    
    @param angle_count:int The number of separate angles that will be tested.
    @param verbose:bool Print extra debugging information.
    @param use_servo_angle:bool Use the reported angle from the servo motor instead of the readout
                                from the potentiometer when calculating the squared error.
    @return float The average squared error in this test.
    """
    sq_er = [] # squared errors
    cont_ang = get_control_angles(angle_count=angle_count) # control angle values from potentiometer
    for count in range(0,angle_count,1):
        servo_est_ang = find_light_source() # Find angle based on light source
        pot_est_ang = potentiometer.angle(DEGREES) # potentiometer value
        if not use_servo_angle:
            sq_er.append((cont_ang[count] - pot_est_ang)**2)
        else:
            sq_er.append((cont_ang[count] - (servo_est_ang+150))**2)
    from statistics import mean
    avg_err = mean(sq_er)
    if verbose: print("Average Squared Error: %s" % str(avg_err))
    return avg_err

### 3: Phototaxis

### 4: Color Track

### DELETED BAD CODE
# max_position = 0
# brightest_so_far = 0
# for key,value in position_values.items():
#     if value > brightest_so_far:
#         max_position = key
#         brightest_so_far = value