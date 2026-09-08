from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.worker import Worker

from app.services.mission_service import (
    create_emergency_mission
)


# =====================================================
# PROCESS HELMET SOS
# =====================================================

def process_helmet_sos(
    db: Session,
    helmet_id: str,
    worker_id: str,
    node_id: str | None = None
):
    # =================================================
    # FIND WORKER
    # =================================================

    worker = (
        db.query(Worker)
        .filter(
            Worker.worker_id == worker_id
        )
        .first()
    )


    # =================================================
    # UPDATE WORKER STATUS
    # =================================================

    if worker:

        worker.status = "EMERGENCY"

        worker.last_node_id = node_id


    # =================================================
    # CREATE CRITICAL ALERT
    # =================================================

    alert = Alert(
        node_id=node_id or "UNKNOWN",

        alert_type="HELMET_SOS",

        severity="CRITICAL",

        value=None,

        message=(
            f"Emergency SOS received from "
            f"{worker_id} "
            f"({helmet_id})"
        ),

        resolved="NO"
    )

    db.add(alert)

    db.flush()


    # =================================================
    # CREATE RESCUE ROVER MISSION
    # =================================================

    mission = create_emergency_mission(
        db=db,
        node_id=node_id,
        worker_id=worker_id,
        reason="HELMET_SOS"
    )


    # =================================================
    # COMMIT DATABASE CHANGES
    # =================================================

    db.commit()


    # =================================================
    # RESPONSE
    # =================================================

    return {
        "success": True,

        "helmet_id": helmet_id,

        "worker_id": worker_id,

        "node_id": node_id,

        "worker_status": (
            worker.status
            if worker
            else "WORKER_NOT_FOUND"
        ),

        "alert_id": alert.id,

        "rover_mission": (
            mission.mission_id
            if mission
            else None
        )
    }