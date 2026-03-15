from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


def build_vector_db():
    folder = "knowledge"  # Define the folder path
    docs = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        print("Loading file:", file)

        if file.endswith(".txt"):
            docs.extend(TextLoader(path).load())

        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())

    print("Total docs loaded:", len(docs))
        


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    splits = splitter.split_documents(docs)

    # ⭐ HuggingFace embeddings (stable)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(splits, embeddings)
    db.save_local("faiss_index")
