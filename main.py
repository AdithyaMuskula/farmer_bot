from fastapi import FastAPI
from app.api.chat import router as chat_router

from app.db.database import engine
from app.db.models import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Farmer AI Backend")

app = FastAPI()

# ✅ ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)