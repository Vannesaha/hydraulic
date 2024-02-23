import time
from config.settings import (
    RESPONSE_TOPIC,  # MQTT topic for responses
    NUM_CYLINDERS,  # Number of cylinders
)


def set_position(mqtt_subscriber, cylinder, position):
    try:
        cylinder = int(cylinder)
        position = int(position)
        if not 1 <= position <= 100:
            raise ValueError("Position must be between 1 and 100")

        # Move the cylinder
        move_cylinder(mqtt_subscriber, cylinder, position)

    except ValueError as e:
        error_message = f"Error: {e}"
        mqtt_subscriber.client.publish(
            RESPONSE_TOPIC, f"Error: {e}", qos=1
        )  # Publish the error message
        print("error_message: ", error_message)


def set_position_all(mqtt_subscriber, position):
    try:
        position = int(position)
        if not 1 <= position <= 100:
            raise ValueError("Position must be between 1 and 100")

        for cylinder_number in range(1, NUM_CYLINDERS + 1):
            move_all_cylinders(mqtt_subscriber, cylinder_number, position)

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


def move_all_cylinders(mqtt_subscriber, cylinder_number, position):
    time.sleep(0.5)
    """
    Move all cylinders to the specified position.

    Parameters:
    position (int): The position to move the cylinders to.

    Returns:
    None
    """
    mqtt_subscriber.client.publish(
        RESPONSE_TOPIC,
        f"Cylinder: {cylinder_number} set to position: {position}",
        qos=1,
    )
