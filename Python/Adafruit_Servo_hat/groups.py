# This script tests groups of servos connected to an Adafruit PCA9685
# by sequentially moving each group between 0 and 180 degrees.
#
# Servo groups are defined as tuples (start_index, end_index), representing
# the range of servo channels that belong to the group. In this example,
# we have three groups:
#   - Group 1: Servos 0 to 7
#   - Group 2: Servos 8 to 15
# 
# The script iterates through each group, setting the angle of all servos
# within that group simultaneously before moving to the next.
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)

# Define servo groups (start index, end index)
groups = [(0, 7), (6, 15)]

while True:
    for angle in (0, 180):
        for start, end in groups:
            for i in range(start, end + 1):  
                kit.servo[i].angle = angle
            time.sleep(0.3)  # Pause between group movements

        # Feedback
        print(f"Servos in group {start}-{end} moved successfully to {angle} degrees.") 
