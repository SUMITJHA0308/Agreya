from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Rover(Base):
    __tablename__ = "rovers"

    id = Column(Integer, primary_key=True, index=True)

    rover_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    status = Column(
        String,
        default="IDLE"
    )

    battery = Column(
        Float,
        default=100
    )

    current_x = Column(
        Float,
        default=0
    )

    current_y = Column(
        Float,
        default=0
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )