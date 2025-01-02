import paho.mqtt.client as mqtt
import time

#####
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic = ", message.topic)
    print("message qos = ", message.qos)
    print("message retain flag = ", message.retain)

def on_log(client, userdata, level, buf):
    print("log: ", buf)
    
#####
    
broker_address="mqttpi.local"
print("Creating an instance")
client = mqtt.Client("P1") #Create an instance
client.on_message=on_message #attach function to callback
print("Connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.on_log=on_log
print("Subscribing to topic test")
client.subscribe("test")
print("Publishing a message to test topic")
client.publish("test","New message to check git working")#Publish
time.sleep(4)#Trust
client.loop_stop() #stop the loop
