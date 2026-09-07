from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sensor import SensorData
from app.services.sensor_service import process_sensor_data


router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"]
)


@router.post("/data")
def receive_sensor_data(
    data: SensorData,
    db: Session = Depends(get_db)
):
    return process_sensor_data(
        db=db,
        node_id=data.node_id,
        mq2=data.mq2,
        ultrasonic=data.ultrasonic,
        ir=data.ir
    )