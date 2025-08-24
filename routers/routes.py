from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from models.models import RecordHistory, Commit, RecordHead
from dto.alldto import CommitRead, CommitCreate
from db.db_connect import SessionLocal, engine
from handlers import handlers


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


vcs_router = APIRouter(tags="All routers")


@vcs_router.post("/commits", response_model=CommitRead)
def create_commit(commit: CommitCreate, db: Session = Depends(get_db)):
    return handlers.commit_creation(db, commit)
