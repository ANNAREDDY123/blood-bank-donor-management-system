from datetime import date
from datetime import timedelta


VALID_STATUS = [
    "Pending",
    "Approved",
    "Rejected",
    "Completed"
]


def valid_request_status(status: str):

    return status in VALID_STATUS


def valid_request_date(request_date):

    return request_date >= date.today()


def donor_is_eligible(last_donation_date):

    if last_donation_date is None:
        return True

    next_eligible_date = last_donation_date + timedelta(days=90)

    return date.today() >= next_eligible_date


def inventory_available(
    available_units,
    requested_units
):

    return available_units >= requested_units


def blood_not_expired(expiry_date):

    return expiry_date >= date.today()
