import time
import json
import random
import paho.mqtt.client as mqtt

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
DEVICE_ID = "velesync-node-01"
TOPIC = "sensors/data"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to Velesync Broker")
    else:
        print(f"Connection failed with code {rc}")

# Setup MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    print(f"Starting Velesync Device Simulation for {DEVICE_ID}...")
    print("Press Ctrl+C to stop.")

    base_temp = 24.5
    base_humi = 45.0

    while True:
        # Simulate neural-like fluctuations
        temp = round(base_temp + random.uniform(-0.5, 0.5), 2)
        humi = round(base_humi + random.uniform(-1.0, 1.0), 1)
        light = random.randint(300, 800)

        payload = {
            "device_id": DEVICE_ID,
            "temperature": temp,
            "humidity": humi,
            "light": light
        }

        client.publish(TOPIC, json.dumps(payload))
        print(f"Sent: Temp={temp}°C, Humi={humi}%, Light={light}lx")
        
        # Slow drift
        base_temp += random.uniform(-0.05, 0.05)
        base_humi += random.uniform(-0.1, 0.1)

        time.sleep(3)

except KeyboardInterrupt:
    print("\nSimulation stopped.")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"Simulation Error: {e}")
