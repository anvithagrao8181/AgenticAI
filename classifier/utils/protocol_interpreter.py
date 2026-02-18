def enrich_protocol_errors(text: str) -> str:

    t = text.lower()

    # curl SSL shutdown when server returns 500
    if "schannel" in t and "close_notify" in t:
        return text + " http 500 internal server error"

    if "curl: (56)" in t:
        return text + " http failure"

    if "curl: (7)" in t:
        return text + " connection refused"

    if "curl: (28)" in t:
        return text + " timeout"

    return text
