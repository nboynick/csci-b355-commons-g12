
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

# Library imports
from vex import *
import math
# COPY CODE FROM src.py INTO THIS FILE


# Heading Stabilization Variables
stabilize_heading = True # Turn off temporarily to be able to turn a corner
last_stabilization_time = 0
current_heading = 0 # Either 0, 90, 180, or 270; Used to stabilize the heading
old_distance = 0

def print_debug(func_name):
        print("T:" + str(round(brain.timer.time(SECONDS), 1)), end="")
        print("  D:" + str(round(distance_8.object_distance(), 1)), end="")
        print("  F:" + func_name)


def check_heading():
    global current_heading
    new_heading = brain_inertial.heading(DEGREES)
    old_temp = current_heading + 90
    new_heading += 90
    if new_heading < (old_temp - 5) or new_heading > (old_temp + 5):
        return True
    return False


def correct_heading():
    drivetrain.stop()
    global stabilize_heading
    global last_stabilization_time
    global current_heading
    while True:
        # Note: It might be simpler/faster to simply write a wait(2,SEC) in each loop iteration
        if stabilize_heading and last_stabilization_time < (brain.timer.time(SECONDS) - 0.5) and check_heading():
            print("Check heading")
            drivetrain.turn_to_heading(current_heading, DEGREES, wait=True)
            last_stabilization_time = brain.timer.time(SECONDS)
            drivetrain.drive(FORWARD)


def init():
    # Drivetrain
    calibrate_drivetrain()
    # Heading Stabilization
    heading_correction_thread = Event()
    heading_correction_thread(correct_heading)
    wait(15, MSEC)
    heading_correction_thread.broadcast()
    servo_a.set_position(-50, DEGREES)
    wait(600, MSEC)


def turn_left(old_distance):
    global stabilize_heading
    stabilize_heading = False

    global current_heading
    current_heading -= 90
    if current_heading < 0:
        current_heading += 360

    clearance = old_distance * (math.cos(math.radians(50)))
    clearance += 12
    drivetrain.drive_for(FORWARD, clearance, INCHES)

    drivetrain.turn_to_heading(current_heading, DEGREES)

    stabilize_heading = True


def turn_right():
    global stabilize_heading
    stabilize_heading = False

    global current_heading
    current_heading += 90
    if current_heading > 360:
        current_heading -= 360

    drivetrain.turn_to_heading(current_heading, DEGREES)

    stabilize_heading = True


def turn_right_bump():
    global old_distance

    print_debug("right-bump")

    global stabilize_heading
    stabilize_heading = False

    drivetrain.drive_for(REVERSE, 4, INCHES)
    turn_right()
    drivetrain.drive(FORWARD)

    old_distance = distance_8.object_distance(INCHES)

    stabilize_heading = True


def main():
    init()

    global old_distance

    limit_switch_b.pressed(turn_right_bump)
    # limit_switch_c.pressed(turn_right_bump)
    old_distance = distance_8.object_distance(INCHES)
    drivetrain.set_drive_velocity(30, PERCENT)
    drivetrain.set_turn_velocity(40, PERCENT)
    drivetrain.drive(FORWARD)
    while True:
        new_distance = distance_8.object_distance(INCHES)
        print(round(distance_8.object_distance(), 1))
        if new_distance > (old_distance + 7):
            drivetrain.stop()
            print_debug("left")
            turn_left(old_distance)
            drivetrain.drive(FORWARD)
            old_distance = distance_8.object_distance(INCHES)
        elif new_distance < (old_distance - 1):
            drivetrain.stop()
            print_debug("right")
            turn_right()
            drivetrain.drive(FORWARD)
            old_distance = distance_8.object_distance(INCHES)
        else:
            old_distance = new_distance

main()
