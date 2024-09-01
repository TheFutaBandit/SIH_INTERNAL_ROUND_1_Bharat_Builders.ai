#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import ssl
import _thread
import json
import time


def on_connect(client, userdata, flags, rc):
    if rc == 0:    
        print("Connected with result code " + str(rc))
        client.subscribe("raspi/data")
    else:
        print("connection error")
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    doWithPayload(payload)


def doWithPayload(payloadmsg):
    print(f"{payloadmsg}")


def publishData():
    while True:
        inputVal = str(input())
        data = {"update" : f"{inputVal}"}
        client.publish("raspi/data", payload = json.dumps(data), qos=0, retain=False)
        print("data published: " + json.dumps(data))
        time.sleep(5)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs='./DEVICE_Certificates/rootCA.pem', certfile='./DEVICE_Certificates/certificate.pem.crt', keyfile='./DEVICE_Certificates/private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3cz6591mmwk24-ats.iot.ap-south-1.amazonaws.com", 8883, 60)
client.loop_start()

try:
    publishData()
except KeyboardInterrupt:
    print("stopped publishing")
    client.loop_stop()
    client.disconnect()

