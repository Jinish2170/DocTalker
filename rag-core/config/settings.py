import os
from dotenv import load_dotenv

# 1. Load environment variables (like API keys)
load_dotenv()

# 2. Define the base path of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 3. Define where data lives
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# 4. Create directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# 5. Define constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# The URL where Ollama lives (default is localhost:11434)
OLLAMA_BASE_URL = "http://localhost:11434"

# Your specific models (Check 'ollama list' in terminal to get exact names)
LLM_MODEL = "llama3"  
EMBEDDING_MODEL = "nomic-embed-text:latest" # <--- IMPORTANT: Change this to what you actually installed!

# Weaviate Settings (Docker)
WEAVIATE_URL = "http://localhost:8080"  # Check your Docker port!
WEAVIATE_INDEX_NAME = "RAG_Knowledge_Base" # This is like the SQL Table Name