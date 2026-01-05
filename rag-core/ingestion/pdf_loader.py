import os
from langchain_community.document_loaders import PyPDFLoader
from config.settings import RAW_DATA_DIR

def load_all_pdfs():
    """
    Scans the data/raw folder and loads all PDFs.
    Returns a list of Document objects.
    """
    documents = []
    
    # 1. List all files in the raw data folder
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.pdf')]
    
    if not files:
        print(f"No PDFs found in {RAW_DATA_DIR}")
        return []

    print(f"Found {len(files)} PDFs. Loading...")

    # 2. Loop through each file and load it
    for file_name in files:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        
        # 3. Use LangChain's loader
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        documents.extend(docs)
        print(f"Loaded: {file_name}")

    return documents

# Simple test block to run this file directly
if __name__ == "__main__":
    loaded_docs = load_all_pdfs()
    print(f"\nTotal pages loaded: {len(loaded_docs)}")