from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from fastapi import Form

from app.db.database import SessionLocal
from app.db.models import ChatHistory, User
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token

from app.core.security import get_current_user
from fastapi import Depends

from app.services.agent_service import (
    handle_text_query,
    handle_image_query
)

router = APIRouter()


# ==============================
# REQUEST MODEL
# ==============================
class Query(BaseModel):
    question: str


# ==============================
# ASK TEXT QUESTION
# ==============================
@router.post("/ask")
def ask_question(query: Query, user_id: int = Depends(get_current_user)):
    answer = handle_text_query(query.question, user_id)
    return {"answer": answer}

# ==============================
# IMAGE + QUESTION
# ==============================
@router.post("/image-question")
async def image_question(
    file: UploadFile = File(None),
    question: str = Form(...),
    user_id: int = Depends(get_current_user)
):
    image_bytes = None

    if file:
        image_bytes = await file.read()

    answer = handle_image_query(question, image_bytes, user_id)
    return {"answer": answer}


# ==============================
# HEALTH CHECK
# ==============================
@router.get("/")
def health():
    return {"message": "Farmer AI Bot API is running"}


# ==============================
# GET USER CHAT HISTORY
# ==============================
@router.get("/history")
def get_history(user_id: int = Depends(get_current_user)):
    db = SessionLocal()

    chats = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).all()

    db.close()

    return [
        {
            "id": chat.id,
            "question": chat.question,
            "answer": chat.answer
        }
        for chat in chats
    ]


# ==============================
# SIGNUP
# ==============================
@router.post("/signup")
def signup(username: str, password: str):
    db = SessionLocal()

    # check if user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        return {"message": "User already exists"}

    # 🔒 hash password
    hashed_password = hash_password(password)

    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()

    db.close()

    return {"message": "User created"}

from fastapi import Form

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()

    user = db.query(User).filter(User.username == username).first()

    if not user:
        db.close()
        return {"message": "User not found"}

    if not verify_password(password, user.password):
        db.close()
        return {"message": "Incorrect password"}

    token = create_access_token({"user_id": user.id})

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }