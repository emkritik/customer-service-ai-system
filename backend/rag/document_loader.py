import os
from pypdf import PdfReader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdfs_from_directory(directory_path="../knowledge_base"):
    """Load all PDFs and return Document objects with chunks"""
    documents = []

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory {directory_path} not found")

    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]

    if not pdf_files:
        raise ValueError(f"No PDF files found in {directory_path}")

    print(f"Loading {len(pdf_files)} PDF files...")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory_path, pdf_file)
        print(f"Processing: {pdf_file}")

        reader = PdfReader(pdf_path)

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text.strip():
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": pdf_file,
                        "page": page_num
                    }
                )
                documents.append(doc)

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} pages")

    return chunks
