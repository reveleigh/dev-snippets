from adafruit_servokit import ServoKit
import time
import datetime

kit = ServoKit(channels=16)

# Initialize Servos 
for i in range(16):
    kit.servo[i].actuation_range = 180
    kit.servo[i].set_pulse_width_range(500, 2500)
    kit.servo[i].angle = 0

# Define servo positions (place values) for hours and minutes
servo_positions = {
    "hours": {8: 3, 4: 4, 2: 5, 1: 6},
    "minutes": {32: 10, 16: 11, 8: 12, 4: 13, 2: 14, 1: 15}
}

def set_servo_angles(value, time_unit):
    """Sets servo angles based on the given time value (hour or minute)."""
    for place_value, servo_index in servo_positions[time_unit].items():
        bit_value = (value // place_value) % 2
        angle = 180 if bit_value == 1 else 0
        kit.servo[servo_index].angle = angle

def binary_clock():
    """Displays time in hours and minutes on servos, updating every second."""
    last_hour = -1  
    last_minute = -1

    while True:
        now = datetime.datetime.now()
        hour_12 = now.hour % 12  

        # Check if either hour or minute has changed
        if hour_12 != last_hour or now.minute != last_minute:
            print(f"Time: {hour_12:02}:{now.minute:02}")  

        # Update servos (even if the time hasn't changed for a visual refresh)
        set_servo_angles(hour_12, "hours")
        set_servo_angles(now.minute, "minutes")

        last_hour = hour_12
        last_minute = now.minute
        time.sleep(1)  

# Start the binary clock
binary_clock()
