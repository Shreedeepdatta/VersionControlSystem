from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from models.models import RecordHistory, Commit, RecordHead
from dto.alldto import CommitHead, CommitCreate
from db.db_connect import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


vcs_router = APIRouter(tags="All routers")


