import json
import time
import paho.mqtt.client as mqtt

data = {
    "node_id": "NODE_01",
    "mq2": 900,
    "ultrasonic": 100,
    "ir": 0
}

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect("localhost", 1883, 60)

client.publish(
    "mine/NODE_01/sensors",
    json.dumps(data)
)

print("MQTT test data sent:")
print(json.dumps(data))

time.sleep(1)

client.disconnect()
