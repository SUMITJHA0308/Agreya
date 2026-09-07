from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime

from app.database import Base


class RoverAssessment(Base):
    __tablename__ = "rover_assessments"

    id = Column(Integer, primary_key=True, index=True)

    mission_id = Column(
        String,
        index=True,
        nullable=False
    )

    mq2 = Column(Float, nullable=True)

    mq7 = Column(Float, nullable=True)

    ultrasonic = Column(
        Float,
        nullable=True
    )

    person_detected = Column(
        Boolean,
        default=False
    )

    crack_detected = Column(
        Boolean,
        default=False
    )

    overall_status = Column(
        String,
        default="SAFE"
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )