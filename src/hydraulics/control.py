# control.py
# Importing Cylinder class from the cylinders module in the hydraulics package
from src.hydraulics.cylinders import Cylinder


# Defining a class named HydraulicDevice
class HydraulicDevice:
    # The constructor method for the HydraulicDevice class
    def __init__(self, mqtt_subscriber):
        # Initializing an attribute named cylinders
        # It is a list of Cylinder objects
        # Each Cylinder object is initialized with an mqtt_subscriber, an index, and a gpio_pin
        # The index and gpio_pin are determined by the position of the Cylinder object in the list
        # The gpio_pin is 10 more than the index
        self.cylinders = [
            Cylinder(mqtt_subscriber, i, gpio_pin=i + 10) for i in range(4)
        ]
