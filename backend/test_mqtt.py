import json
import time
import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883


def send_data(data):

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    client.connect(
        BROKER_HOST,
        BROKER_PORT,
        60
    )

    topic = f"mine/{data['node_id']}/sensors"

    client.publish(
        topic,
        json.dumps(data)
    )

    print("\nMQTT TEST DATA SENT")
    print("Topic:", topic)
    print("Data:", json.dumps(data))

    time.sleep(1)

    client.disconnect()


# ==========================================
# NODE 2 - GREEN
# distance > 18 cm
# ==========================================

send_data({
    "node_id": "NODE_2",
    "ultrasonic": 25,
    "status": "GREEN"
})


# ==========================================
# NODE 2 - YELLOW
# 15 < distance <= 18
# ==========================================

send_data({
    "node_id": "NODE_2",
    "ultrasonic": 17,
    "status": "YELLOW"
})


# ==========================================
# NODE 2 - RED
# distance <= 15
# ==========================================

send_data({
    "node_id": "NODE_2",
    "ultrasonic": 10,
    "status": "RED"
})