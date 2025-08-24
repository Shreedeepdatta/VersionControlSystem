from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from models.models import Commit, RecordHead, RecordHistory
from dto.alldto import CommitCreate

def commit_creation(db: Session, commit: CommitCreate)-> Commit:
    