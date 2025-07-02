import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.v1 import auth, admin
from alembic import command
from alembic.config import Config
from mangum import Mangum
from contextlib import asynccontextmanager

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield

app = FastAPI(lifespan=lifespan, debug=True)
handler = Mangum(app)

# CORS allowances
origins = [
    os.getenv("FRONT_END_DOMAIN")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Portfolio API"}

@app.get("/health", tags=['Health'])
async def health_check():
    return {"health": True}
