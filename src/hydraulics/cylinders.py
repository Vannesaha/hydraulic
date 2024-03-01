import time
from config.settings import (
    RESPONSE_TOPIC,  # MQTT topic for responses
)


def set_hydraulic(mqtt_subscriber, cylinder, position):
    try:
        cylinder = int(cylinder)
        if not 0 <= cylinder <= 3:
            raise ValueError("Cylinder number must be between 0 and 3")
        position = int(position)
        if not 0 <= position <= 180:
            raise ValueError("Position must be between 0 and 180")

        # Move the cylinder
        move_cylinder(mqtt_subscriber, cylinder, position)

    except ValueError as e:
        error_message = f"Error: {e}"
        mqtt_subscriber.client.publish(
            RESPONSE_TOPIC, f"Error: {e}", qos=1
        )  # Publish the error message
        print("error_message: ", error_message)


def move_cylinder(mqtt_subscriber, cylinder_number, position):
    time.sleep(2)
    """
    Move the specified cylinder to the specified position.

    Parameters:
    cylinder_number (int): The number of the cylinder to move.
    position (int): The position to move the cylinder to.

    Returns:
    None
    """
    mqtt_subscriber.client.publish(
        RESPONSE_TOPIC,
        f"Cylinder: {cylinder_number} moving to position: {position}",
        qos=1,
    )
