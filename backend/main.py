from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import paho.mqtt.client as mqtt
import uvicorn
import json
import datetime
import threading

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/+/data"
DATABASE_URL = "sqlite:///./velesync.db"

# Database Setup
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SensorReading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    light = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

class DeviceCommand(BaseModel):
    device_id: str
    command: str

# FastAPI Setup
app = FastAPI(title="Velesync API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MQTT Client Logic
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        db = SessionLocal()
        new_reading = SensorReading(
            device_id=payload.get("device_id", "unknown"),
            temperature=payload.get("temperature", 0),
            humidity=payload.get("humidity", 0),
            light=payload.get("light", 0)
        )
        db.add(new_reading)
        db.commit()
        db.close()
    except Exception as e:
        print(f"MQTT Error: {e}")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message

def start_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.subscribe(MQTT_TOPIC)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")

# Start MQTT in background thread
mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
mqtt_thread.start()

# API Endpoints
@app.get("/api/current")
def get_current():
    db = SessionLocal()
    # Get latest reading for each device
    readings = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).limit(10).all()
    db.close()
    return readings

@app.get("/api/stats")
def get_stats():
    db = SessionLocal()
    total = db.query(SensorReading).count()
    active_devices = db.query(SensorReading.device_id).distinct().count()
    db.close()
    return {
        "total_readings": total,
        "active_devices": active_devices,
        "status": "online"
    }

@app.get("/api/history")
def get_history(limit: int = 50):
    db = SessionLocal()
    history = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).limit(limit).all()
    db.close()
    return history

@app.post("/api/telemetry")
def post_telemetry(reading: SensorReadingCreate):
    db = SessionLocal()
    db_reading = SensorReading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    db.close()
    return {"status": "persisted", "data": reading}

@app.post("/api/command")
def send_command(cmd: DeviceCommand):
    try:
        topic = f"sensors/{cmd.device_id}/commands"
        payload = json.dumps({"command": cmd.command})
        info = mqtt_client.publish(topic, payload)
        info.wait_for_publish()
        return {"status": "dispatched", "device": cmd.device_id, "command": cmd.command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
