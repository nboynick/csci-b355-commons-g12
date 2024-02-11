#!/usr/bin/env python3
"""Notes
- The VEX brain needs to be called brain (or brain needs to be renamed in this scratch)
- The default VEX font allows for 5 rows, each at 16 characters
"""

### NOT FOR COPYING #############################
brain = None
#################################################


### FN CODE BELOW ###############################
brain_was_cleared = False
PRINTB_FN = 1
PRINTB_LENGTH = 2
PRINTB_COLOR = 3
PRINTB_INERTIAL = 4
PRINTB_MISC = 5
PRINTB_DISTANCE = -1
PRINTB_SERVO = -1

def printb(message_type, message, verbose=0):
    # Make global variables available
    global brain_was_cleared
    # Make sure any content not produced by this fn was cleared from the screen
    if not brain_was_cleared:
        brain.screen.clear_screen()
        brain_was_cleared = True
    # Clear the previous content from the needed row
    fn_call_1 = brain.screen.clear_row(message_type) # Should be None
    # Set the cursor to the start of the line
    fn_call_2 = brain.screen.set_cursor(message_type, 1) # Should be None
    # Print the message
    fn_call_3 = brain.screen.print(message) # Should be None
    # Print debug information to the terminal
    if verbose != 0:
        print("- printb fn -------------")
        print("  MessageType: " + str(message_type))
        print("  Message: " + str(message))
        print("  Verbose: " + str(verbose))
        print("  G BrainClear: " + str(brain_was_cleared))
        print("-------------------------")
    return None # Python default return
