from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import pickle


def build_vector_db():

    folder = "knowledge"
    docs = []

    # -----------------------------
    # CHECK FOLDER EXISTS
    # -----------------------------
    if not os.path.exists(folder):
        print("❌ Knowledge folder not found!")
        return

    files = os.listdir(folder)

    if not files:
        print("❌ No files found in knowledge folder!")
        return

    print("📂 Files found:", files)

    # -----------------------------
    # LOAD FILES
    # -----------------------------
    for file in files:
        path = os.path.join(folder, file)
        print("Loading file:", file)

        if file.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")
            loaded_docs = loader.load()

        elif file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            loaded_docs = loader.load()

        else:
            print("Skipping unsupported file:", file)
            continue

        # ✅ Add metadata
        for d in loaded_docs:
            d.metadata["source"] = file

        docs.extend(loaded_docs)

    print("Total raw docs:", len(docs))

    if len(docs) == 0:
        print("❌ No documents loaded!")
        return

    # -----------------------------
    # CLEAN TEXT
    # -----------------------------
    for d in docs:
        d.page_content = d.page_content.replace("\n", " ").strip()

    # -----------------------------
    # SPLITTING
    # -----------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    splits = splitter.split_documents(docs)

    print("Total chunks created:", len(splits))

    # -----------------------------
    # EMBEDDINGS
    # -----------------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # -----------------------------
    # FAISS VECTOR DB
    # -----------------------------
    db = FAISS.from_documents(splits, embeddings)

    # -----------------------------
    # SAVE FAISS
    # -----------------------------
    db.save_local("faiss_index")

    # -----------------------------
    # SAVE SPLITS (FOR BM25)
    # -----------------------------
    with open("splits.pkl", "wb") as f:
        pickle.dump(splits, f)

    print("✅ FAISS index created successfully!")
    print("✅ Splits saved for BM25!")


# -----------------------------
# RUN SCRIPT (VERY IMPORTANT)
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting RAG build...")
    build_vector_db()