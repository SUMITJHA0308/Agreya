from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db

from app.models.helmet import Helmet
from app.models.worker import Worker
from app.models.alert import Alert

from app.schemas.helmet import HelmetSOS, HelmetStatus

from app.services.mission_service import create_emergency_mission


router = APIRouter(
    prefix="/api/helmets",
    tags=["Helmets"]
)


# =========================================================
# WORKER HELMET SOS
# =========================================================

@router.post("/sos")
def helmet_sos(
    data: HelmetSOS,
    db: Session = Depends(get_db)
):

    # -----------------------------------------
    # 1. Find worker
    # -----------------------------------------

    worker = db.query(Worker).filter(
        Worker.worker_id == data.worker_id
    ).first()

    if worker:

        worker.status = "SOS"

        worker.last_node_id = data.node_id

        worker.last_seen = datetime.utcnow()


    # -----------------------------------------
    # 2. Create critical alert
    # -----------------------------------------

    alert = Alert(
        node_id=data.node_id or "UNKNOWN",
        alert_type="WORKER_SOS",
        severity="CRITICAL",
        message=data.message
    )

    db.add(alert)

    db.flush()


    # -----------------------------------------
    # 3. Automatically create rover mission
    # -----------------------------------------

    mission = create_emergency_mission(
        db=db,
        node_id=data.node_id,
        worker_id=data.worker_id,
        reason="WORKER_SOS"
    )


    # -----------------------------------------
    # 4. Save everything
    # -----------------------------------------

    db.commit()


    # -----------------------------------------
    # 5. Response
    # -----------------------------------------

    return {
        "message": "SOS received",

        "worker_id": data.worker_id,

        "node_id": data.node_id,

        "status": "CRITICAL",

        "mission_id": (
            mission.mission_id
            if mission
            else None
        ),

        "rover_status": (
            "ASSIGNED"
            if mission
            else "NO_ROVER_AVAILABLE"
        )
    }


# =========================================================
# HELMET STATUS
# =========================================================

@router.post("/status")
def update_helmet_status(
    data: HelmetStatus,
    db: Session = Depends(get_db)
):

    # -----------------------------------------
    # 1. Find helmet
    # -----------------------------------------

    helmet = db.query(Helmet).filter(
        Helmet.helmet_id == data.helmet_id
    ).first()


    # -----------------------------------------
    # 2. Create helmet if not registered
    # -----------------------------------------

    if not helmet:

        helmet = Helmet(
            helmet_id=data.helmet_id,
            worker_id=data.worker_id
        )

        db.add(helmet)


    # -----------------------------------------
    # 3. Update helmet information
    # -----------------------------------------

    helmet.battery = data.battery

    helmet.status = data.status

    helmet.last_seen = datetime.utcnow()


    # -----------------------------------------
    # 4. Save
    # -----------------------------------------

    db.commit()

    db.refresh(helmet)


    return {
        "message": "Helmet status updated",

        "helmet_id": helmet.helmet_id,

        "worker_id": helmet.worker_id,

        "battery": helmet.battery,

        "status": helmet.status
    }