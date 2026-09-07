from pydantic import BaseModel


class RoverCreate(BaseModel):
    rover_id: str


class RoverStatusUpdate(BaseModel):
    rover_id: str
    status: str
    battery: float
    current_x: float
    current_y: float