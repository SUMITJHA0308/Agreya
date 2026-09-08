from datetime import datetime
from sqlalchemy.orm import Session

from app.models.node import Node
from app.models.sensor_reading import SensorReading
from app.models.alert import Alert

from app.services.mission_service import create_emergency_mission


def process_sensor_data(
    db: Session,
    node_id: str,
    mq2: float | None = None,
    mq7: float | None = None,
    vibration: int | None = None,
    ultrasonic: float | None = None,
    status: str | None = None,
    helmet_sos: bool = False,
    helmet_id: str | None = None
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
    #
    # NODE 1:
    # MQ2 >= 600  -> YELLOW
    # MQ2 >= 1000 -> RED
    # MQ7 >= 600  -> YELLOW
    # MQ7 >= 1000 -> RED
    # Vibration    -> RED
    # Helmet SOS    -> RED
    #
    # NODE 2:
    # Distance <= 15 cm -> RED
    # Distance <= 18 cm -> YELLOW
    #

    calculated_status = "GREEN"

    # Helmet SOS is always critical
    if helmet_sos:
        calculated_status = "RED"

    # Vibration is critical
    elif vibration == 1:
        calculated_status = "RED"

    # MQ2 / MQ7 gas levels
    elif (
        (mq2 is not None and mq2 >= 1000)
        or
        (mq7 is not None and mq7 >= 1000)
    ):
        calculated_status = "RED"

    elif (
        (mq2 is not None and mq2 >= 600)
        or
        (mq7 is not None and mq7 >= 600)
    ):
        calculated_status = "YELLOW"

    # Node 2 ultrasonic
    elif ultrasonic is not None and ultrasonic <= 15:
        calculated_status = "RED"

    elif ultrasonic is not None and ultrasonic <= 18:
        calculated_status = "YELLOW"

    # --------------------------------
    # USE DEVICE STATUS ONLY IF NEEDED
    # --------------------------------

    if status in ["GREEN", "YELLOW", "RED"]:
        # Never downgrade a locally detected critical condition
        if calculated_status == "RED":
            final_status = "RED"

        elif calculated_status == "YELLOW":
            final_status = "YELLOW"

        else:
            final_status = status

    else:
        final_status = calculated_status

    # --------------------------------
    # SAVE SENSOR READING
    # --------------------------------

    reading = SensorReading(
        node_id=node_id,
        mq2=mq2,
        mq7=mq7,
        ultrasonic=ultrasonic,
        vibration=vibration,
        status=final_status
    )

    db.add(reading)

    # --------------------------------
    # UPDATE NODE
    # --------------------------------

    node.status = final_status
    node.last_seen = datetime.utcnow()

    mission = None

    # --------------------------------
    # CREATE ALERT
    # --------------------------------

    if final_status == "RED":

        # Determine alert value
        if helmet_sos:
            alert_value = None
            alert_type = "HELMET_SOS"
            message = (
                f"Emergency SOS received from "
                f"{helmet_id or 'helmet'} at {node_id}"
            )

        elif vibration == 1:
            alert_value = 1
            alert_type = "VIBRATION_ALERT"
            message = (
                f"High vibration detected at {node_id}"
            )

        elif (
            (mq2 is not None and mq2 >= 1000)
            or
            (mq7 is not None and mq7 >= 1000)
        ):
            alert_value = (
                mq2
                if mq2 is not None and mq2 >= 1000
                else mq7
            )
            alert_type = "GAS_ALERT"
            message = (
                f"Critical gas level detected at {node_id}"
            )

        elif ultrasonic is not None and ultrasonic <= 15:
            alert_value = ultrasonic
            alert_type = "ROOF_STABILITY_ALERT"
            message = (
                f"Critical roof stability detected at {node_id}"
            )

        else:
            alert_value = None
            alert_type = "SENSOR_ALERT"
            message = (
                f"Critical condition detected at {node_id}"
            )

        alert = Alert(
            node_id=node_id,
            alert_type=alert_type,
            severity="CRITICAL",
            value=alert_value,
            message=message
        )

        db.add(alert)
        db.flush()

        # --------------------------------
        # CREATE RESCUE ROVER MISSION
        # --------------------------------

        mission = create_emergency_mission(
            db=db,
            node_id=node_id,
            reason=alert_type,
            destination_x=node.location_x,
            destination_y=node.location_y
        )

    # --------------------------------
    # SAVE CHANGES
    # --------------------------------

    db.commit()

    # --------------------------------
    # RESPONSE
    # --------------------------------

    return {
        "success": True,
        "message": "Sensor data processed",
        "node_id": node_id,

        "zone": node.zone,
        "location": node.location,
        "location_x": node.location_x,
        "location_y": node.location_y,

        "mq2": mq2,
        "mq7": mq7,
        "vibration": vibration,
        "ultrasonic": ultrasonic,

        "helmet_sos": helmet_sos,
        "helmet_id": helmet_id,

        "status": final_status,

        "rover_mission": (
            mission.mission_id
            if mission
            else None
        )
    }