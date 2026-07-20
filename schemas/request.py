from datetime import date

from pydantic import BaseModel
from pydantic import Field


class RequestCreate(BaseModel):

    hospital_name: str = Field(..., min_length=2)

    blood_group: str

    units_required: int = Field(..., gt=0)

    request_date: date

    status: str


class RequestResponse(RequestCreate):

    id: int

    class Config:
        from_attributes = True
