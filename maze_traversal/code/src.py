
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
# COPY CODE FROM src.py INTO THIS FILE


# Heading Stabilization Variables
stabilize_heading = True # Turn off temporarily to be able to turn a corner
last_stabilization_time = 0
current_heading = 0 # Either 0, 90, 180, or 270; Used to stabilize the heading

def correct_heading():
    global stabilize_heading
    global current_heading
    while True:
        # Note: It might be simpler/faster to simply write a wait(2,SEC) in each loop iteration
        if stabilize_heading and last_stabilization_time < (brain.timer.time(SECONDS) - 2):
            drivetrain.turn_to_heading(current_heading, DEGREES, wait=True)

def init():
    # Drivetrain
    calibrate_drivetrain()
    # Heading Stabilization
    heading_correction_thread = Event()
    heading_correction_thread(correct_heading)
    wait(15, MSEC)
    heading_correction_thread.broadcast()

def main():
    init()
    pass

main()
