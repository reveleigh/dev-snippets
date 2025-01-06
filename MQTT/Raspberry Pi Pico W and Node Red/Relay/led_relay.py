from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

# Pin sending signal to relay
led = Pin(15, Pin.OUT)

#WIFI Credentials 
SSID = "SSID"
PASSWORD = "Pass"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print("Connected to WiFi")
print(wlan.ifconfig())

SERVER = '192...'
CLIENT_ID = b'PICO'
TOPIC = b'relay_control'
USER = b'user'
PASSWORD = b'pass'

def on_message(topic, msg):
    print("Received message:", msg.decode())
    if msg == b'on':
        led.value(1)
    elif msg == b'off':
        led.value(0)


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
    
main(SERVER, TOPIC, USER, PASSWORD)
