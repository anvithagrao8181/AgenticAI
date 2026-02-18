def build_prompt(label, normalized_log, confidence):
    return f"""
You are a Senior Site Reliability Engineer (SRE).
You diagnose production failures in CI/CD pipelines.

IMPORTANT:
You MUST reason using DevOps knowledge.
DO NOT give generic troubleshooting steps.
Give root cause specific to the error type.

ERROR TYPE KNOWLEDGE:

http_500 → Backend application exception or crash
ssh_timeout → Host unreachable / firewall / network drop
mvn_missing → Maven not installed or PATH misconfigured
connection_refused → Service not running on port
git_auth_failed → Invalid credentials or token
permission_denied → File or system permission issue

Incident classification: {label}
Confidence: {confidence}

Log:
{normalized_log}

Return ONLY JSON:

{{
  "root_cause": "precise technical cause",
  "remediation_steps": [
    {{
      "action": "specific fix",
      "where": "Jenkins | Build Agent | Application Server | CI/CD Config | Repository | Network | Cloud",
      "can_automate": true
    }}
  ],
  "priority": "High | Medium | Low",
  "automation_possible": true
}}
"""
