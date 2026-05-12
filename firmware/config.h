#ifndef CONFIG_H
#define CONFIG_H

// ====== WIFI CONFIGURATION ======
#define WIFI_SSID "YOUR_WIFI_NETWORK_NAME"
#define WIFI_PASS "YOUR_WIFI_PASSWORD"

// ====== MQTT CONFIGURATION ======
#define MQTT_HOST "192.168.1.100" // Update to your server IP
#define MQTT_PORT 1883
#define DEVICE_ID "velesync-node-01"

// ====== SENSOR CONFIGURATION ======
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define LIGHT_SENSOR_PIN 34
#define LED_PIN 2

// ====== TIMING ======
#define SENSOR_INTERVAL 5000 // 5 seconds
#define MQTT_RECONNECT_INTERVAL 5000

#endif
