import re

def clean_log(raw_log: str) -> str:
    if not raw_log:
        return ""

    lines = raw_log.splitlines()
    cleaned = []

    for line in lines:
        # Skip Jenkins pipeline noise
        if line.strip().startswith("[Pipeline]"):
            continue

        # Skip workspace paths
        if "Jenkins" in line and "workspace" in line:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)
