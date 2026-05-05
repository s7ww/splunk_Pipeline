from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import tool

import re

# -----------------------------
# LLM
# -----------------------------
llm = OllamaLLM(model="llama3")

# -----------------------------
# TOOL: Extract IP intelligence (simple version)
# -----------------------------
@tool
def enrich_ip(ip: str) -> str:
    """Basic IP enrichment tool"""
    if ip.startswith("192.168"):
        return "Internal IP - likely inside network"
    return "External IP - possible threat source"

# -----------------------------
# OUTPUT PARSER
# -----------------------------
parser = JsonOutputParser()

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an experienced SOC analyst working in a Security Operations Center.

Your job:
- Analyze security logs
- Identify attack patterns
- Classify threats correctly
- Be concise and precise

Rules:
- Always return ONLY valid JSON
- No explanations outside JSON
- Use professional SOC terminology

Threat Levels:
- LOW → normal / harmless
- MEDIUM → suspicious
- HIGH → confirmed attack
- CRITICAL → severe breach

Attack Types:
- Brute Force
- SQL Injection
- XSS
- Privilege Escalation
- Port Scan
- Data Exfiltration
- Malware Execution
- Unauthorized Access
- DDoS
- Unknown

Think step-by-step BEFORE answering.
"""),

    ("human", """
Logs:
{logs}

Context:
- Logs are grouped by same IP
- Multiple similar events = stronger threat

Return STRICT JSON:
{format_instructions}
""")
])

# -----------------------------
# MAIN ANALYZER
# -----------------------------
def analyze_event(logs):
    if not logs:
        return {"status": "no logs"}

    combined = "\n".join(logs)

    # Extract IP (basic)
    ip_match = re.search(r"\b\d+\.\d+\.\d+\.\d+\b", combined)
    ip = ip_match.group(0) if ip_match else "unknown"

    # Tool usage
    ip_context = enrich_ip.invoke(ip)

    try:
        chain = prompt | llm | parser

        result = chain.invoke({
            "logs": combined + f"\n\nIP Context: {ip_context}",
            "format_instructions": parser.get_format_instructions()
        })

        return result

    except Exception as e:
        print("LLM error:", e)
        return {
            "threat_level": "UNKNOWN",
            "attack_type": "Unknown",
            "summary": "LLM failed",
            "recommended_action": "Check logs manually"
        }