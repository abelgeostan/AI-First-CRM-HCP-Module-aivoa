import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    JSON,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found in .env")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String, nullable=True)

    interaction_type = Column(
        String,
        default="Meeting",
        nullable=False,
    )

    date = Column(String, nullable=True)

    time = Column(String, nullable=True)

    attendees = Column(
        JSON,
        default=list,
        nullable=False,
    )

    topics_discussed = Column(
        String,
        nullable=True,
    )

    materials_shared = Column(
        JSON,
        default=list,
        nullable=False,
    )

    samples_distributed = Column(
        JSON,
        default=list,
        nullable=False,
    )

    sentiment = Column(
        String,
        nullable=True,
    )

    outcomes = Column(
        String,
        nullable=True,
    )

    follow_up_actions = Column(
        String,
        nullable=True,
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()