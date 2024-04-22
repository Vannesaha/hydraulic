# mqtt_subscriber.py

# This code creates an MQTT subscriber that connects to an MQTT broker,
# subscribes to a topic, and handles messages on that topic.
# The messages are expected to contain commands to set the position of a hydraulic cylinder.
# The subscriber maintains a dictionary of Cylinder objects and uses the
# commands in the messages to operate the cylinders.

# Import necessary modules
from umqtt.simple import MQTTClient
from src.hydraulics.cylinders import Cylinder
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


# Define the MQTTSubscriber class
class MQTTSubscriber:
    def __init__(self):
        # Initialize MQTT client with device ID, broker, and port
        self.client = MQTTClient(DEVICE_ID, BROKER, PORT)
        # Set the last will message
        self.client.set_last_will(STATUS_TOPIC, LWT_MESSAGE, retain=True)
        # Initialize messages dictionary
        self.messages = {}
        # Initialize cylinders dictionary with Cylinder objects
        self.cylinders = {
            i: Cylinder(self, i, None) for i in range(4)
        }  # Create a dictionary of Cylinder objects for cylinders 0 to 3

    def on_connect(self):
        try:
            # Connect to the MQTT broker
            self.client.connect()
            print(f"Connected successfully to broker: {BROKER}.")
            # Set the callback function to handle messages
            self.client.set_callback(self.on_message)
            # Publish the online message
            self.client.publish(STATUS_TOPIC, ONLINE_MESSAGE, retain=True)
            # Subscribe to the set_cylinder_position topic
            self.client.subscribe(
                f"{DIRECT_TOPIC}/set_cylinder_position"
            )  # Subscribe to the correct topic
        except OSError:
            print("Connection failed.")

    def on_message(self, topic, msg):
        # Decode the topic and payload
        topic = topic.decode()  # Decode the topic to a string
        payload = msg.decode()
        # Store the message in the messages dictionary
        self.messages[topic] = payload
        # If the topic is set_cylinder_position, handle the message
        if (
            topic == f"{DIRECT_TOPIC}/set_cylinder_position"
        ):  # Check for the correct topic
            actions = payload.split(",")  # Split the payload into actions
            for action in actions:  # Loop through the actions
                command, value = action.split(
                    ":"
                )  # Split the action into command and value
                if command == "set_cylinder":
                    cylinder = int(value)  # Convert the value to an integer
                    print(f"Received on {topic}: set cylinder to {cylinder}")
                elif command == "set_position":
                    position = int(value)  # Convert the value to an integer
                    print(f"Received on {topic}: set position to {position}")
                    # Set the position of the specified cylinder
                    self.cylinders[cylinder].set_hydraulic(
                        position
                    )  # Set the position of the cylinder

                    # example of coming messagesto topic: device/hydraulic/set_cylinder_position:
                    # set_cylinder:2,set_position:180

                    # example how they will be printed:
                    # Received on device/hydraulic/set_cylinder_position: set cylinder to 2
                    # Received on device/hydraulic/set_cylinder_position: set position to 180

    def on_disconnect(self):
        try:
            # Publish the offline message
            self.client.publish(STATUS_TOPIC, OFFLINE_MESSAGE, retain=True)
            # Disconnect from the MQTT broker
            self.client.disconnect()
            print("Disconnected successfully.")
        except OSError:
            print("Disconnection failed.")

    def run(self):
        # print("Running MQTTSubscriber")  # Add this line
        # Connect to the MQTT broker and start handling messages
        self.on_connect()
        self.client.set_callback(self.on_message)
        while True:
            self.client.wait_msg()
        # Disconnect from the MQTT broker when done
        self.on_disconnect()
