from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class SecurityEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_ip: str = Field(max_length=45)
    username: Optional[str] = Field(default=None, max_length=50)
    event_type: str = Field(max_length=50)
    status: str = Field(max_length=20)          # success, fail
    details: str
    severity: str = Field(default="normal", max_length=20)   # normal, suspicious, critical
    mitre_tactic: Optional[str] = Field(default=None, max_length=100)
    mitre_technique: Optional[str] = Field(default=None, max_length=100)

    class Config:
        from_attributes = True