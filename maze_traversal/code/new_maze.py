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
bumper_e = Bumper(brain.three_wire_port.e)


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
    print("adjust")
    drivetrain.stop()
    #Check if the distance is postive and adjust to or form the wall as nesssiary
    if(wall_dif > 0):
	    drivetrain.turn_for(LEFT, 15, DEGREES)
    else:
	    drivetrain.turn_for(RIGHT, 15, DEGREES)
    wait(20, MSEC)

def turn_left():
    print("left")
    #Drive past the wall a little then turn and line somewhat back up with the wall.
    drivetrain.stop()
    drivetrain.drive_for(FORWARD, 300, MM)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 200, MM)
    #Maybe have it drvie forward until it sees the wall the jump back to old function

def alt_turn_left():
    print("alt left turn")
    drivetrain.stop()
    #Set all the motors to spin in such a way that the outside wheels go further than the inside wheels
    left_motor_a.set_velocity(10, PERCENT)
    left_motor_b.set_velocity(10, PERCENT)
    right_motor_a.set_velocity(40, PERCENT)
    right_motor_b.set_velocity(40, PERCENT)
    left_motor_a.spin(FORWARD)
    left_motor_b.spin(FORWARD)
    right_motor_a.spin(FORWARD)
    right_motor_b.spin(FORWARD)
    #Do this untile either the bumpers are pressed or we get too close to the wall
    while (True):
        front_left_bumper_pressing = bumper_e.pressing()
        front_right_bumper_pressing = bumper_d.pressing()
        bumper_pressed = front_left_bumper_pressing or front_right_bumper_pressing
        if(bumper_pressed):
            drivetrain.stop()
            drivetrain.set_drive_velocity(30, PERCENT)
            turn_right()
            break
        if(distance_8.object_distance(MM) < 50):
            drivetrain.stop()
            drivetrain.set_drive_velocity(30, PERCENT)
            break

def turn_right(): 
    print("right turn")
    #Back up then turn right in order to not hit a wall
    drivetrain.stop()
    drivetrain.drive_for(REVERSE, 100, MM)
    drivetrain.turn_for(RIGHT, 95, DEGREES)

    #Simple Debugging algorithm to see what goes wrong
def debug(curr_dist, past_dist, wall_dif):
    print("curr_dist = " + str(curr_dist))
    print("past_dist = " + str(past_dist))
    print("wall _dif = " + str(wall_dif))

def main():
    calibrate_drivetrain()
    #Set the speed of the robot
    drivetrain.set_drive_velocity(40, PERCENT)

    #Enter the maze
    drivetrain.drive(FORWARD)
    wait(0.7,SECONDS)
    drivetrain.stop()

    #Variables that update while in the while true
    curr_dist = 0
    past_dist = int(distance_8.object_distance(MM))
    time_since_last_change = 0
    adjust_count = 0

    while True:
        #Check if the bumpers are pressed
        front_left_bumper_pressing = bumper_e.pressing()
        front_right_bumper_pressing = bumper_d.pressing()
        bumper_pressed = front_left_bumper_pressing or front_right_bumper_pressing

        #Get the distance change along with the current distance
        curr_dist = int(distance_8.object_distance(MM))
        wall_dif = curr_dist - past_dist

        drivetrain.drive(FORWARD)

        debug(curr_dist, past_dist, wall_dif)

        #If we are hitting a wall in front of us do a right turn
        if(bumper_pressed):
            turn_right()
            time_since_last_change = 0
            curr_dist = int(distance_8.object_distance(MM))
            adjust_count = 0

        #If the left wall is too far away do a left turn
        elif(curr_dist > (past_dist + 75)):
            #turn_left()
            alt_turn_left()
            time_since_last_change = 0
            curr_dist = int(distance_8.object_distance(MM))
            adjust_count = 0

        #If the wall diffrence is below what is above and above 25 do a small adjust to drive somewhat straight
        elif(abs(wall_dif) > 25):
            #If we adjust three times in a row go forward
            if (adjust_count >= 3):
                adjust_count = 0
                drivetrain.drive(FORWARD)
                wait(0.5, SECONDS)
                drivetrain.stop()
            #Else adjust
            else:
                adjust(wall_dif)
                time_since_last_change = 0
                curr_dist = int(distance_8.object_distance(MM))
                adjust_count += 1

        #If we are stuck on something for long enough move
        #WAS never used
        elif(time_since_last_change > 1000):
            print("time change")
            drivetrain.turn_for(LEFT, 90, DEGREES)
            adjust_count = 0

        #If we have a change in the distances reset last_time_change
        elif(curr_dist != past_dist):
            time_since_last_change = 0
            adjust_count = 0

        #Update the we did not move counter
        else:
            time_since_last_change += 1
        
        #Mark the old distance
        past_dis = curr_dist

main()