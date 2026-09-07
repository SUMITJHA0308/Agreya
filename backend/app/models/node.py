from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)

    node_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    location = Column(String, nullable=True)

    zone = Column(String, nullable=True)

    location_x = Column(Float, nullable=True)

    location_y = Column(Float, nullable=True)

    status = Column(
        String,
        default="OFFLINE"
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )