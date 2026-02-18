from flask import Flask, request, jsonify, render_template
import json

from services.rule_fallback import plan_with_rules
from services.prompt_builder import build_prompt
from services.llm_client import call_llm

app = Flask(__name__)

# Stores latest incident for dashboard
LAST_INCIDENT = None


# -------------------------------------------------------
# UI DASHBOARD
# -------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/latest")
def latest_incident():
    global LAST_INCIDENT

    if LAST_INCIDENT is None:
        return jsonify({"status": "waiting"})

    return jsonify(LAST_INCIDENT)


# -------------------------------------------------------
# MAIN PLANNER API
# -------------------------------------------------------
@app.route("/plan", methods=["POST"])
def plan():
    global LAST_INCIDENT

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    label = data.get("label", "unknown")
    confidence = data.get("confidence", 0)
    normalized_log = data.get("normalized_log", "")

    print(f"\n>>> Planner received: {label} (confidence={confidence})")

    # -------- BUILD PROMPT --------
    prompt = build_prompt(label, normalized_log, confidence)

    print("\n================ PROMPT SENT TO LLM ================\n")
    print(prompt)
    print("\n====================================================\n")

    # -------- CALL LLM --------
    llm_text = call_llm(prompt)

    print("\n================ RAW LLM RESPONSE ==================\n")
    print(llm_text)
    print("\n====================================================\n")

    llm_result = None
    llm_used = False

    if llm_text:
        try:
            llm_result = json.loads(llm_text)
            llm_used = True
        except json.JSONDecodeError:
            print(">>> Invalid JSON from LLM → fallback rules")

    # ================= LLM SUCCESS =================
    if llm_result:
        result = {
            "label": label,
            "confidence": confidence,
            "root_cause": llm_result.get("root_cause"),
            "remediation_steps": llm_result.get("remediation_steps"),
            "priority": llm_result.get("priority", "medium").lower(),
            "automation_possible": llm_result.get("automation_possible", False),
            "llm_used": True,

            # 🔥 DEBUG TRACE
            "debug": {
                "prompt": prompt,
                "raw_llm_output": llm_text
            }
        }

        LAST_INCIDENT = result
        return jsonify(result), 200

    # ================= RULE FALLBACK =================
    rule_plan = plan_with_rules(label)

    result = {
        "label": label,
        "confidence": confidence,
        "root_cause": rule_plan.get("root_cause"),
        "remediation_steps": [
            {
                "action": step,
                "where": "Manual Investigation",
                "can_automate": False
            } for step in rule_plan.get("steps", [])
        ],
        "priority": rule_plan.get("priority", "medium"),
        "automation_possible": True,
        "llm_used": False,

        # 🔥 DEBUG TRACE
        "debug": {
            "prompt": prompt,
            "raw_llm_output": "RULE_FALLBACK_TRIGGERED"
        }
    }

    LAST_INCIDENT = result
    return jsonify(result), 200



# -------------------------------------------------------
# START SERVER
# -------------------------------------------------------
if __name__ == "__main__":
    print("Starting Planner service on port 7000...")
    app.run(host="0.0.0.0", port=7000, debug=False)
