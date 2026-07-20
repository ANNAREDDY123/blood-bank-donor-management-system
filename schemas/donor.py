from datetime import date

from pydantic import BaseModel
from pydantic import Field


class DonorCreate(BaseModel):

    name: str = Field(..., min_length=2, max_length=100)

    age: int = Field(..., ge=18, le=65)

    blood_group: str

    phone: str = Field(..., min_length=10, max_length=10)

    city: str = Field(..., min_length=2)

    last_donation_date: date | None = None

    is_eligible: bool = True


class DonorResponse(DonorCreate):

    id: int

    class Config:
        from_attributes = True
