#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
left_motor_a = Motor(Ports.PORT1, False)
left_motor_b = Motor(Ports.PORT6, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT5, True)
right_motor_b = Motor(Ports.PORT10, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 219.44, 320, 40, MM, 1)
limit_switch_left = Limit(brain.three_wire_port.b)
limit_switch_right = Limit(brain.three_wire_port.c)
servo_distance = Servo(brain.three_wire_port.a)
distance_8 = Distance(Ports.PORT8)
orientation_f = PotentiometerV2(brain.three_wire_port.f)
bumper_front = Bumper(brain.three_wire_port.d)
bumper_rear = Bumper(brain.three_wire_port.e)
optical_2 = Optical(Ports.PORT2)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
#
# 	Project:      Maze Traversal
#	Author:       Creed (Goldencode20), Augie, Nathaniel (nboynick)
#	Created:      2024-02-16
#	Description:  Code for the maze traversal assignment
#
# ------------------------------------------

# LIBRARY IMPORTS ##################################################################################
from vex import *
import math





# CONSTANTS ########################################################################################
ROBOT_LENGTH = 280  # in MM
DISTANCE_SENSOR_SERVO_POSITION = -50
DRIVETRAIN_DRIVE_SPEED = 40
DRIVETRAIN_TURN_SPEED = 30





# GLOBAL VARIABLES #################################################################################
heading_stabilization_on = False
current_theoretical_heading = 0  # in degrees





# DEBUGGING ########################################################################################
def my_print(input_string):
    current_time = brain.timer.time(SECONDS)
    current_time = round(current_time, 3)
    output_string = str(current_time) + "--" + input_string + "---"
    print(output_string)
    wait(50, MSEC)





# HELPER METHODS ###################################################################################
def init():
    # Import global variables into the local scope
    global DISTANCE_SENSOR_SERVO_POSITION
    global DRIVETRAIN_DRIVE_SPEED
    global DRIVETRAIN_TURN_SPEED
    global heading_stabilization_on

    # Give user feedback - Part 1
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Initializing...")

    # Drivetrain stuff
    calibrate_drivetrain()
    drivetrain.set_drive_velocity(DRIVETRAIN_DRIVE_SPEED, PERCENT)
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_SPEED, PERCENT)

    # Position distance sensor's servo
    servo_distance.set_position(DISTANCE_SENSOR_SERVO_POSITION)
    wait(650, MSEC)

    # Initialize separte thread/callback for drive direction/heading alignment
    #  (alignment still turned off at this point)
    align_heading = Event()
    align_heading(check_heading_alignment)
    wait(20, MSEC)
    align_heading.broadcast()

    # Buffer for all changes to sink in
    wait(1000, MSEC) # Potentially remove this for competition day

    # Enable heading alignment
    heading_stabilization_on = True

    # Reset brain's timer to reflect "actual" runtime
    brain.timer.clear()
    pass



def is_heading_aligned():
    # Import global variables into the local scope
    global current_theoretical_heading

    # Obtain the current heading measurement
    current_actual_heading = brain_inertial.heading(DEGREES)

    # Normalize both to the (90, 450) range to prevent accidental rollover
    #  i.e. if we are off by less than 90 degrees, this function will work otherwise it will just give weird results
    reference_heading = current_theoretical_heading + 90
    current_actual_heading += 90

    # Return false if a new alignment needs to be executed
    if (current_actual_heading < (reference_heading - 1) or  # more than 1 degree error towards the LEFT
        current_actual_heading > (reference_heading + 1)):  # more than 1 degree error towards the RIGHT
        return False
    else:
        return True



def correct_heading():
    # Import global variables into the local scope
    global current_theoretical_heading

    # Prevent the drivetrain from potentially already moving forward
    drivetrain.stop()

    # Realign the drivetrain (through VEX API call) which what our current heading should be
    drivetrain.turn_to_heading(current_theoretical_heading, DEGREES, wait=True)



def set_current_theoretical_heading(direction):
    # Import global variables into the local scope
    global current_theoretical_heading

    # Modify the heading based on the provided direction
    if direction == "right":
        current_theoretical_heading += 90
    elif direction == "left":
        current_theoretical_heading -= 90
    else:
        my_print("bug in set_current_theoretical_heading:" + str(direction))

    # Ensure heading value within constrains (i.e., normalize to 0 - 359 degrees)
    if current_theoretical_heading > 360:
        current_theoretical_heading -= 360
    elif current_theoretical_heading < 0:
        current_theoretical_heading += 360



