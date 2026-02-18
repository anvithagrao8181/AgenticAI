from flask import Flask, request, jsonify
from models.vector_classifier import classify_log

app = Flask(__name__)

# ---------------------------------------------------------
# RAW MODEL LABEL → PLATFORM OPERATIONAL CATEGORY
# (Detection != Action)
# ---------------------------------------------------------
RAW_TO_PLATFORM = {

    # demo scenarios
    "disk_full": "disk_full",
    "docker_daemon_down": "service_unreachable",
    "git_auth_failed": "authentication_failed",
    "ssh_auth_failed": "authentication_failed",
    "ssh_timeout": "network_timeout",
    "connection_refused": "service_unreachable",
    "network_unreachable": "network_unreachable",
    "permission_denied": "authorization_failed",
    "scm_checkout_failed": "ci_project_missing",
    "mvn_missing": "tool_not_installed",
    "http_500": "service_unreachable",

    # infra / platform
    "oom_error": "out_of_memory",
    "db_connection_failed": "service_unreachable",
    "k8s_image_pull_failed": "service_unreachable",
    "cloud_auth_failed": "authentication_failed",

    # default
    "unknown": "unknown_failure"
}

# ---------------------------------------------------------
# USER FRIENDLY DESCRIPTIONS
# ---------------------------------------------------------
LABELS = {
    "network_timeout": "Network timeout",
    "authentication_failed": "Authentication failed",
    "service_unreachable": "Service unreachable or refused connection",
    "network_unreachable": "Network unreachable",
    "tool_not_installed": "Required build tool not installed",
    "authorization_failed": "Permission denied",
    "ci_project_missing": "SCM checkout or project configuration issue",
    "disk_full": "Disk full on build agent",
    "out_of_memory": "Out of memory error",
    "unknown_failure": "Unknown / uncategorized failure"
}

CONFIDENCE_THRESHOLD = 0.45


# ---------------------------------------------------------
# CLASSIFICATION ENDPOINT
# ---------------------------------------------------------
@app.route("/classify", methods=["POST"])
def classify():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    event_id = data.get("event_id")
    normalized_log = data.get("normalized_log", "")

    print("\n>>> Received event:", event_id)

    # -------- VECTOR AI PREDICTION --------
    raw_label, confidence = classify_log(normalized_log)

    # -------- MAP TO PLATFORM CATEGORY --------
    platform_label = RAW_TO_PLATFORM.get(raw_label, "unknown_failure")

    # -------- SAFETY FALLBACK --------
    if confidence < CONFIDENCE_THRESHOLD:
        platform_label = "unknown_failure"

    print(">>> Raw Label:", raw_label)
    print(">>> Platform Label:", platform_label)
    print(">>> Confidence:", confidence)

    return jsonify({
        "event_id": event_id,
        "label": platform_label,
        "label_description": LABELS.get(platform_label, "Unknown"),
        "confidence": round(confidence, 3),
        "model": "vector_similarity",
        "raw_label": raw_label
    }), 200


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
