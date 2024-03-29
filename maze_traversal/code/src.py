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
servo_distance = Servo(brain.three_wire_port.a)
distance_8 = Distance(Ports.PORT8)
orientation_f = PotentiometerV2(brain.three_wire_port.f)
bumper_front_right = Bumper(brain.three_wire_port.d)
bumper_front_left = Bumper(brain.three_wire_port.e)
optical_3 = Optical(Ports.PORT3)
limit_back_left = Limit(brain.three_wire_port.g)
limit_back_right = Limit(brain.three_wire_port.h)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

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



"""Work Comments:
"""

"""Memos:
"""



# CONSTANTS ########################################################################################
ROBOT_LENGTH = 170  # in MM
DRIVETRAIN_DRIVE_SPEED = 35
DRIVETRAIN_TURN_SPEED = 15
PRINTING_TIMEOUT = 60  # timeout used between print calls in miliseconds


SERVO_LEFT = 33
SERVO_STRAIGHT = 2 # not working
SERVO_RIGHT = (-34)

# Print messages marked as debugging (i.e., those using the my_printd function)
DEBUG_MODE = True

# Permanently turn off the callback/separeate 'thread' used for heading stabilization
GLOBAL_STABILIZATION_SCHUTOFF = True

# Distance between the tip of the distance sensor and the tip of the axle when the distance sensor
# is turned 90° towards the left
AXLE_OPTICAL_DISTANCE = 70

# Distance constant used in various contexts (in milimeters)
# TODO: Find better namings
# Minimum needed change in the distance to the left wall to consider it to be a hole/gap/potential
#  left turn
MINIMUM_WALL_DIST_INCREASE_LEFT_TURN_POSSIBILITY = 75
# Minimum distance to maintain between the left wall and the outside of the left axle before triggering
#  some form of wall evasion code
MINIMUM_LEFT_WALL_SEAPARATION_DIST = 20
# Width of the band of distance in which we want the robot to be driving (used for calculating the max
#  distance away from the left wall)
LEFT_WALL_SEPARATION_BAND = 75
# Maximum distance that the bot should be away from the left wall before moving closer to the left wall
#  again
MAXIMUM_LEFT_WALL_SEPARATION_DIST = MINIMUM_LEFT_WALL_SEAPARATION_DIST + LEFT_WALL_SEPARATION_BAND





# GLOBAL VARIABLES #################################################################################
heading_stabilization_on = False
current_theoretical_heading = 0  # in degrees

limit_triggered_past_iter = False
most_recent_turn = None





# DEBUGGING ########################################################################################
def my_print(input_string):
    # Import global constants into the local scope
    global PRINTING_TIMEOUT

    # Add a timestamp to the output
    current_time = brain.timer.time(SECONDS)
    current_time = round(current_time, 2)
    output_string = str(current_time) + "--" + input_string + "---"

    # Print the string
    print(output_string)

    # Wait/Timeout to prevent output tearing/incomleteness
    wait(PRINTING_TIMEOUT, MSEC)



def my_printd(input_string):
    global DEBUG_MODE
    if DEBUG_MODE:
        my_print(input_string)




# HELPER METHODS ###################################################################################
def init():
    # Import global variables into the local scope
    global DRIVETRAIN_DRIVE_SPEED
    global DRIVETRAIN_TURN_SPEED
    global heading_stabilization_on
    global SERVO_LEFT

    # Give user feedback - Part 1
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Initializing...")

    # Drivetrain stuff
    calibrate_drivetrain()
    drivetrain.set_drive_velocity(DRIVETRAIN_DRIVE_SPEED, PERCENT)
    drivetrain.set_turn_velocity(DRIVETRAIN_TURN_SPEED, PERCENT)

    # Position distance sensor's servo
    servo_distance.set_position(SERVO_LEFT, DEGREES)
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

    # Register limit switch callbacks
    limit_back_right.pressed(limit_left_triggered)

    # Reset brain's timer to reflect "actual" runtime
    brain.timer.clear()
    pass



def limit_left_triggered():
    drivetrain.stop()
    my_printd("limit")
    global most_recent_turn
    global current_theoretical_heading
    copy_most_recent = most_recent_turn
    my_printd("h:" + str(current_theoretical_heading))
    if most_recent_turn == "right":
        set_current_theoretical_heading("left")
    elif most_recent_turn == "left":
        set_current_theoretical_heading("right")
    my_printd("h:" + str(current_theoretical_heading))
    correct_heading()
    my_printd("ah:" + str(brain_inertial.heading(DEGREES)))
    drivetrain.drive_for(FORWARD, 100, MM)
    set_current_theoretical_heading(copy_most_recent)
    my_printd("h:" + str(current_theoretical_heading))
    correct_heading()
    my_printd("ah:" + str(brain_inertial.heading(DEGREES)))



