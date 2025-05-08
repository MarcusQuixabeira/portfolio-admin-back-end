from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.v1 import auth, admin

# CORS allowances
origins = [
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/health", tags=['Health'])
async def helth_check():
    return {"health": True}
