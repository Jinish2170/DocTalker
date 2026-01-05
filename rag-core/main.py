import sys
import warnings
warnings.filterwarnings("ignore")

from retrieval.router import route_query
from retrieval.web_search import search_web
from ingestion.scrapers import DynamicWebLoader
from retrieval.qa import format_docs, generate_answer # Reuse your existing QA logic

def answer_with_web_playwright(query):
    # 1. Find Links (DDGS)
    urls = search_web(query, max_results=2) # Keep it low to save time
    
    if not urls: 
        return "I couldn't find any relevant links on the web."

    # 2. Scrape Content (Playwright)
    loader = DynamicWebLoader()
    # Mute the browser for production feel (set headless=True in scrapers.py if you want)
    web_docs = []
    
    print("Scraping content with Playwright...")
    for url in urls:
        # Check if url is valid
        if not url.startswith("http"): continue
        
        new_docs = loader.scrape_url(url)
        if new_docs:
            web_docs.extend(new_docs)

    if not web_docs: 
        return "I found links, but the scraper couldn't read them (Anti-bot blockage)."

    # 3. Answer (LLM)
    # We construct a temporary prompt just for this web answer
    print(f"Synthesizing answer from {len(web_docs)} pages...")
    context_text = format_docs(web_docs)
    
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    from config.settings import OLLAMA_BASE_URL, LLM_MODEL
    
    llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    template = """You are a helpful assistant. Answer the question based strictly on the provided Web Context.
    
    Web Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    return chain.invoke({"context": context_text, "question": query})


def start_chat():
    print("--- Jinish's Personal RAG (Playwright Edition) ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]: break
            if not user_input.strip(): continue

            # 1. The Brain (Router)
            target = route_query(user_input)
            print(f"Routing Decision: [{target}]")

            if target == "WEB":
                response = answer_with_web_playwright(user_input)
            else:
                # Local Resume Search
                # Note: Ensure you have run 'python -m ingestion.embedder' to load your resume!
                response = generate_answer(user_input)

            print(f"\nAI: {response}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"System Error: {e}")

if __name__ == "__main__":
    start_chat()