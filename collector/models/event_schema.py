# from pydantic import BaseModel
# from typing import Dict, Any

# class UnifiedEvent(BaseModel):
#     event_id: str
#     source: str
#     service: str
#     environment: str
#     timestamp: str
#     raw_log: str
#     normalized_log: str
#     metadata: Dict[str, Any]
#     severity: str

from pydantic import BaseModel
from typing import Dict, Any

class UnifiedEvent(BaseModel):
    event_id: str
    source: str
    service: str
    environment: str
    timestamp: str
    raw_log: str
    normalized_log: str
    metadata: Dict[str, Any]
    severity: str
