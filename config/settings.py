# Configuration settings for MQTT Broker
BROKER = "localhost"  # broker address
PORT = 1883
MQTT_CLIENT_ID = "hydraulic_rasberryPi"  # client ID for MQTT broker
DEVICE_ID = "hydraulic"

STATUS_TOPIC = f"status/{DEVICE_ID}"  # status topic for this device
RESPONSE_TOPIC = f"response/device/{DEVICE_ID}"  # response topic for this device
DIRECT_TOPIC = f"device/{DEVICE_ID}"  # direct messages to this device

NUM_CYLINDERS = 4  # number of cylinders

LWT_MESSAGE = f"offline due to error"  # last will and testament message
OFFLINE_MESSAGE = f"offline"  # message to send when device goes offline
ONLINE_MESSAGE = f"online"  # message to send when device comes online
# COMMAND_TOPIC = f"device/{DEVICE_ID}/command"  # command topic for this device
