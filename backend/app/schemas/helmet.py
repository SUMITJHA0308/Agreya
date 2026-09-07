from pydantic import BaseModel


class HelmetSOS(BaseModel):
    helmet_id: str
    worker_id: str
    node_id: str | None = None
    message: str = "Worker SOS"


class HelmetStatus(BaseModel):
    helmet_id: str
    worker_id: str
    battery: int
    status: str