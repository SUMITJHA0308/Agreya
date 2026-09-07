from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.rover import Rover
from app.schemas.rover import RoverCreate, RoverStatusUpdate

router = APIRouter(
    prefix="/api/rovers",
    tags=["Rovers"]
)


@router.post("/")
def create_rover(
    data: RoverCreate,
    db: Session = Depends(get_db)
):

    rover = Rover(
        rover_id=data.rover_id
    )

    db.add(rover)
    db.commit()
    db.refresh(rover)

    return rover


@router.get("/")
def get_rovers(
    db: Session = Depends(get_db)
):

    return db.query(Rover).all()


@router.post("/status")
def update_rover_status(
    data: RoverStatusUpdate,
    db: Session = Depends(get_db)
):

    rover = db.query(Rover).filter(
        Rover.rover_id == data.rover_id
    ).first()

    if not rover:
        return {
            "message": "Rover not found"
        }

    rover.status = data.status
    rover.battery = data.battery
    rover.current_x = data.current_x
    rover.current_y = data.current_y
    rover.last_seen = datetime.utcnow()

    db.commit()

    return {
        "message": "Rover status updated"
    }