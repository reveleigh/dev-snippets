from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

led = Pin(15, Pin.OUT)

#WIFI Credentials 
SSID = "SSID"
PASSWORD = "PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print("Connected to WiFi")
print(wlan.ifconfig())

#Setup MQTT
SERVER = '192....'
CLIENT_ID = b'PICO'
TOPIC_LED = b'led_state'
TOPIC_BUTTON = b'button_state'
USER = b'user'
PASSWORD = b'password'

client = MQTTClient(CLIENT_ID,
                    SERVER,
                    user=USER,
                    password=PASSWORD,
                    keepalive=3600)

client.connect()

def button_callback(pin):
    if button.value():
        print("pressed")
        client.publish(TOPIC_BUTTON, "1")
    else:
        print("Unpressed")
        client.publish(TOPIC_BUTTON, "0")

button = Pin(14, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
           handler=button_callback)

def led_callback(topic, msg):
    print("Received message:", msg.decode())
    if msg == b'on':
        led.value(1)
    elif msg == b'off':
        led.value(0)
        
client.set_callback(led_callback)
client.connect()
client.subscribe(TOPIC_LED)
print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC_LED))

while True:
    client.wait_msg()
    




