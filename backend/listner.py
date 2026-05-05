from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import splunklib.client as client
import splunklib.results as results
from agent import analyze_event
from storage import add_alert, load_alerts

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

alerts_store = load_alerts()

# Rate limit control
last_processed = {}
COOLDOWN = 30  # seconds


# -------------------------
# Fetch logs safely
# -------------------------
def fetch_related_logs(ip):
    try:
        service = client.connect(
            host='localhost',
            port=8089,
            username='sawan',
            password='Fcrx7_1209'
        )

        query = f"search index=soc_logs ip={ip} | sort -_time | head 10"
        job = service.jobs.create(query)

        start = time.time()
        while not job.is_done():
            if time.time() - start > 10:
                print("Splunk query timeout")
                return []
            time.sleep(0.5)

        reader = results.ResultsReader(job.results())

        logs = []
        for item in reader:
            if isinstance(item, dict):
                logs.append(item.get("_raw", ""))

        return logs

    except Exception as e:
        print("Splunk error:", e)
        return []


# -------------------------
# ALERT RECEIVER
# -------------------------
@app.post("/splunk-alert")
async def receive_alert(request: Request):
    data = await request.json()

    print("\nALERT RECEIVED")

    result_data = data.get("result", {})

    raw_log = result_data.get("_raw", "")
    logs_from_alert = result_data.get("logs", [])
    ip = result_data.get("ip")

    print("Raw log:", raw_log)
    print("Logs from alert:", logs_from_alert)
    print("IP:", ip)

    if not ip:
        return {"status": "ignored"}

    # Rate limiting
    current_time = time.time()
    if ip in last_processed:
        if current_time - last_processed[ip] < COOLDOWN:
            print(f"Skipping duplicate alert for {ip}")
            return {"status": "skipped"}

    last_processed[ip] = current_time

    # Select log source
    if logs_from_alert:
        if isinstance(logs_from_alert, str):
            logs = [logs_from_alert]
        else:
            logs = logs_from_alert
        print("Using logs from alert")

    elif raw_log:
        logs = [raw_log]
        print("Using raw log")

    else:
        print("No logs in alert, fetching from Splunk")
        logs = fetch_related_logs(ip)

    # Filter meaningful logs
    if not any(
        any(keyword in log for keyword in [
        "FAILED",
        "CRITICAL",
        "ERROR",
        "SQL Injection",
        "XSS",
        "port scan",
        "Unauthorized",
        "Privilege",
        "upload",
        "command execution",
        "request rate"
    ])
    for log in logs
    ):
        print("Logs not relevant, ignoring")
        return {"status": "ignored"}

    print("\nRELATED LOGS:")
    for l in logs:
        print(l)

    # LLM analysis
    result = analyze_event(logs)

    print("\nAI ANALYSIS:")
    print(result)

    # Store for frontend
    alert_data = {
        "timestamp": time.time(),
        "raw_log": raw_log,
        "ip": ip,
        "logs": logs,
        "analysis": result
    }

    alerts_store[:] = add_alert(alert_data)

    return {"analysis": result}


# -------------------------
# GET ALERTS
# -------------------------
@app.get("/alerts")
async def get_alerts():
    return {"alerts": load_alerts()}

@app.get("/actions")
async def get_actions():
    return {"actions": {}}

@app.post("/trigger-alert")
async def trigger_alert():
    # Simulate an alert (e.g., use sample data)
    sample_alert = {
        "timestamp": time.time(),
        "raw_log": "Sample ERROR log",
        "ip": "192.168.1.100",
        "logs": ["INFO User login success ip=192.168.1.211",
    "INFO File accessed ip=192.168.1.20",
    "FAILED LOGIN user=admin ip=192.168.1.211",
    "FAILED LOGIN user=root ip=192.168.1.211",
    "FAILED LOGIN user=admin ip=192.168.1.211",
    "FAILED LOGIN user=sawan ip=192.168.1.211",
    "FAILED LOGIN user=sawan-warkar ip=192.168.1.211",
    "CRITICAL Possible brute force attack ip=192.168.1.211",
    "ERROR Unauthorized access attempt ip=192.168.1.50"],
        "analysis": {"threat_level": "Low", "attack_type": "Test", "summary": "Manual trigger", "recommended_action": "None"}
    }
    alerts_store[:] = add_alert(sample_alert)
    return {"status": "alert triggered"}