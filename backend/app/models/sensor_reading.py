from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    node_id = Column(String, index=True, nullable=False)

    mq2 = Column(Float, nullable=True)
    ultrasonic = Column(Float, nullable=True)
    ir = Column(Integer, nullable=True)

    status = Column(String, default="GREEN")

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )