from machine import ADC, Pin 
import utime 
import json # Importing the JSON library
from umqtt.simple import MQTTClient
import network

adc_x = ADC(26)
adc_y = ADC(27)

button = Pin(17,  Pin.IN, Pin.PULL_UP)

#WIFI Credentials 
SSID = "ssid"
PASSWORD = "pass"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print("Connected to WiFi")
print(wlan.ifconfig())

SERVER = '192....'
CLIENT_ID = b'PICO'
TOPIC = b'joystick'
USER = b'user'
PASSWORD = b'pass'

def mqtt_connect():
    client = MQTTClient(CLIENT_ID, SERVER, user=USER, password = PASSWORD, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker' % (SERVER))
    return client

def reconnect():
    print("Failed to connect to MQTT Broker. Reconnecting...")
    sleep(5)
    machine.reset()

try:
    client = mqtt_connect() 
except OSError as e:
    reconnect()

while True:
    x = adc_x.read_u16() # Reading the x-axis value
    y = adc_y.read_u16() # Reading the y-axis value
    
    btn_state = button.value() # Reading the button state
    
    # Creating a dictionary to store the data
    data = {
        'x_value': x,
        'y_value': y,
        'button_value': 'Pressed' if btn_state == 0 else 'Not Pressed'
        }
    
    print('X:', x, 'Y:', y, 'Button:', 'Pressed' if btn_state == 0 else 'Not Pressed')
    
    # Converting the dictionary to a JSON string
    data_json = json.dumps(data)
    print(data_json)

    # Publishing the JSON string to the MQTT broker
    client.publish(TOPIC, data_json)
    
    utime.sleep(0.25)
