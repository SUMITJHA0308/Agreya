from pydantic import BaseModel


class NodeCreate(BaseModel):
    node_id: str
    location: str
    zone: str
    location_x: float
    location_y: float


class NodeResponse(BaseModel):
    node_id: str
    location: str | None = None
    zone: str | None = None
    location_x: float | None = None
    location_y: float | None = None
    status: str