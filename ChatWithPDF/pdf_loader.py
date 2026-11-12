from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

MAX_PDF_SIZE_BYTES = 10 * 1024 * 1024
MAX_PDF_PAGES = 50
CHUNK_BATCH_SIZE = 32
MAX_CHUNKS = 300

def build_index(pdf_path):
    import os

    if os.path.getsize(pdf_path) > MAX_PDF_SIZE_BYTES:
        raise ValueError("PDF is too large. Please upload a file under 10 MB.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    embedder = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db = Chroma(embedding_function=embedder)
    batch = []
    chunk_count = 0
    page_count = 0
    for page in PyPDFLoader(pdf_path).lazy_load():
        page_count += 1
        if page_count > MAX_PDF_PAGES:
            raise ValueError("PDF has more than 50 pages. Please upload a shorter document.")
        for chunk in splitter.split_documents([page]):
            chunk_count += 1
            if chunk_count > MAX_CHUNKS:
                raise ValueError("PDF contains too much text to index on this service.")
            batch.append(chunk)
            if len(batch) == CHUNK_BATCH_SIZE:
                db.add_documents(batch)
                batch = []

    if batch:
        db.add_documents(batch)
    if not chunk_count:
        raise ValueError("No readable text was found in the PDF.")

    return db