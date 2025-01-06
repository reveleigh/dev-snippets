from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

slide = Pin(14, Pin.IN, Pin.PULL_DOWN)

def check_slide():
    if slide.value():
        print("Right")
        client.publish(TOPIC, "true")
    else:
        print("Left")
        client.publish(TOPIC, "false")

def slideswitch_callback(pin):
    check_slide()
    
slide.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=slideswitch_callback)


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

SERVER = '192...')
CLIENT_ID = b'PICO'
TOPIC = b'slide_switch'
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
    
check_slide()

while True:
    pass
