import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "llama3"

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "root_cause": {"type": "string"},
        "remediation_steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {"type": "string"},
                    "where": {"type": "string"},
                    "can_automate": {"type": "boolean"}
                },
                "required": ["action", "where", "can_automate"]
            }
        },
        "priority": {"type": "string"},
        "automation_possible": {"type": "boolean"}
    },
    "required": ["root_cause", "remediation_steps", "priority", "automation_possible"]
}

def call_llm(prompt: str):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": JSON_SCHEMA,         
            "options": {
                "temperature": 0,
                "top_p": 0.1
            }
        }

        res = requests.post(OLLAMA_URL, json=payload, timeout=300)

        if res.status_code != 200:
            print(">>> Ollama error:", res.text)
            return None

        data = res.json()
        return data.get("response", "").strip()

    except Exception as e:
        print(">>> Ollama LLM call failed:", str(e))
        return None
