import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from .document_loader import load_pdfs_from_directory

PERSIST_DIRECTORY = "../chroma_db"

def create_vectorstore():
    """Create and persist vector store"""
    print("Loading documents...")
    chunks = load_pdfs_from_directory()

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Building vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    print(f"Vector store created and saved to {PERSIST_DIRECTORY}")
    return vectorstore

def load_vectorstore():
    """Load existing vector store"""
    if not os.path.exists(PERSIST_DIRECTORY):
        raise FileNotFoundError(f"Vector store not found. Run init_rag.py first")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

    return vectorstore

def search_knowledge_base(query, k=3):
    """Search the vector store"""
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return results
