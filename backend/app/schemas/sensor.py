from pydantic import BaseModel


class SensorData(BaseModel):
    node_id: str

    # Node 1
    mq2: float | None = None
    mq7: float | None = None
    vibration: int | None = None

    # Node 2
    ultrasonic: float | None = None

    # Optional device status
    status: str | None = None

    # Helmet SOS
    helmet_sos: bool = False
    helmet_id: str | None = None


class SensorResponse(BaseModel):
    message: str
    node_id: str
    status: str