# rag_loader.py

import pickle
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever


# -----------------------------
# LOAD EMBEDDINGS
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# LOAD FAISS (VECTOR)
# -----------------------------
db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

vector_retriever = db.as_retriever(search_kwargs={"k": 3})


# -----------------------------
# LOAD BM25
# -----------------------------
with open("splits.pkl", "rb") as f:
    splits = pickle.load(f)

bm25 = BM25Retriever.from_documents(splits)
bm25.k = 5


# -----------------------------
# 🔥 HYBRID SEARCH FUNCTION
# -----------------------------
def hybrid_search(query):

    vector_docs = vector_retriever.invoke(query)
    bm25_docs = bm25.invoke(query)

    all_docs = vector_docs + bm25_docs

    # remove duplicates
    unique_docs = list({d.page_content: d for d in all_docs}.values())

    return unique_docs[:5]