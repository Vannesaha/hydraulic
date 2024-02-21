import time
from config.settings import (
    RESPONSE_TOPIC,  # MQTT topic for responses
)


def set_position(client, payload):
    _, cylinder_str, position_str = payload.split(":")
    try:
        cylinder = int(cylinder_str)
        position = int(position_str)
        if not 1 <= cylinder <= 4:
            raise ValueError("Cylinder number must be between 1 and 4")
        if not 1 <= position <= 100:
            raise ValueError("Position must be between 1 and 100")

        # time out for the cylinder to move
        time.sleep(2)
        print(f"Cylinder: {cylinder} set to position: {position}")
        # Actual control logic to set the cylinder's position
        client.publish(
            RESPONSE_TOPIC, f"Cylinder: {cylinder} set to position: {position}"
        )
    except ValueError as e:
        error_message = f"Error: {e}"
        client.publish(RESPONSE_TOPIC, f"Error: {e}")  # Publish the error message
        print("error_message: ", error_message)
