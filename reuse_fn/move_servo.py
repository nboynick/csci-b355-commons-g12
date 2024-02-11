#!/usr/bin/env python3
"""Notes
- set_position fn is non blocking, i.e. you have to use a wait VEX API call to ensure it has
  finished moving
- The servo motor needs to be called servo (or motor needs to be renamed in this scratch)
"""

### NOT FOR COPYING #############################
servo = None
DEGREES = None
printb = None
PRINTB_FN = None
PRINTB_SERVO = None
PERCENT = None
wait = None
MSEC = None
#################################################


### FN CODE BELOW ###############################
servo_position = 0

def move_servo(new_position, unit=DEGREES, vexprint=True, verbose=False):
    # Make global variables available
    global servo_position
    global PRINTB_FN
    global PRINTB_SERVO
    # Print fn name to VEX screen
    if vexprint: printb(PRINTB_FN, "move_servo")
    # Adjust new servo position value
    if unit == PERCENT:
        new_servo_position = new_position - 50
    else:
        new_servo_position = new_position
    # Check for valid servo position values
    if new_servo_position < -50 or new_servo_position > 50:
        print("Error: move_servo: New position value outside of range of servo.")
    # Make VEX API call to move the servo
    fn_call = servo.set_position(new_servo_position, DEGREES)
    # Wait for the servo to finish moving
    wait_time = ((abs(servo_position - new_servo_position) / 100) * 620) + 10
    wait(wait_time, MSEC)
    # Update servo position
    servo_position = new_servo_position
    # Print new servo position to VEX screen
    if vexprint: printb(PRINTB_SERVO, new_servo_position)
    # Print debug information to the terminal
    if verbose != 0:
        print("- move_servo fn ---------")
        print("  NewPos: " + str(new_position))
        print("  Unit: " + str(unit))
        print("  Vexprint: " + str(vexprint))
        print("  Verbose: " + str(verbose))
        print("  NewServoPos: " +str(new_servo_position))
        print("-------------------------")
    return None # Python default return

def delta_move_servo(delta_angle, vexprint=True, verbose=False):
    # Make global variables available
    global servo_position
    global PRINTB_FN
    # Print fn name to VEX screen
    if vexprint: printb(PRINTB_FN, "delta_move_servo")
    # New/Adjusted servo position
    new_servo_position = servo_position + delta_angle
    # Make local API call
    move_servo(new_servo_position)
    # Print debug information to the terminal
    if verbose != 0:
        print("- delta_move_servo fn ---")
        print("  DeltaAngle: " + str(delta_angle))
        print("  Vexprint: " + str(vexprint))
        print("  Verbose: " + str(verbose))
        print("  NewServoPos: " + str(new_servo_position))
        print("-------------------------")
    return None # Python default return
