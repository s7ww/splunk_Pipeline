from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")


def analyze_event(logs):
    if not logs:
        return {"status": "no logs"}

    combined = "\n".join(logs)

    prompt = f"""
You are a SOC analyst.

Analyze this incident:
{combined}

Return STRICT JSON:
{{
 "threat_level": "",
 "attack_type": "",
 "summary": "",
 "recommended_action": ""
}}
"""

    try:
        return llm.invoke(prompt)
    except Exception as e:
        print("❌ LLM error:", e)
        return {"error": "LLM failed"}
