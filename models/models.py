from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship)
import uuid
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy import (ForeignKey, Text, CheckConstraint, JSON)
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Commit(Base):
    __tablename__ = "commit"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_commit: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("commit.id"), nullable=True
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(datetime.timezone.utc))

    parent: Mapped["Commit"] = relationship(
        remote_side=[id], backref="children")
    records: Mapped[list["RecordHistory"]] = relationship(
        back_populates="commit")


class RecordHistory(Base):
    __tablename__ = "record_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_key: Mapped[str] = mapped_column(Text, index=True)
    commit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("commit.id"))
    operation: Mapped[str] = mapped_column(Text, CheckConstraint(
        "operation IN ('add', 'update', 'delete')"), nullable=False)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(datetime.timezone.utc))

    commit: Mapped["Commit"] = relationship(back_populates="records")


class RecordHead(Base):
    __tablename__ = "record_head"

    record_key: Mapped[str] = mapped_column(Text, primary_key=True)
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_commit: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("commit.id"))
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(datetime.timezone.utc))
