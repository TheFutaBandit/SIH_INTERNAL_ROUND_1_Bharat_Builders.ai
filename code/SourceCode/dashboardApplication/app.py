import streamlit as st
import datetime
import time
import pandas as pd
import json
import paho.mqtt.client as mqtt
import ssl
import threading
import asyncio

# AWS IoT configuration
ENDPOINT = "a3cz6591mmwk24-ats.iot.ap-south-1.amazonaws.com"
PORT = 8883
PUBLISH_TOPIC =  "raspi/data"
SUBSCRIBE_TOPIC = "raspi/data"
PATH_TO_CERT = '../DEVICE_Certificates/certificate.pem.crt'
PATH_TO_KEY = '../DEVICE_Certificates/private.pem.key'
PATH_TO_ROOT = '../DEVICE_Certificates/rootCA.pem'

# Initialize session state
if 'alarms' not in st.session_state:
    st.session_state.alarms = []
if 'received_data' not in st.session_state:
    st.session_state.received_data = []
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        st.success("Connected to AWS IoT")
        client.subscribe(SUBSCRIBE_TOPIC)
    else:
        st.error(f"Failed to connect, return code {rc}")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    st.session_state.received_data.append(payload)

def init_mqtt():
    if st.session_state.mqtt_client is None:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        client.on_message = on_message

        # Configure TLS/SSL
        client.tls_set(ca_certs=PATH_TO_ROOT, certfile=PATH_TO_CERT, keyfile=PATH_TO_KEY, tls_version=ssl.PROTOCOL_TLSv1_2)
        client.tls_insecure_set(True)

        # Connect to AWS IoT Core
        try:
            client.connect(ENDPOINT, PORT, 60)
            client.loop_start()
            st.session_state.mqtt_client = client
        except Exception as e:
            st.error(f"Failed to connect to AWS IoT: {str(e)}")

def publish_to_aws_iot(data):
    if st.session_state.mqtt_client:
        message = json.dumps(data)
        result = st.session_state.mqtt_client.publish(PUBLISH_TOPIC, message, qos=1)
        if result.rc == 0:
            st.success(f"Published to AWS IoT: {message}")
        else:
            st.error(f"Failed to publish message")
    else:
        st.error("MQTT client not initialized")

def main():
    st.title("Alarm App with AWS IoT Integration")

    # Initialize MQTT client
    init_mqtt()

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Set Alarm", "Alarm List", "Received Data", "Settings"])

    if page == "Set Alarm":
        set_alarm_page()
    elif page == "Alarm List":
        alarm_list_page()
    elif page == "Received Data":
        received_data_page()
    elif page == "Settings":
        settings_page()

def set_alarm_page():
    st.header("Set New Alarm")
    alarm_time = st.time_input("Set alarm time")
    alarm_name = st.text_input("Alarm name")
    if st.button("Set Alarm"):
        new_alarm = {"action": "set_alarm", "time": str(alarm_time), "message": alarm_name, "display" : "1"}
        st.session_state.alarms.append(new_alarm)
        publish_to_aws_iot(new_alarm)
        st.success(f"Alarm set for {alarm_time}")

def alarm_list_page():
    st.header("Your Alarms")
    for idx, alarm in enumerate(st.session_state.alarms):
        st.write(f"{alarm['name']} - {alarm['time']}")
        if st.button(f"Delete Alarm {idx}"):
            deleted_alarm = st.session_state.alarms.pop(idx)
            publish_to_aws_iot({"action": "delete", "alarm": deleted_alarm})
            st.experimental_rerun()

def received_data_page():
    st.header("Received Data from Raspberry Pi")
    if st.session_state.received_data:
        for data in st.session_state.received_data:
            st.json(data)
    else:
        st.write("No data received yet.")

def settings_page():
    st.header("Settings")
    st.write("AWS IoT Configuration:")
    st.write(f"Endpoint: {ENDPOINT}")
    st.write(f"Port: {PORT}")
    st.write(f"Publish Topic: {PUBLISH_TOPIC}")
    st.write(f"Subscribe Topic: {SUBSCRIBE_TOPIC}")

if __name__ == "__main__":
    main()