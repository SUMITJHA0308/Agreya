from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.worker import Worker
from app.schemas.worker import WorkerCreate

router = APIRouter(
    prefix="/api/workers",
    tags=["Workers"]
)


@router.post("/")
def create_worker(
    data: WorkerCreate,
    db: Session = Depends(get_db)
):

    worker = Worker(
        worker_id=data.worker_id,
        name=data.name,
        helmet_id=data.helmet_id
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker


@router.get("/")
def get_workers(
    db: Session = Depends(get_db)
):

    return db.query(Worker).all()


@router.get("/{worker_id}")
def get_worker(
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

    return worker