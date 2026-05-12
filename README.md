# 🌌 Velesync

> A premium, high-performance IoT intelligence platform for real-time sensor telemetry and neural visualization.

![Velesync Dashboard](https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=1000)

**Velesync** is a professional-grade IoT ecosystem designed to bridge the gap between raw hardware telemetry and high-fidelity intelligence. Utilizing a state-of-the-art **Glassmorphism** interface and a high-concurrency **FastAPI** backbone, Velesync provides a robust, scalable foundation for modern industrial, scientific, and smart-infrastructure deployments.

---

## 🛠️ Tech Stack (v2026.05 Stable)

Velesync utilizes a curated selection of high-performance technologies, pinned to their latest stable releases for maximum reliability:

### 🧠 Core Intelligence (Backend)
- **FastAPI (v0.136.1)**: Asynchronous, high-performance web framework for Python.
- **SQLAlchemy (v2.0.49)**: Professional-grade SQL toolkit and Object-Relational Mapper.
- **Paho-MQTT (v2.1.0)**: Industrial-standard MQTT client implementing `CallbackAPIVersion.VERSION2`.
- **Uvicorn (v0.46.0)**: Lightning-fast ASGI server implementation.

### 🌉 Neural Bridge (Infrastructure)
- **Eclipse Mosquitto (v2.1.2)**: Lightweight and scalable MQTT message broker.
- **Docker & Compose**: Containerized orchestration for deterministic deployments.
- **Nginx (v1.27.0-alpine)**: High-performance reverse proxy and static file server.

### 👁️ Visualization (Frontend)
- **Vanilla JS/CSS3**: Zero-dependency frontend logic for ultra-low latency.
- **Chart.js (v4.5.1)**: Premium, responsive charting with custom neural gradients.
- **Design System**: Custom Glassmorphism theme utilizing Deep Obsidian (`#0B0E14`) and Electric Cobalt (`#2E5BFF`).

---

## 🚀 Deployment & Usage

### 1. Rapid Deployment (Docker)
The recommended way to run Velesync is via Docker Compose. This initializes the entire stack—Backend, MQTT Broker, and Frontend—automatically.

```bash
# Clone and enter the repository
git clone https://github.com/your-username/velesync.git
cd velesync

# Launch the neural stack
docker-compose up -d --build
```

#### Access Points:
- **Intelligence Dashboard**: [http://localhost:80](http://localhost:80)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **MQTT Neural Bridge**: `localhost:1883`

### 2. Manual Development Setup
For local debugging or modification of the core intelligence:

```bash
# Setup Python environment
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows

# Install pinned dependencies
pip install -r requirements.txt

# Start the API
uvicorn main:app --reload --port 8000
```

### 3. Neural Simulation (Demo)
To instantly visualize the platform's capabilities without hardware:

**Option A: Browser Demo (No Setup)**
1. Open the dashboard at [http://localhost:80](http://localhost:80).
2. Click **"START DEMO MODE"** in the top navbar.
3. Observe real-time neural data generation and visualization.

**Option B: System-Wide Simulation (Full Stack Test)**
1. Ensure the stack is running via Docker.
2. Run the Python simulator:
   ```bash
   python scripts/simulate_device.py
   ```
3. This will broadcast live telemetry across the MQTT bridge, populating the real database and dashboard.

---

## 📡 Hardware Integration (Firmware)

Velesync is hardware-agnostic, supporting any device capable of MQTT. We recommend the following stable libraries for ESP32/Arduino development:

- **ArduinoJson (v7.4.3)**: For efficient neural packet serialization.
- **Adafruit DHT (v1.4.7)**: For precise environmental sensing.
- **PubSubClient (v2.8.0)**: For reliable MQTT synchronization.

### Payload Schema
Edge nodes should publish telemetry to the `sensors/[device_id]/data` topic using the following JSON structure:

```json
{
  "device_id": "velesync-node-01",
  "temperature": 24.5,
  "humidity": 45.2,
  "light": 320,
  "timestamp": 1715526000
}
```

---

## 🎨 Design Philosophy: Glassmorphism

Velesync utilizes a custom design system focused on **Visual Depth** and **Information Hierarchy**:

1.  **Deep Obsidian Base**: `#0B0E14` provides a high-contrast, professional background.
2.  **Electric Cobalt Accents**: `#2E5BFF` guides the user's eye to critical system updates.
3.  **Backdrop Fusion**: `backdrop-filter: blur(20px)` combined with subtle 1px white borders (8% opacity) creates a premium glass-panel effect.
4.  **Neural Gradients**: Real-time charts utilize multi-stop CSS gradients to visualize data trends with high fidelity.

---
*Velesync — Synchronizing the Future of IoT.*
