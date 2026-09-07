from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.node import Node
from app.models.sensor_reading import SensorReading
from app.models.alert import Alert

from app.services.mission_service import create_emergency_mission

from app.schemas.sensor import SensorData


router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"]
)


@router.post("/data")
def receive_sensor_data(
    data: SensorData,
    db: Session = Depends(get_db)
):

    # -----------------------------
    # FIND NODE
    # -----------------------------

    node = db.query(Node).filter(
        Node.node_id == data.node_id
    ).first()

    if not node:
        return {
            "message": "Node not found",
            "node_id": data.node_id
        }


    # -----------------------------
    # SENSOR STATUS
    # -----------------------------

    if data.mq2 >= 800:

        status = "RED"

    elif data.ultrasonic <= 30:

        status = "RED"

    elif data.mq2 >= 500:

        status = "YELLOW"

    elif data.ultrasonic <= 60:

        status = "YELLOW"

    else:

        status = "GREEN"


    # -----------------------------
    # SAVE SENSOR READING
    # -----------------------------

    reading = SensorReading(
        node_id=data.node_id,
        mq2=data.mq2,
        ultrasonic=data.ultrasonic,
        ir=data.ir,
        status=status
    )

    db.add(reading)


    # -----------------------------
    # UPDATE NODE STATUS
    # -----------------------------

    node.status = status


    # -----------------------------
    # UPDATE LAST SEEN
    # -----------------------------

    from datetime import datetime

    node.last_seen = datetime.utcnow()


    mission = None


    # -----------------------------
    # RED ALERT
    # -----------------------------

    if status == "RED":

        alert = Alert(
            node_id=data.node_id,
            alert_type="SENSOR_ALERT",
            severity="CRITICAL",
            value=data.mq2,
            message=f"Critical condition detected at {data.node_id}"
        )

        db.add(alert)

        db.flush()


        # -----------------------------
        # CREATE ROVER MISSION
        # -----------------------------

        mission = create_emergency_mission(
            db=db,
            node_id=data.node_id,
            reason="NODE_SENSOR_ALERT",
            destination_x=node.location_x,
            destination_y=node.location_y
        )


    # -----------------------------
    # SAVE EVERYTHING
    # -----------------------------

    db.commit()


    # -----------------------------
    # RESPONSE
    # -----------------------------

    return {

        "message": "Sensor data received",

        "node_id": data.node_id,

        "zone": node.zone,

        "location": node.location,

        "location_x": node.location_x,

        "location_y": node.location_y,

        "mq2": data.mq2,

        "ultrasonic": data.ultrasonic,

        "ir": data.ir,

        "status": status,

        "rover_mission": (
            mission.mission_id
            if mission
            else None
        )
    }