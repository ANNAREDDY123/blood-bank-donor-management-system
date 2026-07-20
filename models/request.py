from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Request(Base):

    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    hospital_name = Column(
        String(100),
        nullable=False
    )

    blood_group = Column(
        String(10),
        nullable=False
    )

    units_required = Column(
        Integer,
        nullable=False
    )

    request_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(30),
        default="Pending"
    )
