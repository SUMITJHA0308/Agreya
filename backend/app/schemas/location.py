from pydantic import BaseModel


class WorkerLocationUpdate(BaseModel):
    worker_id: str
    node_id: str
    signal_strength: float | None = None