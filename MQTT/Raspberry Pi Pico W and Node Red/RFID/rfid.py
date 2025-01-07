from mfrc522 import MFRC522
from umqtt.simple import MQTTClient
from time import sleep
import network

reader = MFRC522(sck=2, mosi=3, miso=4, rst=5, cs=0)  # Adjust pin numbers if needed

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

SERVER = '192...'
CLIENT_ID = b'PICO'
TOPIC = b'rfid_status'
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
    


print("Bring TAG closer...")
print("")

while True:
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, raw_uid) = reader.anticoll()  # Get the UID first
        if stat == reader.OK:
            print("New card detected")
            print("  - tag type: 0x%02x" % tag_type)
            print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            print("")

            if reader.select_tag(raw_uid) == reader.OK:  # Select the tag using its UID
                card = int.from_bytes(bytes(raw_uid),"little",False)
                print("CARD ID: " + str(card))
                if card == 541511126515:
                    print("Card ID: " + str(card) + " PASS: Open door")
                    client.publish(TOPIC, "open")
                else:
                    print("Card ID: " + str(card) + " UNKNOWN CARD! Lock door")
                    client.publish(TOPIC, "close")
                    
    sleep(1)
