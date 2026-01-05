from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(documents):
    """
    Splits a list of Document objects into smaller chunks.
    """
    if not documents:
        print("No documents to chunk.")
        return []

    print(f"Chunking {len(documents)} documents...")

    # 1. Initialize the splitter using our settings
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""] # Try to split by paragraphs first
    )

    # 2. Split the documents
    chunks = text_splitter.split_documents(documents)
    
    print(f"Split into {len(chunks)} chunks.")
    return chunks

# Test block
if __name__ == "__main__":
    # We need to load docs first to test chunking
    from ingestion.pdf_loader import load_all_pdfs
    
    raw_docs = load_all_pdfs()
    chunked_docs = chunk_documents(raw_docs)
    
    # Print the first chunk to see what it looks like
    if chunked_docs:
        print("\n--- SAMPLE CHUNK 1 ---")
        print(chunked_docs[0].page_content)
        print("----------------------")