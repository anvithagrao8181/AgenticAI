import os
import json

def save_raw_log(base_path, event_id, raw_log):
    path = os.path.join(base_path, "raw_logs", f"{event_id}.log")
    path = os.path.abspath(path)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    print(">>> Saving RAW log to:", path)

    with open(path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(raw_log)

    return path


def save_event_json(base_path, event_id, event_data):
    path = os.path.join(base_path, "events", f"{event_id}.json")
    path = os.path.abspath(path)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    print(">>> Saving EVENT json to:", path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(event_data, f, indent=2)

    return path
