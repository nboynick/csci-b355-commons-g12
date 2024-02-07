# Notes on the different Sensors/Motors

## Brain Inertial
- Needs to be calibrated at the beginning of each script to make a slew of other things function
  correctly. -> Run calibrate_inertial() at the beginning of each script.

## Optical
- The brightness() function has to be typecast to float() so that the linter does not throw a fit
  because the API is incorrectly defined.
- The brightness() function returns its values as a percentage in the range of (0,100).
- The object_detected() method does not seem to work as long as the scopes are attached to it.
- Has a light for better color recognition that has to be turned on.

## Servo
- set_position() is non blocking, i.e., you have to run a wait() afterwords for however long it will
  take the servo to have adjusted its position.
