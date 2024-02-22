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
limit_switch_b = Limit(brain.three_wire_port.b)
limit_switch_c = Limit(brain.three_wire_port.c)
servo_a = Servo(brain.three_wire_port.a)
distance_8 = Distance(Ports.PORT8)
orientation_f = PotentiometerV2(brain.three_wire_port.f)


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

# LIBRARY IMPORTS ##############################################################################################
from vex import *
import math
# COPY CODE FROM src.py INTO THIS FILE



# CONSTANTS #######################################################################################
OPTICAL_ANGLE = 40


# GLOBAL VARIABLES ##############################################################################################
base_wall_dist = -1 # base wall distance in MM
theo_head = 0       # current base heading in degrees (one of the four cardinal directions)
stabilize = True    # toggle for the separate stabilization thread
# pre_stab_time = 0   # brain clock value the last time the stabilization code was run
right_bump_on = False
left_bump_on = False
init_finished = False



# DEBUGGING ####################################################################################################
def print_debug(func_name, new_wall_dist):
    # Import global variables into the function scope
    global base_wall_dist
    global theo_head

    # Construct the debug string
    string = "M"
    string += "  T:" + str(round(brain.timer.time(SECONDS), 3))
    string += "  F:" + func_name
    string += "  BD:" + str(base_wall_dist)
    string += "  ND:" + str(new_wall_dist)
    string += "  H:" + str(theo_head)
    string += ":::"

    # Print the debug string
    # print(string)

    # Wait to ensure that the string has been cleared out of the buffer
    wait(20, MSEC)



def distance_out_of_range():
    drivetrain.stop()
    global stabilize
    stabilize = False
    print("Distance Error Encountered. Bot halted, now printing distance values.")
    while True:
        print(int(distance_8.object_distance(MM)))



def incorrect_state_wall_and_bump():
    drivetrain.stop()
    global stabilize
    stabilize = False
    print("Check bot for weird condition. Left wall gap but also bumping.")



# HELPER METHODS ############################################################################################
def heading_aligned():
    # Import global variables into the local scope
    global theo_head

    # Obtain the current heading measurement
    cur_head = brain_inertial.heading(DEGREES)

    # Normalize both to the (90, 450) range to prevent accidental rollover
    ref_head = theo_head + 90
    cur_head += 90

    # Return false if a new aligment needs to be executed
    if cur_head < (ref_head - 1) or cur_head > (ref_head + 1):
        return False
    return True



def modify_theo_head(direction):
    # Import global variables into the local scope
    global theo_head

    # Figure out by in which direction the value needs to be modified
    if direction == "r":
        modification_value = 90
    elif direction == "l":
        modification_value = (-90)
    else:
        print("Error in modify_theo_head: direction=" + str(direction) + ":::")

    # Check if the global variable will have rollover and thus modify it
    # This is (unnecessarily) complex due to the theo_head variable also being used in the other thread
    #   --> thread safety issues if it is not modified in one single step
    if theo_head + modification_value > 360:
        theo_head += (modification_value - 360)
    elif theo_head + modification_value < 0:
        theo_head += (modification_value + 360)
    else:
        theo_head += modification_value



def update_drivetrain():
    # Import global variables into the local scope
    global theo_head
    global stabilize

    print("b")

    # Prevent the stabilization thread from running
    stabilize = False

    # Update the drivetrain
    drivetrain.stop()
    drivetrain.turn_to_heading(theo_head, DEGREES)
    drivetrain.drive(FORWARD)

    # Restart the stabilization thread
    stabilize = True



def turn_right_after_bump():
    # Back away from the corner to give ourselves turning space
    drivetrain.stop()
    drivetrain.drive_for(REVERSE, 51, MM)

    # Call the turn right function
    turn_right()



def turn_right():
    # Modify the theoretical heading
    modify_theo_head("r")

    # Update the drivetrain to recognize the changes
    update_drivetrain()



def clear_wall():
    pass



def turn_left(wall_dist):
    # Modify the theoretical heading
    modify_theo_head("l")

    clearance = wall_dist * (math.cos(math.radians(50)))
    clearance += 280
    drivetrain.stop()
    drivetrain.drive_for(FORWARD, clearance, MM)

    # Update the drivetrain to recognize the changes
    update_drivetrain()



def register_right_bump():
    global right_bump_on
    right_bump_on = True

def register_left_bump():
    global left_bump_on
    left_bump_on = True



