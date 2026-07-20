from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.inventory import Inventory
from models.request import Request

from schemas.request import RequestCreate

from services.blood_service import (
    valid_request_status,
    valid_request_date,
    inventory_available,
    blood_not_expired
)

router = APIRouter(
    prefix="/requests",
    tags=["Blood Requests"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_request(
    request: RequestCreate,
    db: Session = Depends(get_db)
):

    if not valid_request_date(
        request.request_date
    ):

        raise HTTPException(
            status_code=400,
            detail="Request date cannot be in the past."
        )

    if not valid_request_status(
        request.status
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid request status."
        )

    inventory = db.query(Inventory).filter(
        Inventory.blood_group == request.blood_group
    ).first()

    if not inventory:

        raise HTTPException(
            status_code=404,
            detail="Blood group not available."
        )

    if not blood_not_expired(
        inventory.expiry_date
    ):

        raise HTTPException(
            status_code=400,
            detail="Blood units are expired."
        )

    if not inventory_available(
        inventory.units_available,
        request.units_required
    ):

        raise HTTPException(
            status_code=400,
            detail="Insufficient blood stock."
        )

    db_request = Request(**request.dict())

    if request.status == "Approved":

        inventory.units_available -= request.units_required

    db.add(db_request)

    db.commit()

    db.refresh(db_request)

    return db_request


@router.get("/")
def get_requests(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Request)

    if status:

        query = query.filter(
            Request.status == status
        )

    total = query.count()

    requests = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": requests
    }


@router.get("/{request_id}")
def get_request(
    request_id: int,
    db: Session = Depends(get_db)
):

    request = db.query(Request).filter(
        Request.id == request_id
    ).first()

    if not request:

        raise HTTPException(
            status_code=404,
            detail="Request not found."
        )

    return request


@router.put("/{request_id}")
def update_request(
    request_id: int,
    request: RequestCreate,
    db: Session = Depends(get_db)
):

    db_request = db.query(Request).filter(
        Request.id == request_id
    ).first()

    if not db_request:

        raise HTTPException(
            status_code=404,
            detail="Request not found."
        )

    db_request.hospital_name = request.hospital_name
    db_request.blood_group = request.blood_group
    db_request.units_required = request.units_required
    db_request.request_date = request.request_date
    db_request.status = request.status

    db.commit()

    return {
        "message": "Blood request updated successfully."
    }
