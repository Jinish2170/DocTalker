from ingestion.xml_loader import load_xml_from_url
from ingestion.chunker import chunk_documents
from ingestion.embedder import index_documents

# 1. Load Data (Source: XML)
# Let's try a different one: NASA Image of the Day
url = "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"
raw_docs = load_xml_from_url(url)

# 2. Chunk Data (Transformation)
# Note: XML snippets are usually small, so chunking might not split them much, 
# but we run it anyway to ensure consistency.
chunks = chunk_documents(raw_docs)

# 3. Index Data (Destination: Weaviate)
index_documents(chunks)