import weaviate
from langchain_ollama import OllamaEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from config.settings import WEAVIATE_URL, WEAVIATE_INDEX_NAME, EMBEDDING_MODEL, OLLAMA_BASE_URL

def get_vector_store():
    """
    Connects to the existing Weaviate index and returns the VectorStore object.
    """
    client = weaviate.connect_to_local(
        port=8080,
        grpc_port=50051
    )

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )

    vector_store = WeaviateVectorStore(
        client=client,
        index_name=WEAVIATE_INDEX_NAME,
        text_key="text",
        embedding=embeddings
    )
    
    return vector_store

def retrieve_context(query, k=3):
    """
    Searches Weaviate for the top 'k' most similar chunks to the query.
    """
    print(f"Searching for: '{query}'...")
    
    vector_store = get_vector_store()
    
    # Perform Similarity Search
    results = vector_store.similarity_search(query, k=k)
    
    return results

if __name__ == "__main__":
    # Test the search functionality
    test_query = "What experience does Jinish have with GenAI?"
    
    results = retrieve_context(test_query)
    
    print(f"\nFound {len(results)} relevant chunks:")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(doc.page_content[:200] + "...") # Print just the first 200 chars