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
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 259.34, 320, 40, MM, 1)
servo_a = Servo(brain.three_wire_port.a)
bumper_d = Bumper(brain.three_wire_port.d)
distance_8 = Distance(Ports.PORT8)
motor_3 = Motor(Ports.PORT3, False)


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
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *



# Begin project code

def adjust(wall_dif):
    drivetrain.stop()
    if(wall_dif > 0):
	    drivetrain.turn_for(LEFT, 5, DEGREES)
    else:
	    drivetrain.turn_for(RIGHT, 5, DEGREES)

def turn_left():
    drivetrain.stop()
    drivetrain.drive_for(FORWARD, 170,  MM)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    #Maybe have it drvie forward until it sees the wall the jump back to old function

def alt_turn_left():
    drivetrain.stop()
    left_motor_a.set_velocity(50, PERCENT)
    left_motor_b.set_velocity(50, PERCENT)
    right_motor_a.set_velocity(60, PERCENT)
    right_motor_b.set_velocity(60, PERCENT)
    while (TRUE):
        if(distance_8.object_distance(MM) < 50):
            break
    drivetrain.stop()
    #This should stop and work fine for driving after?

def turn_right(): 
    drivetrain.stop()
    drivetrain.drive_for(REVERSE, 10, MM)
    drivetrain.turn_for(RIGHT, 90, DEGREES)

def init():
    servo_a.set_position(33, DEGREES)
    calibrate_drivetrain()

def main():
    init()

    curr_dist = 0
    past_dist = distance_8.object_distance(MM)
    time_since_last_change = 0

    while True:
        curr_dist = distance_8.object_distance(MM)
        wall_dif = curr_dist - past_dist
        drivetrain.drive(FORWARD)
        if(curr_dis > (past_dist + 75)):
            turn_left()
            #alt_turn_left()
            time_since_last_change = 0
        elif(abs(wall_dif) > 5):
            adjust(wall_dif)
            time_since_last_change = 0
        elif(bumper_d.pressing()):
            turn_right()
            time_since_last_change = 0
        elif(time_since_last_change > 100):
            drivetrain.turn_for(LEFT, 90, DEGREES)
        else:
            time_since_last_change += 1
        past_dis = curr_dist

main()