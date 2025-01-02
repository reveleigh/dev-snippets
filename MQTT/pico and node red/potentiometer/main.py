# Import necessary modules for GPIO control, 
# ADC, MQTT communication, and network handling
from machine import Pin, ADC
from time import sleep
from umqtt.simple import MQTTClient
import network

pot = ADC(26) # Create an ADC object for the potentiometer

#WIFI Credentials
SSID = "SSID"
PASSWORD = "PASS"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait until the connection is established
while not wlan.isconnected():
    pass

# Print connection details
print("Connected to WiFi")
print(wlan.ifconfig())

# MQTT Broker Details
SERVER = '192...' # Broker Address (Change to the IP address of your Pi)
CLIENT_ID = b'PICO' # Client ID
TOPIC = b'pot_guage' # Topic to publish to
USER = b'user' # MQTT Username
PASSWORD = b'password' # MQTT Password

# Function to connect to the MQTT broker
def mqtt_connect():
    # Create an instance of the MQTTClient
    client = MQTTClient(CLIENT_ID, SERVER, user=USER, password = PASSWORD, keepalive=3600)
    client.connect()

    # Print connection details
    print('Connected to %s MQTT Broker' % (SERVER))
    return client

# Function to reconnect to the MQTT broker
def reconnect():
    print("Failed to connect to MQTT Broker. Reconnecting...")
    sleep(5)
    machine.reset()

# Connect to the MQTT broker
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    
# Publish potentiometer values to the MQTT broker   
while True:
    value = pot.read_u16()
    client.publish(TOPIC,  str(value))
    print("Pot value = ", value)
    sleep(1.0)
    
    

