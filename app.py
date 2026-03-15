# ==============================
# IMPORTS
# ==============================
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# LangChain / RAG
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Agents
from agents.coordinator_agent import create_coordinator_agent

# Vision (Groq)
from groq import Groq


# ==============================
# LOAD ENVIRONMENT VARIABLES
# ==============================
load_dotenv()


# ==============================
# GROQ CLIENT (VISION)
# ==============================
client = Groq(api_key=os.getenv("GROQ_API_KEY_1"))


# ==============================
# EMBEDDINGS MODEL
# ==============================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==============================
# LOAD FAISS VECTOR DATABASE
# ==============================
db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 3})


# ==============================
# LLM (GROQ)
# ==============================
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


# ==============================
# LANGGRAPH AGENT
# ==============================
coordinator_agent = create_coordinator_agent(llm, retriever)


# ==============================
# FASTAPI APP
# ==============================
app = FastAPI()


# ==============================
# REQUEST MODEL
# ==============================
class Query(BaseModel):
    question: str


# ==============================
# TEXT QUESTION ENDPOINT
# ==============================
@app.post("/ask")
def ask_question(query: Query):

    result = coordinator_agent.invoke({
        "question": query.question,
        "image": None
    })

    return {"answer": result["answer"]}


# ==============================
# IMAGE + QUESTION ENDPOINT
# ==============================
@app.post("/image-question")
async def image_question(
    file: UploadFile = File(None),
    question: str = Form(...)
):

    image_bytes = None

    if file is not None:
        image_bytes = await file.read()

    result = coordinator_agent.invoke({
        "question": question,
        "image": image_bytes
    })

    return {"answer": result["answer"]}


# ==============================
# HEALTH CHECK
# ==============================
@app.get("/")
def home():
    return {"message": "Farmer AI Bot API is running"}