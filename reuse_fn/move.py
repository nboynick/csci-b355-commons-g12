#!/usr/bin/env python3
"""Notes
- The drivetrain needs to be called motor (or motor in this scratch needs to be renamed)
- This fn requires the printb fn to be included
"""

### NOT FOR COPYING #############################
MM = None
FORWARDS = None
motor = None
printb = None
calibrate_drivetrain = None
PRINTB_FN = None
PRINTB_LENGTH = None
#################################################


### FN CODE BELOW ###############################
length = 0                             # Total distance traveled by the bot
drivetrain_has_been_calibrated = False # VEX calibrate_drivetrain fn has been run

def move(step_size=15, unit=MM, direction=FORWARDS, vexprint=True, verbose=0):
    # Make global variables available
    global length
    global drivetrain_has_been_calibrated
    global PRINTB_FN
    global PRINTB_LENGTH
    # Check that the drivetrain was calibrated (and is ready for use)
    if not drivetrain_has_been_calibrated:
        calibrate_drivetrain()
        drivetrain_has_been_calibrated = True
    # Print fn name to VEX screen
    if vexprint: printb(PRINTB_FN, "move")
    # Call the VEX API
    fn_call = motor.drive_for(direction, step_size, unit) # Should be None
    # Update distance traveled
    length += step_size
    # Print new distance to VEX screen
    if vexprint: printb(PRINTB_LENGTH, length)
    # Print debug information to the terminal
    if verbose != 0:
        print("- move fn ---------------")
        print("  StepSize: " + str(step_size))
        print("  Unit: " + str())
        print("  Direction: " + str(direction))
        print("  Vexprint: " + str(vexprint))
        print("  Verbose: " + str(verbose))
        print("  G Length: " + str(length))
        print("  G DriveCalib: " + str(drivetrain_has_been_calibrated))
        print("-------------------------")
    return None # Python default return
