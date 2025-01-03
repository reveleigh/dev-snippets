from machine import Pin, ADC
from time import sleep
from umqtt.simple import MQTTClient
import network

# LED Pin
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

SERVER = '192...' # Broker Address (Change to the IP address of your Pi)
CLIENT_ID = b'PICO'
TOPIC = b'led_state'
USER = b'user'
PASSWORD = b'password'

# Function to connect to the MQTT broker
def on_message(topic, msg):
    print("Received message:", msg.decode())
    if msg == b'on':
        led.value(1)
    elif msg ==b'off':
        led.value(0)

# Function to connect to the MQTT broker
def main(server, topic, username, passw):
    client = MQTTClient(CLIENT_ID,
                        SERVER,
                        user=username,
                        password = passw,
                        keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    print('Connected to %s, subscribed to %s topic' % (server, topic))

    try:
        while True:
            client.wait_msg()
    finally:
        client.disconnect()
        
# Call the main function   
main(SERVER, TOPIC, USER, PASSWORD)