def prevent_wall_rubbing(side):
    # Import global variables into the local scope
    global heading_stabilization_on

    # Prevent the drivetrain from driving forward during the turn
    drivetrain.stop()

    # Prevent heading stabilization during the turn
    heading_stabilization_on = False

    # Drive backwards, rotate slightly, drive forwards a bit (to give buffer to the wall), realign with original heading
    drivetrain.drive_for(REVERSE, 200, MM)
    if side == "left":
        drivetrain.turn_for(RIGHT, 5, DEGREES)
    elif side == "right":
        drivetrain.turn_for(LEFT, 5, DEGREES)
    else:
        my_print("prevent_wall_rubbing:bad side argument=" + str(side))
    drivetrain.drive_for(FORWARD, 200, MM)
    correct_heading()

    # Re-enable heading stabilization after finishing the turn
    heading_stabilization_on = True



def turn_right():
    # Import global variables into the local scope
    global heading_stabilization_on

    # Prevent the drivetrain from driving forward during the turn
    drivetrain.stop()

    # Prevent heading stabilization during the turn
    heading_stabilization_on = False

    # Drive backwards to avoid the wall
    drivetrain.drive_for(REVERSE, 75, MM)

    # Modify the theoretical heading
    set_current_theoretical_heading("right")

    # Make the turn (update the robots position to reflect the change in theoretical heading)
    correct_heading()

    # Re-enable heading stabilization after finishing the turn
    heading_stabilization_on = True



def turn_left(wall_distance):
    # Import global variables into the local scope
    global ROBOT_LENGTH
    global DISTANCE_SENSOR_SERVO_POSITION
    global heading_stabilization_on

    # Prevent the drivetrain from driving forward during the turn
    drivetrain.stop()

    # Prevent heading stabilization during the turn
    heading_stabilization_on = False

    # Drive forwards to avoid the wall
    wall_clearance_distance = wall_distance * (math.cos(math.radians(abs(DISTANCE_SENSOR_SERVO_POSITION))))
    wall_clearance_distance += ROBOT_LENGTH
    drivetrain.drive_for(FORWARD, wall_clearance_distance, MM)

    # Modify the theoretical heading
    set_current_theoretical_heading("left")

    # Make the turn (update the robots position to reflect the change in theoretical heading)
    correct_heading()

    # Re-enable heading stabilization after finishing the turn
    heading_stabilization_on = True





# PARALLEL THREADS #################################################################################
def check_heading_alignment():
    # Import global variables into the local scope
    global heading_stabilization_on

    # Instantiate a permanent loop
    while True:
        # Check conditions for heading re-alignment
        # Note: Use the double loop to prevent calling is_heading_aligned() unless actually necessary, whilst
        #       also maintaining the result of that function call for a debug print statement
        if heading_stabilization_on:
            heading_aligned_result = is_heading_aligned()
            if not heading_aligned_result:
                # Realign the heading (if needed)
                correct_heading()
                # Prevent heading from being realigned more than once every <2> seconds
                wait(2, SECONDS)

                # Debugging statement
                string_output = "cha:hso=" + str(heading_stabilization_on) + ":iha=" + str(heading_aligned_result)
                my_print(string_output)



def main():
    # Get global variables
    # Initialize all the code/sensors
    init()

    # Local variables/(Things needed to figure out the state of the finite state machine)
    previous_wall_distance = distance_8.object_distance(MM)
    made_turn_this_iteration = False

    # Create main game loop
    while True:
        # Get sensor input
        current_wall_distance = distance_8.object_distance(MM)
        front_bumper_pressing = bumper_front.pressing()
        rear_bumper_pressing = bumper_rear.pressing()
        limit_left_pressing = limit_switch_left.pressing()
        limit_right_pressing = limit_switch_right.pressing()
        # optical input???

        # Parse sensor input
        distance_increased = current_wall_distance > (previous_wall_distance + 76)  # distance increase by >3in

        # Debugging
        output_string = ("M:cwd=" + str(current_wall_distance) +
                         ":fbp=" + str(front_bumper_pressing) +
                         ":rbp=" + str(rear_bumper_pressing) +
                         "llp=" + str(limit_left_pressing) +
                         "lrp=" + str(limit_right_pressing))
        my_print(output_string)

        # Process the state
        #   Order of precedence: bumper, limit switches, distance, (no input/keep driving forward)     NEEEDS WOOORRRKRKKKKK---------<<<-----<-----------------<<<<--------
        #   More states possible through combinations??
        if front_bumper_pressing:
            turn_right()
            made_turn_this_iteration = True
        elif rear_bumper_pressing:
            pass # Ignore for now
        elif limit_left_pressing:
            prevent_wall_rubbing("left")
            pass
        elif limit_right_pressing:
            prevent_wall_rubbing("right")
            pass
        elif distance_increased:
            turn_left(previous_wall_distance)
            made_turn_this_iteration = True
        else:
            drivetrain.drive(FORWARD)

        # Re-find current distance after a turn was executed
        if made_turn_this_iteration:
            current_wall_distance = distance_8.object_distance(MM)
            current_wall_distance = False

        # Cleanup
        previous_wall_distance = current_wall_distance



main()
