from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime

from models.event_schema import UnifiedEvent
from services.validator import validate_payload
from services.metadata import enrich_metadata
from services.storage import save_raw_log, save_event_json
from services.forwarder import forward_to_preprocessor
from config import STORAGE_PATH

routes = Blueprint("routes", __name__)

@routes.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True)

    print(">>> /collect HIT")
    print(">>> Incoming data keys:", list(data.keys()) if data else None)

    try:
        if not data:
            raise ValueError("Invalid or missing JSON body")

        validate_payload(data)
        print(">>> Validation passed")

        event_id = str(uuid.uuid4())

        # ---- Metadata ----
        metadata = enrich_metadata()
        metadata.update({
            "build_number": data.get("build_number"),
            "node": data.get("node"),
            "job_name": data.get("service"),
            "git_branch": data.get("git_branch"),
            "commit_id": data.get("commit_id"),
            "triggered_by": data.get("triggered_by")
        })

        full_log = data.get("raw_log")
        job_name = data.get("service")

        event = UnifiedEvent(
            event_id=event_id,
            source=data.get("source"),
            service=job_name,
            environment=data.get("environment", "ci"),
            timestamp=datetime.utcnow().isoformat(),
            raw_log=full_log,
            normalized_log=full_log,
            metadata=metadata,
            severity=data.get("severity", "unknown")
        )

        # ---------------- PREPROCESSOR CALL ----------------
        payload = {
            "event_id": event.event_id,
            "service": event.service,
            "raw_log": event.raw_log,
            "source": event.source,
            "severity": event.severity
        }

        ok, pre = forward_to_preprocessor(payload)

        # Guarantee deterministic downstream behavior
        if not ok or not pre:
            print(">>> Preprocessor failed, using fallback signature")
            event.metadata["error_signature"] = "preprocessor_failed"
        else:
            event.normalized_log = pre.get("normalized_log", event.raw_log)
            event.metadata["error_signature"] = pre.get("error_signature", "unknown_error")
            event.metadata["cleaned_log"] = pre.get("cleaned_log")

        print(">>> FINAL ERROR SIGNATURE:", event.metadata.get("error_signature"))

        # ---------------- STORAGE ----------------
        save_raw_log(STORAGE_PATH, event_id, event.raw_log)
        save_event_json(STORAGE_PATH, event_id, event.dict())

        return jsonify({
            "status": "accepted",
            "event_id": event_id
        }), 200

    except Exception as e:
        print(">>> ERROR in /collect:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
