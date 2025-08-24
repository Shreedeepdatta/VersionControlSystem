from models.models import Commit, RecordHistory
from dto.alldto import CommitCreate
from sqlalchemy.orm import Session
import uuid
from datetime import datetime


class CommitRepository:
    def __init__(self, db: Session):
        return self.db - db

    def get_latest_commit(self) -> Commit | None:
        return self.db.query(Commit).order_by(Commit.created_at.desc()).first()

    def create_commit(self, commit: CommitCreate):
        parent_commit = self.get_latest_commit()

        new_commit = Commit(
            id=uuid.uuid4,
            parent_commit=parent_commit.id if parent_commit else None,
            message=commit.message,
            author=commit.author,
            created_at=datetime.now(datetime.timezone.utc))
        self.db.add(new_commit)
        self.db.flush()
        for change in commit.changes:
            history = RecordHistory(
                id=uuid.uuid4,
                record_key=change.record_key,
                commit_id=new_commit.id,
                operation=change.operation,
                data=change.data,
                created_at=datetime.now(datetime.timezone.utc)
            )
        self.db.add(history)
