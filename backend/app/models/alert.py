from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    node_id = Column(String, index=True, nullable=False)

    alert_type = Column(String)
    severity = Column(String)

    value = Column(Float, nullable=True)

    message = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    resolved = Column(
        String,
        default="NO"
    )