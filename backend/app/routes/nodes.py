from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.node import Node
from app.schemas.node import NodeCreate

router = APIRouter(
    prefix="/api/nodes",
    tags=["Nodes"]
)


@router.post("/")
def create_node(
    data: NodeCreate,
    db: Session = Depends(get_db)
):
    existing_node = db.query(Node).filter(
        Node.node_id == data.node_id
    ).first()

    if existing_node:
        return {
            "message": "Node already exists",
            "node_id": existing_node.node_id
        }

    node = Node(
        node_id=data.node_id,
        location=data.location,
        zone=data.zone,
        location_x=data.location_x,
        location_y=data.location_y,
        status="OFFLINE",
        last_seen=datetime.utcnow()
    )

    db.add(node)
    db.commit()
    db.refresh(node)

    return node


@router.get("/")
def get_nodes(
    db: Session = Depends(get_db)
):
    return db.query(Node).all()


@router.get("/{node_id}")
def get_node(
    node_id: str,
    db: Session = Depends(get_db)
):
    node = db.query(Node).filter(
        Node.node_id == node_id
    ).first()

    if not node:
        return {
            "message": "Node not found"
        }

    return node