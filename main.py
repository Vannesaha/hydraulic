# main.py

# Import the MQTTSubscriber class from src.mqtt_client module
from src.mqtt_subscriber import MQTTSubscriber

# from src.hydraulics.cylinders import Cylinder
# from src.hydraulics.control import HydraulicDevice


# Define the main function
def main():
    # Create an instance of MQTTSubscriber
    subscriber = MQTTSubscriber()
    # Run the MQTT subscriber
    subscriber.run()

    # Create a list of cylinders
    # subscriber.hydraulic_device = HydraulicDevice(subscriber)


# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    main()
