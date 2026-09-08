import json

import paho.mqtt.client as mqtt

from app.database import SessionLocal

from app.services.sensor_service import (
    process_sensor_data
)

from app.services.alert_service import (
    process_helmet_sos
)


# =====================================================
# MQTT CONFIG
# =====================================================

BROKER_HOST = "localhost"
BROKER_PORT = 1883

SENSOR_TOPIC = "mine/+/sensors"

HELMET_SOS_TOPIC = (
    "mine/helmet/+/sos"
)


# =====================================================
# MQTT CONNECT
# =====================================================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties=None
):

    print("MQTT connected")

    # --------------------------------
    # NODE SENSOR DATA
    # --------------------------------

    client.subscribe(
        SENSOR_TOPIC
    )

    # --------------------------------
    # HELMET SOS
    # --------------------------------

    client.subscribe(
        HELMET_SOS_TOPIC
    )

    print(
        f"Subscribed to: {SENSOR_TOPIC}"
    )

    print(
        f"Subscribed to: {HELMET_SOS_TOPIC}"
    )


# =====================================================
# MQTT MESSAGE
# =====================================================

def on_message(
    client,
    userdata,
    message
):

    db = SessionLocal()

    try:

        payload = (
            message.payload
            .decode()
        )

        print()

        print(
            "MQTT DATA | "
            f"Topic: {message.topic} | "
            f"Data: {payload}"
        )

        data = json.loads(
            payload
        )


        # =================================================
        # HELMET SOS
        # =================================================

        if message.topic.startswith(
            "mine/helmet/"
        ):

            print(
                ">>> HELMET SOS MESSAGE DETECTED <<<"
            )

            helmet_id = data.get(
                "helmet_id"
            )

            worker_id = data.get(
                "worker_id"
            )

            node_id = data.get(
                "node_id"
            )

            sos = data.get(
                "sos",
                False
            )


            print(
                "Helmet ID:",
                helmet_id
            )

            print(
                "Worker ID:",
                worker_id
            )

            print(
                "Node ID:",
                node_id
            )

            print(
                "SOS:",
                sos
            )


            # --------------------------------
            # VALIDATION
            # --------------------------------

            if not helmet_id:

                print(
                    "Helmet SOS ERROR: "
                    "helmet_id missing"
                )

                return


            if not worker_id:

                print(
                    "Helmet SOS ERROR: "
                    "worker_id missing"
                )

                return


            if sos is not True:

                print(
                    "Helmet SOS ignored: "
                    "sos is not true"
                )

                return


            # --------------------------------
            # PROCESS HELMET SOS
            # --------------------------------

            result = process_helmet_sos(

                db=db,

                helmet_id=helmet_id,

                worker_id=worker_id,

                node_id=node_id
            )


            print()

            print(
                "Helmet SOS processing result:",
                result
            )


            # --------------------------------
            # DO NOT PROCESS AS SENSOR DATA
            # --------------------------------

            return


        # =================================================
        # NODE SENSOR DATA
        # =================================================

        node_id = data.get(
            "node_id"
        )


        if not node_id:

            print(
                "MQTT ERROR: "
                "node_id missing"
            )

            return


        # --------------------------------
        # SENSOR VALUES
        # --------------------------------

        mq2 = data.get(
            "mq2"
        )

        mq7 = data.get(
            "mq7"
        )

        vibration = data.get(
            "vibration"
        )

        ultrasonic = data.get(
            "ultrasonic"
        )

        status = data.get(
            "status"
        )

        helmet_sos = data.get(
            "helmet_sos",
            False
        )

        helmet_id = data.get(
            "helmet_id"
        )


        # --------------------------------
        # CONVERT TYPES
        # --------------------------------

        if mq2 is not None:

            mq2 = float(
                mq2
            )


        if mq7 is not None:

            mq7 = float(
                mq7
            )


        if vibration is not None:

            vibration = int(
                vibration
            )


        if ultrasonic is not None:

            ultrasonic = float(
                ultrasonic
            )


        # --------------------------------
        # PROCESS SENSOR DATA
        # --------------------------------

        result = process_sensor_data(

            db=db,

            node_id=node_id,

            mq2=mq2,

            mq7=mq7,

            vibration=vibration,

            ultrasonic=ultrasonic,

            status=status,

            helmet_sos=helmet_sos,

            helmet_id=helmet_id
        )


        print()

        print(
            "Sensor processing result:",
            result
        )


    # =================================================
    # JSON ERROR
    # =================================================

    except json.JSONDecodeError:

        db.rollback()

        print(
            "MQTT ERROR: "
            "Invalid JSON payload"
        )


    # =================================================
    # GENERAL ERROR
    # =================================================

    except Exception as e:

        db.rollback()

        print(
            "MQTT message error:",
            e
        )


    # =================================================
    # CLOSE DATABASE
    # =================================================

    finally:

        db.close()


# =====================================================
# START MQTT
# =====================================================

def start_mqtt():

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(
        BROKER_HOST,
        BROKER_PORT,
        60
    )

    client.loop_start()

    return client