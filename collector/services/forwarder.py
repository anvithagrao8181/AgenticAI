import requests

PREPROCESSOR_URL = "http://192.168.29.105:5001/preprocess"

def forward_to_preprocessor(event_data):
    try:
        res = requests.post(PREPROCESSOR_URL, json=event_data, timeout=20)

        print(">>> Forwarded to preprocessor:", PREPROCESSOR_URL)
        print(">>> Response status:", res.status_code)

        if res.status_code == 200:
            return True, res.json()
        else:
            print(">>> Preprocessor error:", res.text)
            return False, None

    except Exception as e:
        print(">>> Preprocessor forward failed:", str(e))
        return False, None
