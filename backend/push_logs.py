import requests
import time
import random

HEC_URL = "http://localhost:8088/services/collector"
HEC_TOKEN = "677d83f2-a52a-4de7-bf0a-4cf9250fc223"

headers = {
    "Authorization": f"Splunk {HEC_TOKEN}"
}

# Mix of logs (normal + attack)
logs = [

    # SQL Injection attempts (same IP)
    "WARNING Possible SQL Injection attempt ip=192.168.1.45 payload=' OR 1=1 --",
    "ERROR Database query failed suspicious input ip=192.168.1.45",
    "WARNING SQL Injection attempt ip=192.168.1.45 payload=admin'--",
    "ERROR Login bypass attempt detected ip=192.168.1.45 payload=' OR 'a'='a",
    "CRITICAL SQL Injection exploitation attempt ip=192.168.1.45 table=users",

]


def send_log(log):
    data = {
        "event": log,
        "sourcetype": "soc_test"
    }

    try:
        response = requests.post(HEC_URL, json=data, headers=headers)
        print("Sent:", log, "| Status:", response.status_code)
    except Exception as e:
        print("Error:", e)


def simulate_attack():
    print("\n Simulating controlled traffic...\n")

    for log in logs:
        send_log(log)

        #slow down
        time.sleep(3)

    print("\n Simulation complete")


if __name__ == "__main__":
    simulate_attack()