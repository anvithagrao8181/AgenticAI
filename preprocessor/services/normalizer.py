import re

def normalize_log(text: str) -> str:
    if not text:
        return ""

    # Replace IP addresses
    text = re.sub(r"\b\d{1,3}(\.\d{1,3}){3}\b", "<IP>", text)

    # Replace file paths
    text = re.sub(r"[A-Z]:\\\\[^\s]+", "<WINDOWS_PATH>", text)

    # Replace timestamps
    text = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "<TIMESTAMP>", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()
