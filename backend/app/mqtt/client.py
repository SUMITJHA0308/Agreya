import json

import paho.mqtt.client as mqtt

from app.database import SessionLocal
from app.services.sensor_service import process_sensor_data


BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC = "mine/+/sensors"


def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties=None
):

    print("MQTT connected")

    client.subscribe(TOPIC)

    print(
        f"Subscribed to: {TOPIC}"
    )


def on_message(
    client,
    userdata,
    message
):

    db = SessionLocal()

    try:

        payload = message.payload.decode()

        print(
            f"MQTT DATA | "
            f"Topic: {message.topic} | "
            f"Data: {payload}"
        )

        data = json.loads(payload)

        node_id = data["node_id"]
        mq2 = float(data["mq2"])
        ultrasonic = float(data["ultrasonic"])
        ir = int(data["ir"])

        result = process_sensor_data(
            db=db,
            node_id=node_id,
            mq2=mq2,
            ultrasonic=ultrasonic,
            ir=ir
        )

        print(
            "Sensor processing result:",
            result
        )

    except Exception as e:

        db.rollback()

        print(
            "MQTT message error:",
            e
        )

    finally:

        db.close()


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