# A test script to detect whether all 16 servos are working or not
# using Adafruit 16-Channel 12-bit PWM/Servo Driver - I2C interface - PCA9685

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import time

for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)

while True:
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0
    kit.servo[2].angle = 0
    kit.servo[3].angle = 0
    kit.servo[4].angle = 0
    kit.servo[5].angle = 0
    kit.servo[6].angle = 0
    kit.servo[7].angle = 0
    kit.servo[8].angle = 0
    kit.servo[9].angle = 0
    kit.servo[10].angle = 0
    kit.servo[11].angle = 0
    kit.servo[12].angle = 0
    kit.servo[13].angle = 0
    kit.servo[14].angle = 0
    kit.servo[15].angle = 0
    time.sleep(1)
    kit.servo[0].angle = 180
    kit.servo[1].angle = 180
    kit.servo[2].angle = 180
    kit.servo[3].angle = 180
    kit.servo[4].angle = 180
    kit.servo[5].angle = 180
    kit.servo[6].angle = 180
    kit.servo[7].angle = 180
    kit.servo[8].angle = 180
    kit.servo[9].angle = 180
    kit.servo[10].angle = 180
    kit.servo[11].angle = 180
    kit.servo[12].angle = 180
    kit.servo[13].angle = 180
    kit.servo[14].angle = 180
    kit.servo[15].angle = 180
    time.sleep(1)
