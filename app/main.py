from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import models
from app.database import engine
from app.routers import auth, users, calculations

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (development-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(calculations.router)

# Static frontend
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

@app.get("/")
def read_root():
    return {"message": "FastAPI Calculator with BREAD"}
