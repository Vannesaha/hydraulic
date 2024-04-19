# mqtt_subscriber.py

from umqtt.simple import MQTTClient

from src.hydraulics.control import HydraulicDevice
from config.settings import (
    BROKER,
    PORT,
    STATUS_TOPIC,
    DIRECT_TOPIC,
    LWT_MESSAGE,
    OFFLINE_MESSAGE,
    DEVICE_ID,
    ONLINE_MESSAGE,
)


class MQTTSubscriber:
    def __init__(self):
        self.client = MQTTClient(DEVICE_ID, BROKER, PORT)
        self.client.set_last_will(STATUS_TOPIC, LWT_MESSAGE, retain=True)
        self.messages = {}
        self.hydraulic_device = HydraulicDevice(mqtt_subscriber=self)

    def on_connect(self):
        try:
            self.client.connect()
            print("Connected successfully.")
            self.client.set_callback(self.on_message)  # Set the callback function
            self.client.publish(STATUS_TOPIC, ONLINE_MESSAGE, retain=True)
            for i in range(0, 3 + 1):
                self.client.subscribe(f"{DIRECT_TOPIC}/{i}")
        except OSError:
            print("Connection failed.")

    def on_message(self, topic, msg):
        payload = msg.decode()
        self.messages[topic] = payload
        if topic.startswith(DIRECT_TOPIC) and ":" in payload:
            action, command = payload.split(":")
            if action == "set_hydraulic":
                cylinder = int(topic.split("/")[-1])
                position = int(command)
                self.hydraulic_device.cylinders[cylinder].set_hydraulic(position)
                print(f"Received on {topic}: {payload.encode()}")

    def on_disconnect(self):
        try:
            self.client.publish(STATUS_TOPIC, OFFLINE_MESSAGE, retain=True)
            self.client.disconnect()
            print("Disconnected successfully.")
        except OSError:
            print("Disconnection failed.")

    def run(self):
        self.on_connect()
        self.client.set_callback(self.on_message)
        while True:
            self.client.wait_msg()
        self.on_disconnect()
