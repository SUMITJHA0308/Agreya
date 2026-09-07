from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db
from app.models.mission import Mission
from app.models.rover import Rover
from app.schemas.mission import MissionCreate, MissionStatusUpdate

router = APIRouter(
    prefix="/api/missions",
    tags=["Rover Missions"]
)


@router.post("/")
def create_mission(
    data: MissionCreate,
    db: Session = Depends(get_db)
):

    rover = db.query(Rover).filter(
        Rover.status == "IDLE"
    ).first()

    if not rover:
        return {
            "message": "No rover available"
        }

    mission = Mission(
        mission_id=f"M-{uuid.uuid4().hex[:8].upper()}",
        rover_id=rover.rover_id,
        node_id=data.node_id,
        worker_id=data.worker_id,
        destination_x=data.destination_x,
        destination_y=data.destination_y,
        reason=data.reason,
        status="ASSIGNED"
    )

    rover.status = "MISSION"

    db.add(mission)
    db.commit()
    db.refresh(mission)

    return mission


@router.get("/")
def get_missions(
    db: Session = Depends(get_db)
):

    return (
        db.query(Mission)
        .order_by(Mission.created_at.desc())
        .all()
    )


@router.get("/{mission_id}")
def get_mission(
    mission_id: str,
    db: Session = Depends(get_db)
):

    mission = db.query(Mission).filter(
        Mission.mission_id == mission_id
    ).first()

    if not mission:
        return {
            "message": "Mission not found"
        }

    return mission


@router.patch("/{mission_id}/status")
def update_mission_status(
    mission_id: str,
    data: MissionStatusUpdate,
    db: Session = Depends(get_db)
):

    mission = db.query(Mission).filter(
        Mission.mission_id == mission_id
    ).first()

    if not mission:
        return {
            "message": "Mission not found"
        }

    mission.status = data.status

    if data.status == "COMPLETED":
        mission.completed_at = datetime.utcnow()

        rover = db.query(Rover).filter(
            Rover.rover_id == mission.rover_id
        ).first()

        if rover:
            rover.status = "IDLE"

    db.commit()

    return {
        "message": "Mission status updated",
        "mission_id": mission_id,
        "status": data.status
    }