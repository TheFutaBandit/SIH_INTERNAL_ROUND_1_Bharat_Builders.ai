## Tasks Accomplished

- [x] **Core Functionality:** Implemented a Raspberry Pi with a 1.44" LCD hat to display the set alarm time. The Raspberry Pi subscribes to MQTT topics from AWS IoT Core to receive alarm time updates, which are triggered by a button click in the Streamlit app.
- [x] **Cloud Integration:** Configured AWS IoT Core for MQTT-based communication between the Streamlit app and the Raspberry Pi. Set up an AWS IoT Core rule that triggers an AWS Lambda function to process incoming alarm messages and store them in a database.
- [x] **Dashboard/Mobile-App Integration:** Developed a Streamlit app that serves as a dashboard for alarm management. The app publishes MQTT messages to AWS IoT Core which is received by the RaspberryPi subscribed to the same topic.

## Technology Stack

This project leverages the following technologies:

- **[aws-iot-core](https://aws.amazon.com/iot-core/):** Selected for its reliable MQTT-based communication and device management, AWS IoT Core facilitates the interaction between the Streamlit app and the Raspberry Pi by handling message publishing and subscribing.

- **[Streamlit](https://streamlit.io/):** Chosen for its simplicity and rapid development capabilities, Streamlit is used to create a web-based dashboard for alarm management, allowing us to set alarms.

- **[aws-lambda](https://aws.amazon.com/lambda/):** AWS Lambda processes incoming messages from AWS IoT Core and performs operations such as storing alarm data in a database.

- **[raspberrypi](https://www.raspberrypi.org/):** Raspberry Pi acts as the core device to display the alarm time on a 1.44" LCD hat and execute commands received via AWS IoT Core.

## Key Features

- **Feature 1:** Remote Alarm Setup; Set alarms remotely using Streamlit Applicationo using MQTT communication with AWS IoT Core.
- **Feature 2:** Real-Time Data Display; Displays the set alarm time on a 1.44" LCD hat connected to a Raspberry Pi, ensuring real-time updates and visualization.


## Local Setup Instructions (Write for both windows and macos)

Follow these steps to run the project locally

1. **Clone the Repository**
   ```bash
   git clone GITHUB_LINK_TO_THE_REPO
   cd SIH_INTERNAL_ROUND_1_Bharat_Builders.ai/code/SourceCode/dashboardApplication
   ```

Important Pre-requisites:
```bash
pip3 install streamlit
pip install paho-mqtt
```

