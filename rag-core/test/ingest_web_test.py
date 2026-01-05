from ingestion.web_loader import load_web_page
from ingestion.chunker import chunk_documents
from ingestion.embedder import index_documents

# 1. Define the URL
# Let's try something specific so we can test the answer later
URL = "https://en.wikipedia.org/wiki/Large_language_model"

# 2. Load
print(f"--- Step 1: Loading {URL} ---")
raw_docs = load_web_page(URL)

# 3. Chunk
# Wikipedia pages are long! Expect 20-30 chunks here.
print(f"--- Step 2: Chunking ---")
chunks = chunk_documents(raw_docs)

# 4. Index
print(f"--- Step 3: Indexing to Weaviate ---")
index_documents(chunks)