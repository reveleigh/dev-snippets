# -------------------------------------------- # 
#        Imports and general config            #
# -------------------------------------------- #

from cotswolds import towns # Import the towns list from cotswolds.py

from machine import Pin # Import the Pin class from the machine module
import utime
import random
from neopixel import Neopixel # Import the Neopixel class from the neopixel module
from umqtt.simple import MQTTClient # Import the MQTTClient class from the umqtt.simple module
import network # Import the network module
import _thread # Import the _thread module

# Configure Neopixels
numpix = 145
strip = Neopixel(numpix, 0, 22, "GRB")
strip.brightness(200)

# -------------------------------------------- #
#        MQTT and WiFi Configuration           #
# -------------------------------------------- #

# WIFI Credentials
SSID = "Wi Fi Fo Fum"
PASSWORD = "Isaacleavethecandlesalone"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print("Connected to WiFi")
print(wlan.ifconfig())

#Setup MQTT
SERVER = '192.168.68.55'
CLIENT_ID = b'PICO'
TOPIC = b'dijkstra'
USER = b'russell'
PASSWORD = b'Nr1216719543'

client = MQTTClient(CLIENT_ID,
                    SERVER,
                    user=USER,
                    password=PASSWORD,
                    keepalive=3600)

client.connect()

# Global variable, flag to indicate if the button has been pressed
GO = False

# Create a lock
lock = _thread.allocate_lock()

# -------------------------------------------- #
#        Dijkstras Algorithm                   #
# -------------------------------------------- #

# Function to fade towns by criteria
def fade(type, town, start_town=None, end_town=None):
    # Don't fade the start and end towns
    if town != start_town and town != end_town and start_town != None:
        # All the fade in options
        if type == "in":
            if town.visited: # Bright red if visited
                start_r, start_g, start_b = 255, 0, 0  
            else:
                start_r, start_g, start_b = 10, 0, 0
            end_r, end_g, end_b = 255, 255, 255  # Current town is white
        # All the fade out options
        elif type == "out": # Fade out to red
            start_r, start_g, start_b = 255, 255, 255
            if town.visited:
                end_r, end_g, end_b = 255, 0, 0
            else:
                end_r, end_g, end_b = 10, 0, 0
        elif type == "neighbour_in" and not town.visited:
            start_r, start_g, start_b = 10, 0, 0
            end_r, end_g, end_b = 255, 0, 0
        elif type == "neighbour_out" and not town.visited:
            start_r, start_g, start_b = 255, 0, 0
            end_r, end_g, end_b = 10, 0, 0
    elif type == "terminal":
        start_r, start_g, start_b = 10, 0, 0
        end_r, end_g, end_b = 255, 255, 255
    else:
        return

    steps = 50  # Number of steps in the fade
    delay = 0.02  # Delay between each step (in seconds)

    for i in range(steps + 1):
        # Calculate the current RGB values for this step
        r = int(start_r + (end_r - start_r) * (i / steps))
        g = int(start_g + (end_g - start_g) * (i / steps))
        b = int(start_b + (end_b - start_b) * (i / steps))

        for led in town.leds:
            strip[led] = (r, g, b)
        strip.show()
        utime.sleep(delay)

# Function to pick two different random towns
def pick_towns(towns):
    town1 = random.choice(towns)
    town2 = random.choice(towns)
    while town2 == town1:
        town2 = random.choice(towns)
    return town1, town2

# Function to get the euclidean distance between two towns when given x and y coordinates of each
def get_distance(town1, town2):
    return ((town1.x - town2.x) ** 2 + (town1.y - town2.y) ** 2) ** 0.5

# Function to get the town with the smallest distance that has not been visited
def get_smallest_distance(towns):
    smallest_distance = 9999
    smallest_town = None
    for town in towns:
        if not town.visited and town.distance < smallest_distance:
            smallest_distance = town.distance
            smallest_town = town
    return smallest_town

# Function to turn all lights off
def turn_off():
    for i in range(numpix):
        strip[i] = (0, 0, 0)
    strip.show()

def printTownNames(towns):
    for town in towns:
        print(town)
        utime.sleep(1)

# -------------------------------------------- #
#        MQTT Callbacks                        #
# -------------------------------------------- #

# Thread to handle incoming messages
def sub_cb(topic, msg):
    global GO
    # Get lock
    lock.acquire()
    if msg == b'start':
        GO = True
        print("Start")
    elif msg == b'stop':
        GO = False
        print("Stop")
    # Release lock
    lock.release()

client.set_callback(sub_cb)
client.subscribe(TOPIC)
print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC))


def start_dijkstras():
    while True:
        printTownNames(towns)


# Start threads for MQTT and Dijkstras
_thread.start_new_thread(start_dijkstras, ())
print("Started D thread")


# Main loop
while True:
    client.check_msg()


