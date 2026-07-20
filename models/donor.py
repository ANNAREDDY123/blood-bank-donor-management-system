from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Donor(Base):

    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    blood_group = Column(
        String(10),
        nullable=False
    )

    phone = Column(
        String(15),
        unique=True,
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    last_donation_date = Column(
        Date,
        nullable=True
    )

    is_eligible = Column(
        Boolean,
        default=True
    )
