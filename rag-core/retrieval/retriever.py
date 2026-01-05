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

# ... imports ...

def retrieve_context(query, k=3, source_filter=None):
    """
    Retrieves chunks. 
    If source_filter is provided (e.g. "resume"), it ONLY looks at those docs.
    """
    print(f"Searching Weaviate for: '{query}' (Filter: {source_filter})...")
    
    vector_store = get_vector_store()
    
    # Weaviate Filter Syntax
    search_kwargs = {"k": k}
    
    if source_filter:
        # This tells Weaviate: "Only give me chunks where metadata['source'] contains this string"
        # Note: This assumes your resume chunks have metadata={"source": "Jinish_Kathiriya_Resume.pdf"}
        # You might need to adjust the filter value based on your actual filename
        search_kwargs["filter"] = {
            "path": ["source"],
            "operator": "Like",
            "valueString": f"*{source_filter}*" 
        }
    
    results = vector_store.similarity_search(query, **search_kwargs)
    return results

if __name__ == "__main__":
    # Test the search functionality
    test_query = "What experience does Jinish have with GenAI?"
    
    results = retrieve_context(test_query)
    
    print(f"\nFound {len(results)} relevant chunks:")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(doc.page_content[:200] + "...") # Print just the first 200 chars