def correct_heading():
    # Import global variables into the local scope
    global current_theoretical_heading

    # Prevent the drivetrain from potentially already moving forward
    drivetrain.stop()

    # Realign the drivetrain (through VEX API call) with what our current heading should be
    drivetrain.turn_to_heading(current_theoretical_heading, DEGREES, wait=False)
    wait(10, SECONDS)



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



def set_current_theoretical_heading(direction):
    # Import global variables into the local scope
    global current_theoretical_heading
    global most_recent_turn

    # Modify the heading based on the provided direction
    if direction == "right":
        current_theoretical_heading += 90
        most_recent_turn = "right"
    elif direction == "left":
        current_theoretical_heading -= 90
        most_recent_turn = "left"
    else:
        my_printd("bug in set_current_theoretical_heading:" + str(direction))

    # Ensure heading value within constrains (i.e., normalize to 0 - 359 degrees)
    if current_theoretical_heading > 360:
        current_theoretical_heading -= 360
    elif current_theoretical_heading < 0:
        current_theoretical_heading += 360



# def realign_with_wall():
#     # TODO: REFACTOR
#     global heading_stabilization_on
#     heading_stabilization_on = False
#     global current_theoretical_heading
#     drivetrain.stop()
#     # Get the current distance to wall
#     first_wall_dist = distance_8.object_distance(MM)
#     # Drive forward by min. 2 inches/51MM ?
#     travel_distance = 102 # in MM
#     drivetrain.drive_for(FORWARD, travel_distance, MM)
#     # Get second distance
#     second_wall_dist = distance_8.object_distance(MM)
#     # Do the math
#     wall_distance_change = second_wall_dist - first_wall_dist
#     print("wall:" + str(wall_distance_change))
#     turn_right = True
#     if wall_distance_change > 0:
#         turn_right = False
#     wall_distance_change = abs(wall_distance_change)
#     delta_angle = math.degrees(math.atan(wall_distance_change / travel_distance))
#     print("ang:" + str(delta_angle))
#     # Set the new heading
#     if turn_right:
#         current_theoretical_heading += delta_angle
#     else:
#         current_theoretical_heading -= delta_angle
#     print("head:" + str(current_theoretical_heading))
#     # Update current heading
#     correct_heading()
#     heading_stabilization_on = True



def prevent_wall_rubbing(side):
    # Local variables used for code manipulation (i.e., fine tuning)
    backtrack_distance = 200  # in MM
    evasion_angle = 5  # in degrees

    # Import global variables into the local scope
    global heading_stabilization_on
    global current_theoretical_heading


    # Prevent the drivetrain from driving forward during the turn
    drivetrain.stop()

    # Prevent heading stabilization during the turn
    heading_stabilization_on = False

    # Choose turn direction
    if side == "left":
        evasion_direction = RIGHT
        current_theoretical_heading += 1
    elif side == "right":
        evasion_direction = LEFT
        current_theoretical_heading -= 1
    else:
        my_printd("prevent_wall_rubbing:bad side argument=" + str(side))

    # Calculate evasion distance
    evasion_distance = backtrack_distance * math.cos(math.radians(abs(evasion_angle)))

    # Drive backwards, rotate slightly, drive forwards a bit (to give buffer to the wall), realign with original heading
    drivetrain.drive_for(REVERSE, backtrack_distance, MM)
    drivetrain.turn_for(evasion_direction, evasion_angle, DEGREES)
    drivetrain.drive_for(FORWARD, evasion_distance, MM)
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
    drivetrain.drive_for(REVERSE, 90, MM)

    # Modify the theoretical heading
    set_current_theoretical_heading("right")

    # Make the turn (update the robots position to reflect the change in theoretical heading)
    correct_heading()

    # Re-enable heading stabilization after finishing the turn
    heading_stabilization_on = True



def refind_wall():
    # Import global variables into the local scope
    global DRIVETRAIN_DRIVE_SPEED

    # Stop the drivetrain (to make changes to its config)
    drivetrain.stop()

    # Slow down the drivetrain to not accidentally miss a U-turn wall
    drivetrain.set_drive_velocity(35, PERCENT)

    # Drive forward until a wall is registered
    drivetrain.drive(FORWARD)
    far_corridor_dist = distance_8.object_distance(MM)
    while True:
        temp = distance_8.object_distance(MM)
        if temp < (far_corridor_dist - 220) and temp < 400: # potential bug
            drivetrain.stop()
            break

    # Debugging
    output = "RW"
    output += ":far_corr_dist=" + str(far_corridor_dist)
    output += ":new_dist=" + str(distance_8.object_distance(MM))
    my_printd(output)

    # Rvert changes made to the drivetrain config
    drivetrain.set_drive_velocity(DRIVETRAIN_DRIVE_SPEED, PERCENT)



