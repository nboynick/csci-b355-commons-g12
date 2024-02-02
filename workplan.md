# Workplan for Friday

1. Run the test for the optimization of the timing delays for the servo motor.
2. Verify that the find_light_source() function is still working with the new added delta_angle
   and return_brightness parameters.
3. Verify if the drivetrain.turn_for() function is a blocking function or also requires a wait().
4. How to account for the different rotation centers of the optical_servo and the actual SquareBot
   when trying to figure out how far to turn?
5. 139+142: Can this wrap-over to be negative? If the bot is rotated to 7*45 degrees and the servo is
   moved all the way to the right, will the delta_heading become more than 360 degrees?
6. Check the length of the SquareBot in order to know how far to drive forward in the avoid_obstacle
   method to fully clear an obstacle.
7. Check the optical.object_detected() method, so that the distance sensor in the callback function
   does not eroneousely consider a detected object as being far enough away to not be considered an
   obstacle and thus not cause a new callback from the optical sensor when we get closer.
   --> Maybe use the callback function provided by the bumper sensor instead?