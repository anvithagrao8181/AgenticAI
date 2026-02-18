def validate_payload(data: dict):
    required = ["source", "service", "raw_log"]

    for field in required:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data["raw_log"], str):
        raise ValueError("raw_log must be string")
