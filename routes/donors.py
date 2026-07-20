from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.donor import Donor
from schemas.donor import DonorCreate
from services.blood_service import donor_is_eligible

router = APIRouter(
    prefix="/donors",
    tags=["Donors"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_donor(
    donor: DonorCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Donor).filter(
        Donor.phone == donor.phone
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Phone number already exists."
        )

    eligible = donor_is_eligible(
        donor.last_donation_date
    )

    db_donor = Donor(
        name=donor.name,
        age=donor.age,
        blood_group=donor.blood_group,
        phone=donor.phone,
        city=donor.city,
        last_donation_date=donor.last_donation_date,
        is_eligible=eligible
    )

    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)

    return db_donor


@router.get("/")
def get_donors(
    blood_group: str = None,
    city: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Donor)

    if blood_group:
        query = query.filter(
            Donor.blood_group.contains(blood_group)
        )

    if city:
        query = query.filter(
            Donor.city.contains(city)
        )

    total = query.count()

    donors = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": donors
    }


@router.get("/{donor_id}")
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db)
):

    donor = db.query(Donor).filter(
        Donor.id == donor_id
    ).first()

    if not donor:

        raise HTTPException(
            status_code=404,
            detail="Donor not found."
        )

    return donor


@router.put("/{donor_id}")
def update_donor(
    donor_id: int,
    donor: DonorCreate,
    db: Session = Depends(get_db)
):

    db_donor = db.query(Donor).filter(
        Donor.id == donor_id
    ).first()

    if not db_donor:

        raise HTTPException(
            status_code=404,
            detail="Donor not found."
        )

    duplicate = db.query(Donor).filter(
        Donor.phone == donor.phone,
        Donor.id != donor_id
    ).first()

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Phone number already exists."
        )

    db_donor.name = donor.name
    db_donor.age = donor.age
    db_donor.blood_group = donor.blood_group
    db_donor.phone = donor.phone
    db_donor.city = donor.city
    db_donor.last_donation_date = donor.last_donation_date
    db_donor.is_eligible = donor_is_eligible(
        donor.last_donation_date
    )

    db.commit()
    db.refresh(db_donor)

    return db_donor


@router.delete("/{donor_id}")
def delete_donor(
    donor_id: int,
    db: Session = Depends(get_db)
):

    donor = db.query(Donor).filter(
        Donor.id == donor_id
    ).first()

    if not donor:

        raise HTTPException(
            status_code=404,
            detail="Donor not found."
        )

    db.delete(donor)
    db.commit()

    return {
        "message": "Donor deleted successfully."
    }
