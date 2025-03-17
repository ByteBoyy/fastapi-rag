import os
from concurrent.futures import ThreadPoolExecutor
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_pdf(file_path):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

def process_all_pdfs(pdf_folder_path):
    pdf_files = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]
    chunks = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_pdf, pdf_files)
        for doc_chunks in results:
            chunks.extend(doc_chunks)
    return chunks
