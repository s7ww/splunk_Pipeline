import time
import splunklib.client as client
import splunklib.results as results
from langchain_ollama import OllamaLLM

# Initialize LLM
llm = OllamaLLM(model="llama3")

# -------------------------
# 1. Fetch logs from Splunk
# -------------------------
def get_logs():
    service = client.connect(
        host='localhost',
        port=8089,
        username='sawan',
        password='Fcrx7_1209'
    )

    query = "search index=soc_logs | head 5"
    job = service.jobs.create(query)

    while not job.is_done():
        time.sleep(0.5)

    reader = results.ResultsReader(job.results())

    logs = []
    for item in reader:
        if isinstance(item, dict):
            logs.append(item.get("_raw", ""))

    return logs


# -------------------------
# 2. Analyze ONE log
# -------------------------
def analyze_log(log):
    prompt = f"""
You are a SOC analyst.

Analyze this log:
{log}

Return STRICT JSON:
{{
 "threat_level": "",
 "attack_type": "",
 "summary": "",
 "recommended_action": ""
}}
"""
    return llm.invoke(prompt)


# -------------------------
# 3. Full pipeline
# -------------------------
def pipeline():
    logs = get_logs()

    print("\n=== RAW LOGS ===")
    for log in logs:
        print(log)

    print("\n=== ANALYSIS ===")

    for log in logs:
        result = analyze_log(log)

        print("\n--- ALERT ---")
        print(result)


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    pipeline()