def turn_left():
    # Import global variables into the local scope
    global ROBOT_LENGTH
    global DISTANCE_SENSOR_SERVO_POSITION
    global heading_stabilization_on

    # Prevent the drivetrain from driving forward during the turn
    drivetrain.stop()

    # Prevent heading stabilization during the turn
    heading_stabilization_on = False

    # Drive forwards to avoid the wall
    wall_clearance_distance = ROBOT_LENGTH
    debugvar_dist__travelled_after_fn_call = 50
    drivetrain.drive_for(FORWARD, (wall_clearance_distance - debugvar_dist__travelled_after_fn_call), MM)

    # Modify the theoretical heading
    set_current_theoretical_heading("left")

    # Make the turn (update the robots position to reflect the change in theoretical heading)
    correct_heading()

    my_printd("here")
    # Move forward to make distance sensor see the new wall
    refind_wall()

    output_string = "TL"
    # output_string += ":wall_clear_dist=" + str(wall_clearance_distance)
    my_printd(output_string)

    # Re-enable heading stabilization after finishing the turn
    heading_stabilization_on = True





# PARALLEL THREADS #################################################################################
def check_heading_alignment():
    # Import global variables into the local scope
    global heading_stabilization_on
    global GLOBAL_STABILIZATION_SCHUTOFF

    # Instantiate a permanent loop
    while True and not GLOBAL_STABILIZATION_SCHUTOFF:
        # Check conditions for heading re-alignment
        # Note: Use the double loop to prevent calling is_heading_aligned() unless actually necessary, whilst
        #       also maintaining the result of that function call for a debug print statement
        if heading_stabilization_on:
            heading_aligned_result = is_heading_aligned()
            if not heading_aligned_result:
                # Realign the heading (if needed)
                correct_heading()

                # Debugging statement
                string_output = "CHA:hso=" + str(heading_stabilization_on) + ":iha=" + str(heading_aligned_result)
                my_printd(string_output)

                # Prevent heading from being realigned more than once every <2> seconds
                wait(2, SECONDS)



def main():
    # Get global variables
    global current_theoretical_heading
    global AXLE_OPTICAL_DISTANCE

    # Initialize all the code/sensors
    init()

    # Local variables/(Things needed to figure out the state of the finite state machine)
    previous_wall_distance = distance_8.object_distance(MM)
    made_turn_this_iteration = False

    # Create main game loop
    while True:
        """
        Sensor Priorities (in terms of having to react to them quickly:
         - Distance sensor pointing towards the left wall
         - [Optical sensor pointing towards the front]
         - Front bumpers
        """

        # Process Distance Sensor
        current_wall_distance = int(distance_8.object_distance(MM)) - AXLE_OPTICAL_DISTANCE
        left_wall_gap = current_wall_distance > (previous_wall_distance + MINIMUM_WALL_DIST_INCREASE_LEFT_TURN_POSSIBILITY)
        if left_wall_gap: drivetrain.stop() # <-- This should probably only be used as a fallback option
        global MINIMUM_LEFT_WALL_SEAPARATION_DIST
        left_wall_too_close = current_wall_distance < MINIMUM_LEFT_WALL_SEAPARATION_DIST
        global MAXIMUM_LEFT_WALL_SEPARATION_DIST
        left_wall_too_far = False #current_wall_distance > MAXIMUM_LEFT_WALL_SEPARATION_DIST

        # Process Optical Sensor
        # TODO: for future reference

        # Process Bumper(s) input
        front_left_bumper_pressing = bumper_front_left.pressing()
        front_right_bumper_pressing = bumper_front_right.pressing()
        bumper_pressed = front_left_bumper_pressing or front_right_bumper_pressing

        # Debugging
        output_string = ("M" +
                         ":pwd=" + str(previous_wall_distance) +
                         ":cwd=" + str(current_wall_distance) +
                         ":flbp=" + str(front_left_bumper_pressing) +
                         ":frbp=" + str(front_right_bumper_pressing) +
                         ":head=" + str(current_theoretical_heading))
        my_printd(output_string)

        # Process the state
        #   Order of precedence: bumper, limit switches, distance, (no input/keep driving forward)     NEEEDS WOOORRRKRKKKKK---------<<<-----<-----------------<<<<--------
        #   More states possible through combinations??
        if bumper_pressed:
            my_printd("TR")
            turn_right()
            made_turn_this_iteration = True
        elif left_wall_too_close:
            my_printd("LWTC")
            prevent_wall_rubbing("left")
        elif left_wall_too_far:
            my_printd("RWTC")
            prevent_wall_rubbing("right")
        elif left_wall_gap:
            my_printd("LWG")
            turn_left()
            made_turn_this_iteration = True
        else:
            drivetrain.drive(FORWARD)

        # Re-find current distance after a turn was executed
        if made_turn_this_iteration:
            current_wall_distance = distance_8.object_distance(MM)
            made_turn_this_iteration = False

        # Cleanup
        previous_wall_distance = current_wall_distance



main()


# def Test():
#     servo_distance.set_position(20, DEGREES)
#     wait(900, MSEC)
#     servo_distance.set_position(3, DEGREES)

# Test()
