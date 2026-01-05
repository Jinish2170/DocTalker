import weaviate
from langchain_ollama import OllamaEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from config.settings import WEAVIATE_URL, WEAVIATE_INDEX_NAME, EMBEDDING_MODEL, OLLAMA_BASE_URL

def sanitize_metadata(chunks):
    """
    Weaviate does not allow dots (.) in property names.
    This function cleans the metadata keys of all chunks.
    Example: 'ptex.fullbanner' -> 'ptex_fullbanner'
    """
    for chunk in chunks:
        new_metadata = {}
        for key, value in chunk.metadata.items():
            # Replace invalid characters (like dots) with underscores
            clean_key = key.replace('.', '_')
            new_metadata[clean_key] = value
        chunk.metadata = new_metadata
    return chunks

def index_documents(chunks):
    if not chunks:
        print("No chunks to index.")
        return

    # --- NEW STEP: CLEAN THE DATA ---
    print("Sanitizing metadata keys...")
    chunks = sanitize_metadata(chunks)
    # --------------------------------

    print(f"Connecting to Weaviate at {WEAVIATE_URL}...")

    # 1. Connect to Weaviate (v4 Client)
    client = weaviate.connect_to_local(
        port=8080,
        grpc_port=50051
    )

    try:
        # 2. Initialize Embeddings
        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )

        print(f"Pushing {len(chunks)} chunks to index '{WEAVIATE_INDEX_NAME}'...")

        # 3. Create/Update the Vector Store
        vector_store = WeaviateVectorStore.from_documents(
            chunks,
            embeddings,
            client=client,
            index_name=WEAVIATE_INDEX_NAME
        )
        
        print("Success! Documents indexed in Weaviate.")

    finally:
        client.close()

if __name__ == "__main__":
    from ingestion.pdf_loader import load_all_pdfs
    from ingestion.chunker import chunk_documents
    
    docs = load_all_pdfs()
    chunks = chunk_documents(docs)
    index_documents(chunks)