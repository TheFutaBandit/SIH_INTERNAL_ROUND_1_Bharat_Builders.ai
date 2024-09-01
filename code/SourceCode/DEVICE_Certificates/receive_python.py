
import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))
    # Subscribe to the topic
    client.subscribe("raspi/commands")  # Replace with your topic

def on_message(client, userdata, msg):
    # This function will be called when a message is received
    print(f"Message received from topic {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3cz6591mmwk24-ats.iot.ap-south-1.amazonaws.com", 8883, 60)

client.loop_forever()  # Keeps the client loop running to receive messages
