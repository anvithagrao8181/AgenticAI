from flask import Flask, request, jsonify
import requests

from services.cleaner import clean_log
from services.normalizer import normalize_log
from services.signature import extract_signature

app = Flask(__name__)

CLASSIFIER_URL = "http://192.168.29.105:6000/classify"
PLANNER_URL = "http://192.168.29.105:7000/plan"


@app.route("/preprocess", methods=["POST"])
def preprocess():
    data = request.get_json(silent=True)

    if not data or "raw_log" not in data:
        return jsonify({"error": "raw_log missing"}), 400

    raw_log = data.get("raw_log", "")

    print(">>> Preprocessor received log, length:", len(raw_log))

    # 1️⃣ Clean
    cleaned = clean_log(raw_log)

    # 2️⃣ Normalize
    normalized = normalize_log(cleaned)

    # 3️⃣ Extract REAL error line
    signature = extract_signature(normalized)

    print(">>> Extracted error signature:", signature)

    # ⭐ IMPORTANT: AI should see ONLY the error line
    ai_input = signature if signature else normalized[:200]

    result = {
        "event_id": data.get("event_id"),
        "cleaned_log": cleaned,
        "normalized_log": ai_input,   # send reduced text forward
        "error_signature": signature,
        "source": data.get("source"),
        "service": data.get("service"),
        "severity": data.get("severity"),
    }

    cls_data = None

    # ---------------- CLASSIFIER ----------------
    try:
        cls_res = requests.post(
            CLASSIFIER_URL,
            json={
                "event_id": data.get("event_id"),
                "normalized_log": ai_input,
                "error_signature": signature
            },
            timeout=180
        )

        if cls_res.status_code == 200:
            cls_data = cls_res.json()
            result["classification"] = cls_data
            print(">>> Classifier result:", cls_data)
        else:
            print(">>> Classifier error:", cls_res.text)

    except Exception as e:
        print(">>> Classifier call failed:", str(e))

    # ---------------- PLANNER ----------------
    if cls_data:
        try:
            plan_res = requests.post(
                PLANNER_URL,
                json={
                    "label": cls_data.get("label"),
                    "confidence": cls_data.get("confidence"),
                    "normalized_log": ai_input
                },
                timeout=180
            )

            if plan_res.status_code == 200:
                plan_data = plan_res.json()
                result["plan"] = plan_data
                print(">>> Planner result:", plan_data)
            else:
                print(">>> Planner error:", plan_res.text)

        except Exception as e:
            print(">>> Planner call failed:", str(e))

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
