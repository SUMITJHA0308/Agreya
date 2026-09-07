from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.mission import Mission
from app.models.rover import Rover


def create_emergency_mission(
    db: Session,
    node_id: str | None = None,
    worker_id: str | None = None,
    reason: str = "EMERGENCY",
    destination_x: float | None = None,
    destination_y: float | None = None
):
    """
    Automatically create a rover mission for an emergency.
    """

    # Find an available rover
    rover = (
        db.query(Rover)
        .filter(Rover.status == "IDLE")
        .first()
    )

    # No rover available
    if not rover:
        return None

    mission = Mission(
        mission_id=f"M-{uuid.uuid4().hex[:8].upper()}",
        rover_id=rover.rover_id,
        node_id=node_id,
        worker_id=worker_id,
        destination_x=destination_x,
        destination_y=destination_y,
        reason=reason,
        status="ASSIGNED",
        created_at=datetime.utcnow()
    )

    # Mark rover as busy
    rover.status = "MISSION"

    db.add(mission)
    db.commit()
    db.refresh(mission)

    return mission