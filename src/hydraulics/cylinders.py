# Importing the time module
import time

# Importing the RESPONSE_TOPIC constant from the settings module in the config package
from config.settings import (
    RESPONSE_TOPIC,  # MQTT topic for responses
)


# Defining a class named Cylinder
class Cylinder:
    # The constructor method for the Cylinder class
    def __init__(self, mqtt_subscriber, cylinder_number, gpio_pin):
        # Initializing the mqtt_subscriber, cylinder_number, and gpio_pin attributes
        self.mqtt_subscriber = mqtt_subscriber
        self.cylinder_number = cylinder_number
        # self.gpio_pin = gpio_pin

    # Method to set the position of the hydraulic cylinder
    def set_hydraulic(self, position):
        try:
            # Convert the position to an integer
            position = int(position)
            # If the position is not between 0 and 180, raise a ValueError
            if not 0 <= position <= 180:
                raise ValueError("Position must be between 0 and 180")

            # Move the cylinder to the specified position
            self.move_cylinder(position)

        except ValueError as e:
            # If a ValueError is raised, publish an error message to the RESPONSE_TOPIC
            error_message = f"Error: {e}"
            self.mqtt_subscriber.client.publish(
                RESPONSE_TOPIC, error_message.encode(), qos=1
            )  # Publish the error message
            print("error_message: ", error_message)

    # Method to move the cylinder to a specified position
    def move_cylinder(self, position):
        # Sleep for 2 seconds
        time.sleep(2)
        """
        # Set the mode of the GPIO
        GPIO.setmode(GPIO.BOARD)
        # Set up the gpio_pin as an output
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        # Start PWM on the gpio_pin at 50Hz
        pwm = GPIO.PWM(self.gpio_pin, 50)  # GPIO for PWM at 50Hz
        pwm.start(0)

        # Convert the position to a duty cycle
        duty_cycle = position / 18 + 2  # Convert position to duty cycle
        # Output a high signal on the gpio_pin
        GPIO.output(self.gpio_pin, True)
        # Change the duty cycle
        pwm.ChangeDutyCycle(duty_cycle)
        # Sleep for 1 second
        time.sleep(1)
        # Output a low signal on the gpio_pin
        GPIO.output(self.gpio_pin, False)
        # Change the duty cycle to 0
        pwm.ChangeDutyCycle(0)
        """
        # Publish a message to the RESPONSE_TOPIC indicating the cylinder number and the position it is moving to
        self.mqtt_subscriber.client.publish(
            RESPONSE_TOPIC,
            f"Cylinder: {self.cylinder_number} moving to position: {position}",
            qos=1,
        )
