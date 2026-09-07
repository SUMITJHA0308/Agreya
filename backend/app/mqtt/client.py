import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC = "mine/+/sensors"


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("MQTT connected")

    client.subscribe(TOPIC)

    print(f"Subscribed to: {TOPIC}")


def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()

        print(
            f"MQTT DATA | "
            f"Topic: {message.topic} | "
            f"Data: {payload}"
        )

        data = json.loads(payload)

        print("Parsed sensor data:")
        print(data)

    except Exception as e:
        print("MQTT message error:", e)


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