def add_left_wall_buffer():
    global stabilize
    stabilize = False
    print("a")
    drivetrain.drive_for(REVERSE, 250, MM)
    drivetrain.turn_for(RIGHT, 7, DEGREES, wait=True)
    drivetrain.drive_for(FORWARD, 200, MM)
    update_drivetrain()



def init():
    # Import global variabels into the local scope
    global init_finished

    # Drivetrain
    calibrate_drivetrain()

    # Heading Stabilization
    heading_correction_thread = Event()
    heading_correction_thread(correct_heading)
    wait(15, MSEC)
    heading_correction_thread.broadcast()

    # Servo Adjust
    servo_a.set_position(-50, DEGREES)
    wait(600, MSEC)

    # Brain Timer Restart
    brain.timer.clear()

    # Drivetrain Speeds
    drivetrain.set_drive_velocity(40, PERCENT)
    drivetrain.set_turn_velocity(30, PERCENT)

    # Setup the limit switch callbacks
    limit_switch_b.pressed(register_left_bump)
    limit_switch_c.pressed(register_right_bump)
    bumper_reset_thread = Event()
    bumper_reset_thread(reset_bumper_switches)
    wait(15, MSEC)
    bumper_reset_thread.broadcast()

    # Wait until log output is ready
    wait(1, SECONDS)
    brain.screen.clear_row(1)
    brain.screen.set_cursor(1,1)
    brain.screen.print("Here")

    # Commence the other threads
    init_finished = True



# CORE PROJECT THREADS ######################################################################################
def correct_heading():
    # Import global variables into the local scope
    global stabilize
    # global pre_stab_time
    global theo_head
    global init_finished

    while not init_finished:
        wait(200, MSEC)

    # Continuousely check if new alignment should be performed
    while True:
        if stabilize and heading_aligned():
            # Perform the re-alignment
            drivetrain.stop()
            drivetrain.turn_to_heading(theo_head, DEGREES, wait=True)
            drivetrain.drive(FORWARD) # Potential issue

            # Postpone future alignment at least 1 second (prevent constant re-alignment)
            pre_wait_time = round(brain.timer.time(SECONDS), 3)
            wait(1, SECONDS)
            post_wait_time = round(brain.timer.time(SECONDS), 3)

            # Debug statement
            print("alignment")
            # If this debug is not giving back ~1 second separated times, then we will have to go back to
            #   checking for the time as part of one of the conditional statements instead of a wait fn call
            # print("A  Pre:" + str(pre_wait_time) + "  Post:" + str(post_wait_time) + ":::")



def reset_bumper_switches():
    global init_finished

    while not init_finished:
        wait(200, MSEC)

    global right_bump_on
    global left_bump_on
    while True:
        print("bumper reset  " + str(left_bump_on) + "  " + str(right_bump_on))
        right_bump_on = False
        left_bump_on = False
        wait(1000, MSEC)




def main():
    # Make sure everything has been initialized
    init()

    # Import global variables into the local scope
    global base_wall_dist
    global theo_head
    # global stabilize


    base_wall_dist = distance_8.object_distance()
    drivetrain.drive(FORWARD)

    while True:
        # Obtain the current distance sensor measurement
        new_dist = int(distance_8.object_distance(MM))

        # Compare base dist to new dist (the absolute numbers are a buffer region due to inacurate walls)
        left_wall_fallaway = new_dist > (base_wall_dist + 127) # 5in
        center_wall_approach = new_dist < (base_wall_dist - 51) # 2in
        # bumping_into_wall = limit_switch_b.pressing() or limit_switch_c.pressing()
        bumping_into_wall = right_bump_on and left_bump_on

        if left_bump_on and not right_bump_on:
            add_left_wall_buffer()

        # Error if left wall gap but also limit swtich pressing
        if left_wall_fallaway and bumping_into_wall:
            incorrect_state_wall_and_bump()

        # Optimization, only get new distance again if needed
        resync_new_distance = True

        # In order of precedence: bumper, left, right, drive
        if bumping_into_wall:
            print_debug("RightBump", new_dist)
            turn_right_after_bump()
        elif left_wall_fallaway:
            print_debug("Left", new_dist)
            turn_left(base_wall_dist)
        # elif center_wall_approach:
        #     print_debug("Right", new_dist)
        #     turn_right()
        else:
            resync_new_distance = False

        # If a change in the state was created, re-obtain wall distance
        if resync_new_distance:
            new_dist = int(distance_8.object_distance(MM))

        # Set current wall distance to the base wall distance for the next loop
        base_wall_dist = new_dist



main()
