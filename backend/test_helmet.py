import json
import time

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC = "mine/helmet/HELMET_01/sos"


data = {
    "helmet_id": "HELMET_01",
    "worker_id": "WORKER_01",
    "node_id": "NODE_1",
    "sos": True,
    "timestamp": int(time.time())
}


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(
    BROKER_HOST,
    BROKER_PORT,
    60
)

client.publish(
    TOPIC,
    json.dumps(data)
)

print()
print("HELMET SOS TEST SENT")
print("Topic:", TOPIC)
print(
    "Data:",
    json.dumps(data)
)

time.sleep(1)

client.disconnect()