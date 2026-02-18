import re

# High priority patterns (deterministic failures)
STRONG_PATTERNS = [
    r"not recognized as an internal or external command",
    r"command not found",
    r"no such file or directory",
    r"connection timed out",
    r"connection refused",
    r"permission denied",
    r"authentication failed",
    r"access denied",
    r"no route to host",
    r"network is unreachable",
    r"cannot resolve host",
    r"unknown lifecycle phase",
    r"requires a project to execute",
    r"missingprojectexception",
    r"outofmemoryerror",
    r"no space left on device"
]

# Medium priority (generic failures)
WEAK_PATTERNS = [
    r"\berror\b",
    r"\bfailed\b",
    r"\bexception\b"
]

def extract_signature(text: str) -> str:
    if not text:
        return ""

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # 🔴 STEP 1: search from bottom (real failures usually last)
    for line in reversed(lines[-80:]):  # last 80 lines only
        low = line.lower()

        for pat in STRONG_PATTERNS:
            if re.search(pat, low):
                return line[:200]

    # 🔴 STEP 2: fallback generic error lines
    for line in reversed(lines[-80:]):
        low = line.lower()
        for pat in WEAK_PATTERNS:
            if re.search(pat, low):
                return line[:200]

    # 🔴 STEP 3: last meaningful line
    for line in reversed(lines):
        if len(line) > 15:
            return line[:200]

    return lines[-1][:200] if lines else ""
