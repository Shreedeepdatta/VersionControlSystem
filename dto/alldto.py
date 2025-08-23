from pydantic import BaseModel
from typing import Literal, List, Optional
from uuid import UUID
from datetime import datetime


class RecordChange(BaseModel):
    record_key: str
    operation: Literal["add", "update", "delete"]
    data: Optional[dict] = None


class CommitChange(BaseModel):
    message: str
    author: str
    changes: List[RecordChange]


class CommitHead(BaseModel):
    id: UUID
    parent_commit: Optional[UUID]
    message: str
    author: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommitCreate(BaseModel):
    message: str
    author: str
    changes: List[RecordChange]
