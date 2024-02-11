#!/usr/bin/env python3
"""Notes
- The distance sensor needs to be called radar (or radar needs to be renamed in this scratch)
"""

### NOT FOR COPYING #############################
radar = None
PRINTB_FN = None
PRINTB_DISTANCE = None
unit = None
printb = None
MM = None
#################################################


### FN CODE BELOW ###############################
def get_distance(unit=MM, vexprint=True, verbose=0):
    # Make global variables available
    global PRINTB_FN
    global PRINTB_DISTANCE
    # Print fn name to VEX screen
    if vexprint: printb(PRINTB_FN, "get_distance")
    # Call the VEX API to get the distance
    separation = radar.object_distance(unit)
    # Print distance to VEX screen
    if vexprint: printb(PRINTB_DISTANCE, separation)
    # Print debug information to the terminal
    if verbose != 0:
        print("- get_distance fn -------")
        print("  Unit: " + str(unit))
        print("  Vexprint: " + str(vexprint))
        print("  Verbose: " + str(verbose))
        print("  Separation: " + str(separation))
        print("-------------------------")
    # Return the recorded value
    return separation
