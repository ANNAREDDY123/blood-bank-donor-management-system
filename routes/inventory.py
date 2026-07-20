from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.inventory import Inventory
from schemas.inventory import InventoryCreate
from services.blood_service import blood_not_expired

router = APIRouter(
    prefix="/inventory",
    tags=["Blood Inventory"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    if not blood_not_expired(
        inventory.expiry_date
    ):

        raise HTTPException(
            status_code=400,
            detail="Cannot add expired blood units."
        )

    db_inventory = Inventory(**inventory.dict())

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory


@router.get("/")
def get_inventory(
    blood_group: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Inventory)

    if blood_group:

        query = query.filter(
            Inventory.blood_group.contains(blood_group)
        )

    total = query.count()

    inventory = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": inventory
    }


@router.put("/{inventory_id}")
def update_inventory(
    inventory_id: int,
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    db_inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not db_inventory:

        raise HTTPException(
            status_code=404,
            detail="Inventory record not found."
        )

    if not blood_not_expired(
        inventory.expiry_date
    ):

        raise HTTPException(
            status_code=400,
            detail="Cannot store expired blood units."
        )

    db_inventory.blood_group = inventory.blood_group
    db_inventory.units_available = inventory.units_available
    db_inventory.expiry_date = inventory.expiry_date
    db_inventory.storage_location = inventory.storage_location

    db.commit()
    db.refresh(db_inventory)

    return db_inventory
