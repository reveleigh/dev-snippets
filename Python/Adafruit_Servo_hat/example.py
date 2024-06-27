# This script tests the functionality of 16 servos connected to an
# Adafruit PCA9685 PWM driver by moving them between 0 and 180 degrees.
from adafruit_servokit import ServoKit
import time

# Initialize ServoKit with 16 channels
kit = ServoKit(channels=16)

# Set up servo parameters (optional, depends on your servos)
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)

# Main loop
while True:
    for angle in (0, 180):  # Move servos between 0 and 180 degrees
        for i in range(16):
            kit.servo[i].angle = angle
            time.sleep(0.1)  # Short pause for smoother movement

        time.sleep(1)  # Pause for 1 second at each position

    # Feedback
    print("Servos moved successfully to", angle, "degrees.")
