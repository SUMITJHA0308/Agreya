from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    name = Column(String, nullable=False)

    helmet_id = Column(
        String,
        unique=True,
        nullable=True
    )

    status = Column(
        String,
        default="SAFE"
    )

    last_node_id = Column(
        String,
        nullable=True
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )