#!/usr/bin/env python3
"""Notes
- The optical sensor needs to be called eye (or eye needs to be renamed in this scratch)
- the float casting around the hue fn is needed for the VEX linter
"""

### NOT FOR COPYING #############################
eye = None
LedStateType = None
printb = None
PRINTB_COLOR = None
PRINTB_FN = None
#################################################


### FN CODE BELOW ###############################
eye_light_enabled = False
# Color Constants
COLOR_RED = 0
COLOR_ORANGE = 1
COLOR_YELLOW = 2
COLOR_GREEN = 3
COLOR_TEAL = 4
COLOR_BLUE = 5
COLOR_PURPLE = 6
COLOR_PINK = 7

def convert_color(colour, to_constant=True, vexprint=True, verbose=0):
    # Make global variables available
    global COLOR_RED
    global COLOR_ORANGE
    global COLOR_YELLOW
    global COLOR_GREEN
    global COLOR_TEAL
    global COLOR_BLUE
    global COLOR_PURPLE
    global COLOR_PINK
    global PRINTB_FN
    # Print fn name to VEX screen
    if vexprint: printb(PRINTB_FN, "convert_color")
    # Initialize return variable
    return_value = None
    # Convert a hue to a color constant, or a color constant to a user-friendly name
    if to_constant:
        if colour >= 345 or colour < 15:
            return_value = COLOR_RED
        elif colour >= 15 and colour < 45:
            return_value = COLOR_ORANGE
        elif colour >= 45 and colour < 75:
            return_value = COLOR_YELLOW
        elif colour >= 75 and colour < 175:
            return_value = COLOR_GREEN
        elif colour >= 175 and colour < 195:
            return_value = COLOR_TEAL
        elif colour >= 195 and colour < 255:
            return_value = COLOR_BLUE
        elif colour >= 255 and colour < 285:
            return_value = COLOR_PURPLE
        elif colour >= 285 and colour < 345:
            return_value = COLOR_PINK
        else:
            print("ERROR: convert_color fn: Unknown hue value.")
    else:
        if colour == COLOR_RED:
            return_value = "red"
        elif colour == COLOR_ORANGE:
            return_value = "orange"
        elif colour == COLOR_YELLOW:
            return_value = "yellow"
        elif colour == COLOR_GREEN:
            return_value = "green"
        elif colour == COLOR_TEAL:
            return_value = "teal"
        elif colour == COLOR_BLUE:
            return_value = "blue"
        elif colour == COLOR_PURPLE:
            return_value = "purple"
        elif colour == COLOR_PINK:
            return_value = "pink"
        else:
            print("ERROR: convert_color fn: Unknown color constant.")
    # Print debug information to the terminal
    if verbose != 0:
        print("- convert_color fn ------")
        print("  Color: " + str(colour))
        print("  ToConst: " + str(to_constant))
        print("  Vexprint: " + str(vexprint))
        print("  Verbose: " + str(verbose))
        print("  Return: " + str(return_value))
        print("-------------------------")
    # Return the found value
    return

def get_color(vexprint=True, verbose=0):
    # Make global variables available
    global eye_light_enabled
    global PRINTB_FN
    global PRINTB_COLOR
    # Make sure the optical sensor's light has been enabled
    if not eye_light_enabled:
        eye.set_light(LedStateType.ON)
        eye_light_enabled = True
    # Print fn name to VEX screen
    if vexprint: printb(PRINTB_FN, "get_color")
    # Get the current color through an API call
    colour = float(eye.hue()) # Value in range 0 to 360
    # Convert the color value to a more understandable color name
    colour_constant = convert_color(colour) # One of the color constants
    # Print new color to VEX screen
    if vexprint: printb(PRINTB_COLOR, convert_color(colour_constant, False))
    # Print debug information to the terminal
    if verbose != 0:
        print("- get_color fn ----------")
        print("  Vexprint: " + str(vexprint))
        print("  Verbose: " + str(verbose))
        print("  Return:" + str(colour_constant))
        print("-------------------------")
    # Return the color constant
    return colour_constant
