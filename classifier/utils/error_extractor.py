KEYWORDS = [
    "error",
    "failed",
    "exception",
    "denied",
    "refused",
    "timed out",
    "not found",
    "unable",
    "cannot",
    "server closed",
    "internal server error"
]

def extract_error(log: str) -> str:

    if not log:
        return ""

    lines = log.splitlines()
    important = []

    for line in lines:
        l = line.lower()
        if any(k in l for k in KEYWORDS):
            important.append(line.strip())

    if not important:
        return log[-400:]  # fallback last lines

    return " ".join(important[-6:])
