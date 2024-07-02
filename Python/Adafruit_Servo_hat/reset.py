## Set all 16 servos to 0 degrees

from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)

for i in range(16):
    kit.servo[i].angle = 0
    time.sleep(0.1)  # Short pause for smoother movement