from datetime import date

from pydantic import BaseModel
from pydantic import Field


class InventoryCreate(BaseModel):

    blood_group: str

    units_available: int = Field(..., ge=0)

    expiry_date: date

    storage_location: str = Field(..., min_length=2)


class InventoryResponse(InventoryCreate):

    id: int

    class Config:
        from_attributes = True
