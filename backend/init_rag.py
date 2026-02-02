#!/usr/bin/env python3
"""Initialize RAG system by creating vector store from PDFs"""

import sys
sys.path.append('.')

from rag.vectorstore import create_vectorstore
from database.db import init_db

def main():
    print("=" * 60)
    print("Initializing Customer Service Support System")
    print("=" * 60)

    # Initialize database
    print("\n[1/2] Initializing database...")
    init_db()
    print("✓ Database initialized")

    # Create vector store
    print("\n[2/2] Creating vector store from PDFs...")
    try:
        vectorstore = create_vectorstore()
        print("✓ Vector store created successfully")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Please place your PDF files in the knowledge_base/ directory")
        return

    print("\n" + "=" * 60)
    print("✓ Initialization complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start backend: cd backend && uvicorn api.main:app --reload")
    print("2. Open frontend/index.html in your browser")

if __name__ == "__main__":
    main()
