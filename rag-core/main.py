import sys
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

from retrieval.router import route_query
from retrieval.web_search import search_web
from ingestion.web_loader import load_web_page
from retrieval.qa import generate_answer, format_docs
from retrieval.retriever import retrieve_context

# --- NEW: Function to answer using Web Data ---
# ... inside main.py ...

def answer_with_web(query):
    # 1. Search & Scrape (One Step)
    from retrieval.web_search import search_web
    
    results = search_web(query)
    if not results:
        return "I couldn't find anything on the web."

    # 2. Format Context
    # Tavily gave us clean content already
    context_text = "\n\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in results])
    
    print(f"Feeding {len(results)} search results to AI...")

    # 3. Ask AI
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    from config.settings import OLLAMA_BASE_URL, LLM_MODEL

    llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    template = """You are a research assistant. Answer strictly based on the provided web context.
    
    Web Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    return chain.invoke({"context": context_text, "question": query})


def start_chat():
    print("--- Jinish's Answer Engine (Hybrid RAG) ---")
    print("Type 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]: break
            if not user_input.strip(): continue

            # --- THE ROUTER ---
            target = route_query(user_input)
            print(f"Routing to: [{target}]")

            if target == "WEB":
                response = answer_with_web(user_input)
            else:
                # Use existing QA logic (Weaviate)
                response = generate_answer(user_input)

            print(f"\nAI: {response}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_chat()