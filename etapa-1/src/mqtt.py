import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions

from time import time
from random import randint

broker_address = "localhost"
broker_port = 1883
client_id = f"valkyrie_{randint(0, 1000)}-{int(round(time() * 1000))}"
qos = 2

def on_connect(client, userdata, flags, reasonCode, properties=None):
    if reasonCode == 0:
        print("Connected to MQTT Broker!")

        # Avoid receiving messages sent by the server itself
        options = SubscribeOptions(qos=qos, noLocal=True)
        client.subscribe("valkyrie/+", options=options )
    else:
        print(f"Failed to connect, return code {reasonCode}\n")

def on_disconnect(client, userdata, reasonCode):
    print(f"Disconnected with result code: {reasonCode}")

client = mqtt.Client(client_id, userdata=None, protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(host=broker_address, port=broker_port)