# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Creed, Augie, Nathaniel                                      #
# 	Created:      1/23/2024, 12:39:54 PM                                       #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #


# Library imports
from vex import *
# Brain should be defined by default
brain=Brain()
# Robot configuration code
brain_inertial = Inertial()
right_bumper = Bumper(brain.three_wire_port.a)
left_bumper = Bumper(brain.three_wire_port.b)
right_motor = Motor(Ports.PORT5, False)
left_motor = Motor(Ports.PORT1, True)
light_sensor = Optical(Ports.PORT3)
distance_sensor = Distance(Ports.PORT8)
# Wait for sensor(s) to fully initialize
wait(100, MSEC)


# Begin project code
import random

### Part 0: Testing the Brain Code
# print("Hello World!")
# while True:
#     if right_bumper.pressing():
#         right_motor.spin(FORWARD)
#     else:
#         right_motor.stop()
#     if left_bumper.pressing():
#         left_motor.spin(FORWARD)
#     else:
#         left_motor.stop()

### Part 1: Hailstone Numbers
# def hailstone(n):
#     """Function to return the next number in the hailstone sequence based on the provided number.

#     :param n: The provided number
#     :type n: int
#     :returns: The next number in the sequence
#     :rtype: int
#     """
#     if (n % 2 == 0): # i.e. "if even"
#         n = (n / 2)
#         return(n)
#     else:
#         n = 3 * n + 1
#         return(n)

# n = 7
# while n > 1:
#     temp = hailstone(n)
#     print(temp)
#     n = temp


### Part 2: Light-Controlled Motor
# while True:
#     """Loop that continually adjusts the motor velocity based on the input from the light sensor."""
#     # Start the motors spinning forward.
#     right_motor.spin(FORWARD)
#     left_motor.spin(FORWARD)
#     # Obtain the brightness level from the light sensor
#     temp = float(light_sensor.brightness()) # float is needed and will work, bug in the brightness
#                                             # method definition
#     # Update the velocity of the two motors based on the brightness level
#     right_motor.set_velocity(temp, PERCENT)
#     left_motor.set_velocity(temp, PERCENT)

### Part 3: Anticipatory Obstacle Avoidance
while True:
    """Loop that continues moving forward while avoiding bumping into objects.
    
    The robot will obtain information if an object is in front of it, based on the the distance
    sensor. And will then turn in a random direction right/left by at least 30 degress and at
    most 180 degrees.
    """
    # Start the two motors moving forwards
    right_motor.spin(FORWARD)
    left_motor.spin(FORWARD)

    # Obtain the distance to the closest object
    distance_away = float(distance_sensor.object_distance(MM))

    # If the distance is closer than 10 centimeters, then...
    if distance_away < 110.0:
        # Stop and back away from the object to give the robot space to turn
        right_motor.spin(REVERSE)
        left_motor.spin(REVERSE)
        wait(0.8, SECONDS)

        # Default to turning 30 degrees left if there is an issue with the random number
        spin_direction = -30
        # Obtain a random turning angle that is between 30 and 180 degrees
        while True:
            spin_direction = random.randint(-180, 180)
            if (abs(spin_direction) > 30):
                break
        
        # Spin the robot based on the rotation angle
        if spin_direction < 0:
            right_motor.spin(FORWARD)
        else:
            left_motor.spin(FORWARD)
        wait((abs(spin_direction)/180) * 1.4, SECONDS)
