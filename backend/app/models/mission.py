from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)

    mission_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    rover_id = Column(
        String,
        nullable=True
    )

    node_id = Column(
        String,
        nullable=True
    )

    worker_id = Column(
        String,
        nullable=True
    )

    destination_x = Column(
        Float,
        nullable=True
    )

    destination_y = Column(
        Float,
        nullable=True
    )

    reason = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )