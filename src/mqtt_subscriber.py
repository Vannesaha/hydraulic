import paho.mqtt.client as mqtt
from src.hydraulics.cylinders import set_position, set_position_all

from config.settings import (
    BROKER,  # MQTT broker address
    PORT,  # MQTT broker port
    STATUS_TOPIC,  # MQTT topic for status messages
    DIRECT_TOPIC,  # MQTT topic for direct messages
    LWT_MESSAGE,  # Last Will and Testament message
    OFFLINE_MESSAGE,  # Offline message
    MQTT_CLIENT_ID,  # Unique client identifier
    DEVICE_ID,  # Unique device identifier
    ONLINE_MESSAGE,  # Online message
    NUM_CYLINDERS,  # Number of cylinders
)


class MQTTSubscriber:
    def __init__(self):
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)
        self.client.will_set(STATUS_TOPIC, payload=LWT_MESSAGE, qos=1, retain=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.messages = {}  # Initialize the messages dictionary

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            client.publish(STATUS_TOPIC, f"{ONLINE_MESSAGE}", qos=1, retain=True)

            # Subscribe to topics for each cylinder
            for i in range(1, NUM_CYLINDERS + 1):
                client.subscribe(f"{DIRECT_TOPIC}/{i}", 0)

            # Subscribe to the 'all' topic
            client.subscribe(f"{DIRECT_TOPIC}/all", 0)
        else:
            print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received on {msg.topic}: {msg.payload.decode()}")
        payload = msg.payload.decode()
        self.messages[msg.topic] = (
            payload  # Update the messages dictionary with the new message
        )

        # Command parsing for 'set_position'
        if msg.topic.startswith(DIRECT_TOPIC):
            action, command = payload.split(":")
            if action == "set_position":
                if "all" in msg.topic:
                    position = int(command)
                    set_position_all(self, position)
                else:
                    cylinder = int(
                        msg.topic.split("/")[-1]
                    )  # Get the cylinder number from the topic
                    position = int(command)
                    set_position(self, cylinder, position)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    def run(self):
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()
            input("Press Enter to disconnect...\n")
        finally:
            self.client.publish(STATUS_TOPIC, OFFLINE_MESSAGE, retain=True)
            self.client.disconnect()
            self.client.loop_stop()
