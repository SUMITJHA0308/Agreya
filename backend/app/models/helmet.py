from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Helmet(Base):
    __tablename__ = "helmets"

    id = Column(Integer, primary_key=True, index=True)

    helmet_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    worker_id = Column(
        String,
        unique=True,
        nullable=True
    )

    battery = Column(
        Integer,
        default=100
    )

    status = Column(
        String,
        default="ONLINE"
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )