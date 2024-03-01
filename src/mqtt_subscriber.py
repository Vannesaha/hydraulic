# Importing the mqtt client from the paho.mqtt package
import paho.mqtt.client as mqtt

# Importing the HydraulicDevice class from the control module in the hydraulics package
from src.hydraulics.control import HydraulicDevice

# Importing constants from the settings module in the config package
from config.settings import (
    BROKER,  # MQTT broker address
    PORT,  # MQTT broker port
    STATUS_TOPIC,  # MQTT topic for status messages
    DIRECT_TOPIC,  # MQTT topic for direct messages
    LWT_MESSAGE,  # Last Will and Testament message
    OFFLINE_MESSAGE,  # Offline message
    DEVICE_ID,  # Unique device identifier
    ONLINE_MESSAGE,  # Online message
)


# Defining a class named MQTTSubscriber
class MQTTSubscriber:
    # The constructor method for the MQTTSubscriber class
    def __init__(self):
        # Initializing the client attribute as an MQTT client with the DEVICE_ID as the client_id
        self.client = mqtt.Client(client_id=DEVICE_ID)
        # Setting the Last Will and Testament message for the client
        self.client.will_set(STATUS_TOPIC, payload=LWT_MESSAGE, qos=1, retain=True)
        # Setting the on_connect, on_message, and on_disconnect methods as the corresponding callback methods for the client
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        # Initializing the messages attribute as an empty dictionary
        self.messages = {}  # Initialize the messages dictionary
        # Initializing the hydraulic_device attribute as a HydraulicDevice object
        self.hydraulic_device = HydraulicDevice(mqtt_subscriber=self)

    # Method to be called when the client connects to the broker
    def on_connect(self, client, userdata, flags, rc):
        # Subscribing the client to the DIRECT_TOPIC
        client.subscribe(DIRECT_TOPIC)
        if rc == 0:
            # If the connection was successful, print a success message and publish an online message to the STATUS_TOPIC
            print("Connected successfully.")
            client.publish(STATUS_TOPIC, f"{ONLINE_MESSAGE}", qos=1, retain=True)

            # Subscribe to topics for each cylinder
            for i in range(0, 3 + 1):
                client.subscribe(f"{DIRECT_TOPIC}/{i}", 0)
        else:
            # If the connection was not successful, print the result code
            print(f"Connected with result code {rc}")

    # Method to be called when a message is received by the client
    def on_message(self, client, userdata, msg):
        # Decoding the payload of the message
        payload = msg.payload.decode()
        # Updating the messages dictionary with the new message
        self.messages[msg.topic] = (
            payload  # Update the messages dictionary with the new message
        )
        # If the topic of the message starts with DIRECT_TOPIC and the payload contains a colon
        if msg.topic.startswith(DIRECT_TOPIC) and ":" in payload:
            # Split the payload into action and command
            action, command = payload.split(":")
            # If the action is 'set_hydraulic'
            if action == "set_hydraulic":
                # Get the cylinder number from the topic of the message
                cylinder = int(msg.topic.split("/")[-1])
                # Convert the command to an integer
                position = int(command)
                # Set the position of the specified cylinder
                self.hydraulic_device.cylinders[cylinder].set_hydraulic(position)
                # Print the topic and payload of the message
                print(f"Received on {msg.topic}: {msg.payload.decode()}")

    # Method to be called when the client disconnects from the broker
    def on_disconnect(self, client, userdata, rc):
        # If the disconnection was not clean, print a message
        if rc != 0:
            print("Unexpected disconnection.")

    # Method to run the MQTTSubscriber
    def run(self):
        try:
            # Connect the client to the broker and start the network loop
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()
            # Wait for the user to press Enter to disconnect
            input("Press Enter to disconnect...\n")
        finally:
            # Publish an offline message to the STATUS_TOPIC, disconnect the client from the broker, and stop the network loop
            self.client.publish(STATUS_TOPIC, OFFLINE_MESSAGE, qos=1, retain=True)
            self.client.disconnect()
            self.client.loop_stop()
