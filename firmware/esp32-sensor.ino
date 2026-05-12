#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include "config.h"

// Initialize sensors
DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient mqtt(espClient);

// Timing variables
unsigned long lastSensorRead = 0;
unsigned long lastMqttReconnect = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("\n🌌 Velesync Node - Active");
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(LIGHT_SENSOR_PIN, INPUT);
  dht.begin();
  
  connectWiFi();
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(onMqttMessage);
  
  Serial.println("✅ Setup complete!");
  Serial.printf("📡 Device ID: %s\n", DEVICE_ID);
}

void loop() {
  if(WiFi.status() != WL_CONNECTED) connectWiFi();
  
  if(!mqtt.connected() && millis() - lastMqttReconnect > MQTT_RECONNECT_INTERVAL) {
    connectMqtt();
    lastMqttReconnect = millis();
  }
  
  mqtt.loop();
  
  if(millis() - lastSensorRead > SENSOR_INTERVAL) {
    readAndSendSensorData();
    lastSensorRead = millis();
  }
  delay(100);
}

void connectWiFi() {
  Serial.printf("🔌 Connecting to WiFi: %s", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  
  int attempts = 0;
  while(WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi connected!");
  } else {
    Serial.println("\n❌ WiFi connection failed!");
  }
}

void connectMqtt() {
  if(WiFi.status() != WL_CONNECTED) return;
  
  Serial.printf("🔗 Connecting to MQTT: %s:%d", MQTT_HOST, MQTT_PORT);
  
  if(mqtt.connect(DEVICE_ID)) {
    Serial.println("\n✅ MQTT connected!");
    String commandTopic = "sensors/" + String(DEVICE_ID) + "/commands";
    mqtt.subscribe(commandTopic.c_str());
    sendDeviceStatus(true);
  } else {
    Serial.printf("\n❌ MQTT failed, rc=%d\n", mqtt.state());
  }
}

void readAndSendSensorData() {
  if(!mqtt.connected()) return;
  
  Serial.println("📊 Reading sensors...");
  
  // Read DHT22 sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Read light sensor (LDR)
  int lightRaw = analogRead(LIGHT_SENSOR_PIN);
  float lightLevel = map(lightRaw, 0, 4095, 0, 1000); // Convert to lux approximation
  
  // Check if readings are valid
  if(isnan(temperature) || isnan(humidity)) {
    Serial.println("❌ Failed to read from DHT sensor!");
    return;
  }
  
  // Create JSON payload
  StaticJsonDocument<200> doc;
  doc["device_id"] = DEVICE_ID;
  doc["temperature"] = round(temperature * 10) / 10.0;  // Round to 1 decimal
  doc["humidity"] = round(humidity * 10) / 10.0;
  doc["light"] = round(lightLevel);
  doc["timestamp"] = millis();
  doc["wifi_rssi"] = WiFi.RSSI();
  
  String payload;
  serializeJson(doc, payload);
  
  // Publish to MQTT
  String topic = "sensors/" + String(DEVICE_ID) + "/data";
  if(mqtt.publish(topic.c_str(), payload.c_str())) {
    Serial.printf("📤 Data sent: %s\n", payload.c_str());
    
    // Quick LED flash to indicate data sent
    digitalWrite(LED_PIN, HIGH);
    delay(50);
    digitalWrite(LED_PIN, LOW);
    
  } else {
    Serial.println("❌ Failed to send data!");
  }
}

void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  String message;
  for(int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.printf("📨 Received command: %s\n", message.c_str());
  
  // Parse JSON command
  StaticJsonDocument<100> doc;
  deserializeJson(doc, message);
  
  String command = doc["command"];
  
  if(command == "led_on") {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("💡 LED turned ON");
  }
  else if(command == "led_off") {
    digitalWrite(LED_PIN, LOW);
    Serial.println("💡 LED turned OFF");
  }
  else if(command == "status") {
    sendDeviceStatus(true);
  }
  else if(command == "restart") {
    Serial.println("🔄 Restarting device...");
    ESP.restart();
  }
  else {
    Serial.printf("❓ Unknown command: %s\n", command.c_str());
  }
}

void sendDeviceStatus(bool online) {
  if(!mqtt.connected()) return;
  
  StaticJsonDocument<150> doc;
  doc["device_id"] = DEVICE_ID;
  doc["status"] = online ? "online" : "offline";
  doc["uptime"] = millis();
  doc["free_heap"] = ESP.getFreeHeap();
  doc["wifi_rssi"] = WiFi.RSSI();
  
  String payload;
  serializeJson(doc, payload);
  
  String topic = "sensors/" + String(DEVICE_ID) + "/status";
  mqtt.publish(topic.c_str(), payload.c_str(), true); // Retained message
  
  Serial.printf("📡 Status sent: %s\n", online ? "online" : "offline");
}

// Send offline status before restart/shutdown
void __attribute__((destructor)) cleanup() {
  sendDeviceStatus(false);
}
