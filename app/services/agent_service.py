# ==============================
# IMPORTS
# ==============================
import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from agents.coordinator_agent import create_coordinator_agent

# ✅ DATABASE IMPORTS
from app.db.database import SessionLocal
from app.db.models import ChatHistory


# ==============================
# LOAD ENV
# ==============================
load_dotenv()


# ==============================
# EMBEDDINGS
# ==============================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==============================
# LOAD FAISS
# ==============================
db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 3})


# ==============================
# LLM
# ==============================
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


# ==============================
# AGENT
# ==============================
coordinator_agent = create_coordinator_agent(llm, retriever)


# ==============================
# SERVICE FUNCTIONS
# ==============================

# 🔥 TEXT QUERY
def handle_text_query(question: str, user_id: int):
    # 1️⃣ Call Agent (AI processing)
    result = coordinator_agent.invoke({
        "question": question,
        "image": None
    })

    # 2️⃣ Extract answer safely
    answer = result.get("answer", "No response generated")

    # 3️⃣ Save to database
    db = SessionLocal()
    try:
        chat = ChatHistory(
            question=question,
            answer=answer,
            user_id=user_id
        )
        db.add(chat)
        db.commit()
    finally:
        db.close()

    # 4️⃣ Return response
    return answer


# 🔥 IMAGE QUERY
def handle_image_query(question: str, image_bytes, user_id: int):
    # 1️⃣ Call Agent (AI processing)
    result = coordinator_agent.invoke({
        "question": question,
        "image": image_bytes
    })

    # 2️⃣ Extract answer safely
    answer = result.get("answer", "No response generated")

    # 3️⃣ Save to database
    db = SessionLocal()
    try:
        chat = ChatHistory(
            question=question,
            answer=answer,
            user_id=user_id   # ✅ link to user
        )
        db.add(chat)
        db.commit()
    finally:
        db.close()

    # 4️⃣ Return response
    return answer