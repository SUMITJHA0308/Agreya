from pydantic import BaseModel
class WorkerCreate(BaseModel):
    worker_id: str
    name: str
    helmet_id: str | None = None