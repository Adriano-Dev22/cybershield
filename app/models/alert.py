from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_id: int
    title: str
    description: str
    severity: str = Field(default="suspicious", max_length=20)
    mitre_tactic: str

    class Config:
        from_attributes = True