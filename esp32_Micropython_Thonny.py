import network
import time
import random
from umqtt.simple import MQTTClient
import json

# --- WiFi Credentials ---
WIFI_SSID = "Eiz_4TX_Net"
WIFI_PASSWORD = "e_20I02_z"

# --- MQTT Configuration ---
MQTT_SERVER = "broker.hivemq.com"
MQTT_TOPIC_SUB = b"esp32/detections"
MQTT_TOPIC_PUB = b"esp32/status"
MQTT_PORT = 1883

# Global variables
wlan = None
mqtt_client = None

def setup_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print("Connecting to", WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Wait for connection
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        time.sleep(0.5)
        print(".", end="")
        timeout -= 1
    
    if wlan.isconnected():
        print("\nWiFi connected")
        print("IP address:", wlan.ifconfig()[0])
        return True
    else:
        print("\nFailed to connect to WiFi")
        return False

def mqtt_callback(topic, msg):
    print("Message received on topic [{}]: {}".format(topic.decode(), msg.decode()))
    
    message = msg.decode()
    print("Object detection result:", message)
    
    # You can add actions here based on detected objects
    if "person" in message.lower():
        print("Person detected! Taking action...")
    elif "car" in message.lower():
        print("Car detected!")
    elif "cat" in message.lower():
        print("Cat detected!")
    elif "bird" in message.lower():
        print("Bird detected!")
    # Add more conditions as needed

def reconnect_mqtt():
    global mqtt_client
    client_id = "esp32-123456" + str(random.getrandbits(16))
    
    try:
        mqtt_client = MQTTClient(client_id, MQTT_SERVER, port=MQTT_PORT)
        mqtt_client.set_callback(mqtt_callback)
        mqtt_client.connect()
        mqtt_client.subscribe(MQTT_TOPIC_SUB)
        print("MQTT connected and subscribed to", MQTT_TOPIC_SUB.decode())
        
        # Send connection status
        mqtt_client.publish(MQTT_TOPIC_PUB, "ESP32 connected and ready")
        return True
    except Exception as e:
        print("MQTT connection failed:", e)
        return False

def main():
    # Setup WiFi
    if not setup_wifi():
        return
    
    # Setup MQTT
    if not reconnect_mqtt():
        print("Failed to connect to MQTT broker")
        return
    
    print("Starting main loop...")
    last_status_time = time.time()
    
    # Main loop
    while True:
        try:
            # Check MQTT messages
            mqtt_client.check_msg()
            
            # Send status update every 30 seconds
            if time.time() - last_status_time > 30:
                mqtt_client.publish(MQTT_TOPIC_PUB, "ESP32 online")
                last_status_time = time.time()
                print("Status update sent")
            
            time.sleep(0.1)
            
        except Exception as e:
            print("Error in main loop:", e)
            print("Attempting to reconnect...")
            time.sleep(5)
            
            # Reconnect if connection is lost
            if not wlan.isconnected():
                setup_wifi()
            
            try:
                if not mqtt_client or not mqtt_client.isconnected():
                    reconnect_mqtt()
            except:
                pass

# Run the program
if __name__ == "__main__":
    main()