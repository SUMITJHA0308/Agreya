from fastapi import FastAPI

from app.database import Base, engine
from app.mqtt.client import start_mqtt
# Import all models so SQLAlchemy knows the tables
from app.models import (
    Node,
    SensorReading,
    Alert,
    Worker,
    Helmet,
    WorkerLocation,
    Rover,
    Mission,
    RoverAssessment
)

from app.routes import (
    sensors,
    nodes,
    alerts,
    workers,
    helmets,
    locations,
    rover,
    missions,
    rover_assessment
)


app = FastAPI(
    title="Smart Mine Safety System",
    description="Complete mine monitoring, rescue rover and worker safety backend",
    version="1.0.0"
)


# Create SQLite tables
Base.metadata.create_all(bind=engine)

mqtt_client = start_mqtt()


# Routes
app.include_router(sensors.router)
app.include_router(nodes.router)
app.include_router(alerts.router)

app.include_router(workers.router)
app.include_router(helmets.router)
app.include_router(locations.router)

app.include_router(rover.router)
app.include_router(missions.router)
app.include_router(rover_assessment.router)


@app.get("/")
def root():
    return {
        "message": "Smart Mine Safety System Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }