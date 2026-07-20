import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routes.auth import router as auth_router
from routes.donors import router as donors_router
from routes.inventory import router as inventory_router
from routes.requests import router as requests_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blood Bank & Donor Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(donors_router)
app.include_router(inventory_router)
app.include_router(requests_router)


@app.get("/")
def home():

    logger.info("Application Started Successfully")

    return {
        "message": "Blood Bank & Donor Management System"
    }
