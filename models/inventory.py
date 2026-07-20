from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    blood_group = Column(
        String(10),
        nullable=False
    )

    units_available = Column(
        Integer,
        nullable=False
    )

    expiry_date = Column(
        Date,
        nullable=False
    )

    storage_location = Column(
        String(100),
        nullable=False
    )
