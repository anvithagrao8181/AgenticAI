REMEDIATION_MAP = {
    "ssh_timeout": {
        "root_cause": "Target host is unreachable or not responding on SSH port.",
        "steps": [
            "Check if target host is powered on",
            "Verify firewall rules allow port 22",
            "Check VPN or network connectivity",
            "Ping the host to verify reachability"
        ],
        "priority": "high"
    },
    "ssh_auth_failed": {
        "root_cause": "Invalid SSH credentials or key configuration.",
        "steps": [
            "Verify SSH username",
            "Check SSH private key configuration",
            "Ensure public key is present on server",
            "Check file permissions on ~/.ssh"
        ],
        "priority": "high"
    },
    "mvn_missing": {
        "root_cause": "Maven is not installed or not in PATH on Jenkins agent.",
        "steps": [
            "Install Maven on Jenkins agent",
            "Add Maven to system PATH",
            "Configure Maven tool in Jenkins Global Tools",
            "Restart Jenkins agent"
        ],
        "priority": "medium"
    },
    "network_unreachable": {
        "root_cause": "Network routing or DNS issue.",
        "steps": [
            "Check network routing",
            "Verify DNS resolution",
            "Check proxy or VPN settings",
            "Contact network administrator"
        ],
        "priority": "high"
    },
    "connection_refused": {
        "root_cause": "Service is not listening on target port.",
        "steps": [
            "Verify service is running on target host",
            "Check port configuration",
            "Restart target service",
            "Check firewall rules"
        ],
        "priority": "high"
    },
    "unknown": {
        "root_cause": "Unable to determine exact root cause.",
        "steps": [
            "Review full console log",
            "Enable debug logging",
            "Retry pipeline",
            "Escalate to DevOps team"
        ],
        "priority": "medium"
    }
}

def plan_with_rules(label: str):
    return REMEDIATION_MAP.get(label, REMEDIATION_MAP["unknown"])
