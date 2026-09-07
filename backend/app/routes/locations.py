from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.worker import Worker
from app.models.worker_location import WorkerLocation
from app.schemas.location import WorkerLocationUpdate

router = APIRouter(
    prefix="/api/locations",
    tags=["Worker Location"]
)


@router.post("/")
def update_location(
    data: WorkerLocationUpdate,
    db: Session = Depends(get_db)
):

    location = WorkerLocation(
        worker_id=data.worker_id,
        node_id=data.node_id,
        signal_strength=data.signal_strength
    )

    db.add(location)

    worker = db.query(Worker).filter(
        Worker.worker_id == data.worker_id
    ).first()

    if worker:
        worker.last_node_id = data.node_id
        worker.last_seen = datetime.utcnow()

    db.commit()

    return {
        "message": "Worker location updated",
        "worker_id": data.worker_id,
        "last_node": data.node_id
    }


@router.get("/{worker_id}")
def get_location(
    worker_id: str,
    db: Session = Depends(get_db)
):

    worker = db.query(Worker).filter(
        Worker.worker_id == worker_id
    ).first()

    if not worker:
        return {
            "message": "Worker not found"
        }

    return {
        "worker_id": worker.worker_id,
        "last_node": worker.last_node_id,
        "last_seen": worker.last_seen
    }