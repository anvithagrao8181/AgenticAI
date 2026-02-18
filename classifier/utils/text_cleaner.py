import re

def clean_log(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r'\d+\.\d+\.\d+\.\d+', '<ip>', text)
    text = re.sub(r'\d+', '<num>', text)
    text = re.sub(r'[/\\].*? ', ' <path> ', text)

    return text.strip()
