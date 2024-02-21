# Import the MQTTSubscriber class from src.mqtt_client module
from src.mqtt_subscriber import MQTTSubscriber


# Define the main function
def main():
    # Create an instance of MQTTSubscriber
    subscriber = MQTTSubscriber()
    # Run the MQTT subscriber
    subscriber.run()


# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    main()
