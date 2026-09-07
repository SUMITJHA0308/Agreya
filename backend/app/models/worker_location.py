from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class WorkerLocation(Base):
    __tablename__ = "worker_locations"

    id = Column(Integer, primary_key=True, index=True)

    worker_id = Column(
        String,
        index=True,
        nullable=False
    )

    node_id = Column(
        String,
        nullable=False
    )

    signal_strength = Column(
        Float,
        nullable=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )