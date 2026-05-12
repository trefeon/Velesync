import time
import json
import random
import requests
try:
    import paho.mqtt.client as mqtt
    HAS_MQTT = True
except ImportError:
    HAS_MQTT = False

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
HTTP_API = "http://localhost:8000/api/telemetry"
DEVICE_ID = "velesync-node-01"
TOPIC = "sensors/data"

mqtt_client = None
if HAS_MQTT:
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to Velesync MQTT Broker")
        else:
            print(f"MQTT Connection failed with code {rc}")

    try:
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqtt_client.on_connect = on_connect
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 5)
        mqtt_client.loop_start()
    except Exception:
        print("MQTT Broker unavailable. Switching to HTTP Direct Injection mode.")
        mqtt_client = None

def send_data(payload):
    # Try MQTT first if available
    if mqtt_client:
        try:
            mqtt_client.publish(TOPIC, json.dumps(payload))
            return "MQTT"
        except Exception:
            pass
    
    # Fallback to HTTP
    try:
        response = requests.post(HTTP_API, json=payload, timeout=2)
        if response.status_code == 200:
            return "HTTP"
    except Exception as e:
        return f"Error: {e}"
    return "Failed"

print(f"Starting Velesync Device Simulation for {DEVICE_ID}...")
print(f"Mode: {'Hybrid (MQTT+HTTP)' if mqtt_client else 'Direct HTTP (Demo Mode)'}")
print("Press Ctrl+C to stop.")

base_temp = 24.5
base_humi = 45.0

try:
    while True:
        temp = round(base_temp + random.uniform(-0.5, 0.5), 2)
        humi = round(base_humi + random.uniform(-1.0, 1.0), 1)
        light = random.randint(300, 800)

        payload = {
            "device_id": DEVICE_ID,
            "temperature": temp,
            "humidity": humi,
            "light": light
        }

        method = send_data(payload)
        print(f"[{method}] Sent: Temp={temp}°C, Humi={humi}%, Light={light}lx")
        
        base_temp += random.uniform(-0.05, 0.05)
        base_humi += random.uniform(-0.1, 0.1)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulation stopped.")
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
except Exception as e:
    print(f"Global Simulation Error: {e}")

