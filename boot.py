# boot.py -- run on boot-up

# Import necessary modules
import network, utime, machine

# Replace the following with your WIFI Credentials
SSID = "ssid"
SSID_PASSWORD = "pass"


# Define a function to connect to the WiFi
def do_connect():
    # Create a station interface
    sta_if = network.WLAN(network.STA_IF)
    # Check if the station interface is not connected
    if not sta_if.isconnected():
        print("connecting to network...")
        # Activate the station interface
        sta_if.active(True)
        # Connect to the WiFi using SSID and password
        sta_if.connect(SSID, SSID_PASSWORD)
        # Keep trying to connect until a connection is established
        while not sta_if.isconnected():
            print("Attempting to connect....")
            # Sleep for 1 second before trying again
            utime.sleep(1)
    # Print the network configuration once connected
    print("Connected to wifi! Network config:", sta_if.ifconfig())


# Print a message indicating the start of the connection process
print("Connecting to your wifi...")
# Call the function to connect to the WiFi
do_connect()
