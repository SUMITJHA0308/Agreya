from datetime import datetime
from sqlalchemy.orm import Session

from app.models.node import Node
from app.models.sensor_reading import SensorReading
from app.models.alert import Alert

from app.services.mission_service import create_emergency_mission


def process_sensor_data(
    db: Session,
    node_id: str,
    mq2: float,
    ultrasonic: float,
    ir: int
):
    # --------------------------------
    # FIND NODE
    # --------------------------------

    node = db.query(Node).filter(
        Node.node_id == node_id
    ).first()

    if not node:
        return {
            "success": False,
            "message": "Node not found",
            "node_id": node_id
        }

    # --------------------------------
    # DETERMINE STATUS
    # --------------------------------

    if mq2 >= 800:
        status = "RED"

    elif ultrasonic <= 30:
        status = "RED"

    elif mq2 >= 500:
        status = "YELLOW"

    elif ultrasonic <= 60:
        status = "YELLOW"

    else:
        status = "GREEN"

    # --------------------------------
    # SAVE SENSOR READING
    # --------------------------------

    reading = SensorReading(
        node_id=node_id,
        mq2=mq2,
        ultrasonic=ultrasonic,
        ir=ir,
        status=status
    )

    db.add(reading)

    # --------------------------------
    # UPDATE NODE
    # --------------------------------

    node.status = status
    node.last_seen = datetime.utcnow()

    mission = None

    # --------------------------------
    # CREATE ALERT
    # --------------------------------

    if status == "RED":

        alert = Alert(
            node_id=node_id,
            alert_type="SENSOR_ALERT",
            severity="CRITICAL",
            value=mq2,
            message=f"Critical condition detected at {node_id}"
        )

        db.add(alert)
        db.flush()

        # --------------------------------
        # CREATE ROVER MISSION
        # --------------------------------

        mission = create_emergency_mission(
            db=db,
            node_id=node_id,
            reason="NODE_SENSOR_ALERT",
            destination_x=node.location_x,
            destination_y=node.location_y
        )

    # --------------------------------
    # COMMIT
    # --------------------------------

    db.commit()

    return {
        "success": True,
        "message": "Sensor data processed",
        "node_id": node_id,
        "zone": node.zone,
        "location": node.location,
        "location_x": node.location_x,
        "location_y": node.location_y,
        "mq2": mq2,
        "ultrasonic": ultrasonic,
        "ir": ir,
        "status": status,
        "rover_mission": (
            mission.mission_id
            if mission
            else None
        )
    }