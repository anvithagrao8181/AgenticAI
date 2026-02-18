import requests
from requests.auth import HTTPBasicAuth
from config import JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN

def fetch_console_log(job_name, build_number):
    try:
        if not all([JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN]):
            return "Jenkins API not configured"

        url = f"{JENKINS_URL}/job/{job_name}/{build_number}/consoleText"

        print(">>> Fetching Jenkins console log from:", url)

        res = requests.get(
            url,
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN),
            timeout=30
        )

        if res.status_code == 200:
            return res.text
        else:
            return f"Failed to fetch console log. Status: {res.status_code}"

    except Exception as e:
        return f"Error fetching console log: {str(e)}"
