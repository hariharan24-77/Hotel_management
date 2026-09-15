from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from app.database import Base, engine
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Management System - Auth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # restrict this in production, e.g. ["http://localhost:5500"]
=======

from app.routers import users
from app.routers import media
from app.core.exception_handler import app_exception_handler

from app.exceptions.custom import AppException

from app.database.connection import AsyncSessionLocal

from app.database.seed import seed_roles

from app.routers import auth
from app.routers import dashboard
from app.routers import staff
from app.routers import room_types
from app.routers import rooms
from app.routers import guests
from app.routers import reservations
from app.routers import operations
from app.routers import billing
from app.routers import reports
from app.routers import settings


app=FastAPI(
    title="Hotel Management System API",
    version="1.0.0"
)


app.include_router(
    auth.router
)

app.include_router(dashboard.router)
app.include_router(staff.router)
app.include_router(room_types.router)
app.include_router(rooms.router)
app.include_router(guests.router)
app.include_router(reservations.router)
app.include_router(operations.router)
app.include_router(billing.router)
app.include_router(reports.router)
app.include_router(settings.router)


@app.get("/")
async def root():

    return {
        "message":
        "Hotel Management System API Running"
    }


@app.on_event("startup")
async def startup_event():

    async with AsyncSessionLocal() as db:

        await seed_roles(db)


app.include_router(
    users.router
)

app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.include_router(
    media.router
)

# The frontend is served separately during development, so browser requests
# need explicit CORS permission (including OPTIONS preflight requests).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "null",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
>>>>>>> sakthi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
<<<<<<< HEAD

app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "running"}
=======
>>>>>>> sakthi
