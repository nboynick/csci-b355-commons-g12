# Workplan for Friday

1. Run the test for the optimization of the timing delays for the servo motor.
2. Verify that the find_light_source() function is still working with the new added delta_angle
   and return_brightness parameters.
3. Verify if the drivetrain.turn_for() function is a blocking function or also requires a wait().
4. How to account for the different rotation centers of the optical_servo and the actual SquareBot
   when trying to figure out how far to turn?
5. 139+142: Can this wrapover to be negative? If the bot is rotated to 7*45 degrees and the servo is
   moved all the way to the right, will the delta_heading become more than 360 degrees?z