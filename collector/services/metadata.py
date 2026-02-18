import socket
import platform
from datetime import datetime

def enrich_metadata():
    return {
        "collector_host": socket.gethostname(),
        "collector_os": platform.system(),
        "collector_os_version": platform.version(),
        "received_at": datetime.utcnow().isoformat()
    }
