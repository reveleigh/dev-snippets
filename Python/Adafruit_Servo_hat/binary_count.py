from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

# Initialize Servos
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].angle = 0

# Define servo positions (place values)
servo_places = [128, 64, 32, 16, 8, 4, 2, 1, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

def binary_counter():
    """Increments the servo angles to represent a binary counter with the specified servo order."""

    counter = 0
    while True:
        for servo_index in range(16):  # Iterate through servo indices directly
            place_value = servo_places[servo_index]  # Get the place value for this servo
            bit_value = (counter // place_value) % 2  # Get the bit value (0 or 1)
            angle = 180 if bit_value == 1 else 0  # Set angle based on bit value
            kit.servo[servo_index].angle = angle  # Set servo angle

        time.sleep(1)  # Adjust delay for desired counting speed
        counter = (counter + 1) % 65536  # Increment and reset the counter

# Start the counter
binary_counter()
