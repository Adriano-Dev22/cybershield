from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(max_length=100)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True