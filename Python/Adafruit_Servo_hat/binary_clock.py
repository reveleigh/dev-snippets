from adafruit_servokit import ServoKit
import time
import datetime

kit = ServoKit(channels=16)

# Initialize Servos
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].angle = 0

# Define servo positions (place values) using separate dictionaries
servo_positions_hours = {16: 3, 8: 4, 4: 5, 2: 6, 1: 7}  
servo_positions_minutes = {32: 10, 16: 11, 8: 12, 4: 13, 2: 14, 1: 15}  

def set_servo_angles(value, servo_positions):
    """Sets servo angles based on the given value and servo positions."""
    for place_value, servo_index in servo_positions.items():
        bit_value = (value // place_value) % 2
        angle = 180 if bit_value == 1 else 0
        kit.servo[servo_index].angle = angle

def binary_counter():
    """Displays time in hours and minutes on servos, updating every 45 seconds."""
    last_update_time = time.time() - 45 

    while True:
        current_time = time.time()
        if current_time - last_update_time >= 45:
            now = datetime.datetime.now()  # Get the current time 
            print(f"Time: {now.hour:02}:{now.minute:02}")  # Print time in hh:mm format
            set_servo_angles(now.hour, servo_positions_hours)
            set_servo_angles(now.minute, servo_positions_minutes)
            last_update_time = current_time  # Update the last update time
        time.sleep(1)  

# Start the counter
binary_counter()
