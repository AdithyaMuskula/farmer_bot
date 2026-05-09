from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


# ==============================
# USER TABLE
# ==============================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


# ==============================
# CHAT HISTORY TABLE
# ==============================
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)

    # ✅ Link each chat to a user
    user_id = Column(Integer, ForeignKey("users.id"))