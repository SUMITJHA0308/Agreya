from pydantic import BaseModel


class MissionCreate(BaseModel):
    node_id: str | None = None
    worker_id: str | None = None
    reason: str
    destination_x: float | None = None
    destination_y: float | None = None


class MissionStatusUpdate(BaseModel):
    status: str