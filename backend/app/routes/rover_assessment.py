from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rover_assessment import RoverAssessment
from app.models.mission import Mission

router = APIRouter(
    prefix="/api/rover-assessments",
    tags=["Rover Assessment"]
)


@router.post("/")
def create_assessment(
    mission_id: str,
    mq2: float | None = None,
    mq7: float | None = None,
    ultrasonic: float | None = None,
    person_detected: bool = False,
    crack_detected: bool = False,
    db: Session = Depends(get_db)
):

    if person_detected or crack_detected:
        status = "DANGER"
    elif (
        (mq2 is not None and mq2 >= 800)
        or
        (mq7 is not None and mq7 >= 800)
    ):
        status = "DANGER"
    else:
        status = "SAFE"

    assessment = RoverAssessment(
        mission_id=mission_id,
        mq2=mq2,
        mq7=mq7,
        ultrasonic=ultrasonic,
        person_detected=person_detected,
        crack_detected=crack_detected,
        overall_status=status
    )

    db.add(assessment)

    mission = db.query(Mission).filter(
        Mission.mission_id == mission_id
    ).first()

    if mission:
        mission.status = "ASSESSMENT_COMPLETED"

    db.commit()
    db.refresh(assessment)

    return assessment


@router.get("/{mission_id}")
def get_assessment(
    mission_id: str,
    db: Session = Depends(get_db)
):

    return (
        db.query(RoverAssessment)
        .filter(
            RoverAssessment.mission_id == mission_id
        )
        .all()
    )