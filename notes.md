# Programming Hints for the VEX robotics materials

## Micropython Generals
- No enumerate function
- No f-strings, use `"%s" % str(variable)` instead
- ??? Incorrect usage of global variables (variables have to be globalized even if they are only
  being read)

## Brain Inertial
- Has to be calibrated before giving back useful date -> `brain_inertial.calibrate()`
  - This is a non-blocking function, that takes about two seconds to complete -> add an appropriate
    await/while-check-loop
- Gives (rather) accurate orientation readings for the VEX brain

## Motors
- Remember rotation direction of motor does not always align with tires due to inversion through
  the gears

### Drivetrain
- The distance calculation of the drivetrain only works if the VEX brain inertial sensor has been
  calibrated
- For sensor processing feedback to arrive at a useful speed, the velocity has to be around/less
  than 3%
- Drifting can occur due to imbalance in the two/four motors used for the drivetrain
- Can use both drive-for-distance and toggle driving
- Keep in mind `drivetrain.temperature(PERCENT)`
- `drivetrain.turn_for()` will only rotate at a minimum delta of 4-5 degrees

## Optical
- `brightness()` fn has to be float typecast due to linter
- `hue()` fn has to be float typecast due to linter
- `brightness()` fn returns a percentage in range (0,100), not (0.0,1.0)
- Cannot detect objects with a scope (both short or long) attached
- Has a built in light for better color detection (`optical.set_light(LedStateType.ON)`)

## Distance
- Does not have a callback fn
- Max recognizable distance is around 7.5 inches (~190MM)

## Servo
- `servo.set_position()` is non-blocking -> run `wait()` afterwards to insure it has finished the
  operation
- Only takes absolute positions in (-50, 50) -> maintain global variable to enable delta movements
- Positioning not as accurate as the potentiometer
- Single degree changes do not always work

## Potentiometer
- Range between (0°, 330°), safe range between (0°, 320°)
- 150° is considered straight forward
