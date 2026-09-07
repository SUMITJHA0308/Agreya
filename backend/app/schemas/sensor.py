from pydantic import BaseModel


class SensorData(BaseModel):
    node_id: str
    mq2: float
    ultrasonic: float
    ir: int


class SensorResponse(BaseModel):
    message: str
    node_id: str
    status: str