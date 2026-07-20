# blood-bank-donor-management-system
FastAPI Blood Bank &amp; Donor Management System with JWT Authentication, Donor Management, Blood Inventory, Blood Request Management, Reports, Search, SQLAlchemy ORM, Pagination, Logging, Docker Support, and Unit Tests.
# Blood Bank & Donor Management System

## Features

- JWT Authentication
- Role-Based Authorization
- Donor Management
- Blood Inventory
- Blood Request Management
- Reports & Search
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Logging
- Unit Test Structure


## Installation


pip install -r requirements.txt


## Run Project


py -m uvicorn main:app --reload


Swagger:


http://127.0.0.1:8000/docs


## Environment Variables


DATABASE_URL=sqlite:///./blood_bank.db
SECRET_KEY=blood_bank_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440


## Business Rules

- Donor cannot donate again within 90 days.
- Age must be between 18 and 65.
- Phone number must be unique.
- Expired blood cannot be allocated.
- Blood cannot be issued if stock is insufficient.
- Inventory updates automatically after request approval.



## Docker


docker build -t blood-bank-system .
docker run -p 8000:8000 blood-bank-system
