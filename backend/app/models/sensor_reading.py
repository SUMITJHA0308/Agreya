from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    node_id = Column(String, index=True, nullable=False)

    # NODE 1 sensors
    mq2 = Column(Float, nullable=True)
    mq7 = Column(Float, nullable=True)
    vibration = Column(Integer, nullable=True)

    # NODE 2 sensor
    ultrasonic = Column(Float, nullable=True)

    status = Column(String, default="GREEN")

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )