# Task 8: Real-Time Data Streaming Dashboard

## Objective

The objective of this task is to build a real-time data streaming system that ingests live sensor data, processes it using statistical techniques, and visualizes it on a browser dashboard using WebSockets.

---

## Features

* Real-time sensor data simulation using asynchronous streams
* Moving average computation using pandas
* Anomaly detection using z-score
* WebSocket-based communication for live updates
* Interactive dashboard with real-time charts (Chart.js)
* Status classification: NORMAL, WARNING, CRITICAL

---

## Project Structure

```plaintext id="k4d2p9"
task-8/
│
├── server.py
├── dashboard.html
├── requirements.txt
```

---

## Prerequisites

* Python 3.x
* Basic understanding of WebSockets and asynchronous programming

---

## Installation

Install required dependencies:

```bash id="g8t3q1"
pip install -r requirements.txt
```

---

## How to Run

### Step 1: Start the Server

```bash id="p2m7x9"
python -m uvicorn server:app --reload
```

---

### Step 2: Open Dashboard

Open the following file in your browser:

```plaintext id="y9f4r2"
dashboard.html
```

---

## Output

### Server Console

```plaintext id="t6n1c8"
[INFO] Stream started at http://localhost:8000
[INFO] Client connected

[14:05:31] temp=72.3 avg=75.1 status=NORMAL
[14:05:32] temp=73.1 avg=75.3 status=NORMAL
[14:05:33] temp=89.7 avg=78.4 status=WARNING
[14:05:34] temp=104.2 avg=82.4 status=CRITICAL
```

---

### Real-Time Processing

```plaintext id="v8k5d3"
Moving Average (window-based):
- Continuously updated using recent data points

Z-Score Calculation:
- Detects anomalies based on deviation from mean

Status Logic:
- NORMAL → within safe range
- WARNING → abnormal deviation (z-score > 2)
- CRITICAL → exceeds threshold (>100)
```

---

### Dashboard Output (Browser)

* Live updating temperature chart
* Real-time status display
* Smooth streaming updates every second

---

### Output Screenshot

![Live Demo](vid.mp4)

---

## Key Concepts Used

* Asynchronous programming with asyncio
* WebSockets for real-time communication
* Streaming data processing
* Moving averages and statistical anomaly detection
* Frontend visualization using Chart.js

---

## What I Learned

This task helped in understanding:

* How real-time data pipelines work
* Handling streaming data with async generators
* Using statistical methods for anomaly detection
* Building interactive dashboards with live updates
* Integrating backend and frontend in real time

---

## Conclusion

This real-time dashboard demonstrates how live data can be processed and visualized efficiently. It reflects real-world applications such as IoT monitoring systems, industrial analytics, and real-time alerting systems.
