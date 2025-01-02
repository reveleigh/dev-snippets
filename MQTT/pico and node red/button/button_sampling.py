from machine import Pin, ADC
from time import sleep
from umqtt.simple import MQTTClient
import network

# Button Pin 
button = Pin(14,Pin.IN, Pin.PULL_UP)

#WIFI Credentials 
SSID = "SSID"
PASSWORD = "PASSWORD"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait until the connection is established
while not wlan.isconnected():
    pass
#   Print connection details
print("Connected to WiFi")
print(wlan.ifconfig())

#  MQTT Broker Details
SERVER = '192...'# Broker Address (Change to the IP address of your Pi)
CLIENT_ID = b'PICO'
TOPIC = b'button_state'
USER = b'user'
PASSWORD = b'password'

# Function to connect to the MQTT broker
def mqtt_connect():
    client = MQTTClient(CLIENT_ID, SERVER, user=USER, password = PASSWORD, keepalive=3600)
    client.connect()
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

# Publish button state to the MQTT broker 
# Samples the button state every second
while True:
    if button.value():
        print("Pressed")
        client.publish(TOPIC, "1")
    else:
        print("Unpressed")
        client.publish(TOPIC, "0")
    sleep(1)
        
    
    


