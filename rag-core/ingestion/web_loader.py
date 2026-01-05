import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def clean_html(soup):
    """
    Engineering Choice: 'Noise Reduction'
    We remove tags that are visible to humans but useless for AI context.
    """
    # 1. Remove JavaScript and CSS (The biggest noise)
    for script in soup(["script", "style"]):
        script.extract()

    # 2. Remove Navigation and Footers (Repetitive text)
    for tag in soup(["nav", "footer", "header", "aside"]):
        tag.extract()

    return soup

def load_web_page(url):
    """
    Fetches a web page, cleans the HTML, and returns the main text.
    """
    print(f"Scraping Web Page: {url}...")
    
    # UPDATED HEADER: Looks exactly like Chrome on Windows
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }

    try:
        # Increase timeout to 15 seconds to prevent 'read timed out'
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # --- CLEANING PHASE ---
        soup = clean_html(soup)
        
        # --- EXTRACTION PHASE ---
        # Heuristic: Try to find the 'main' content first.
        # Most modern sites use <main> or <article> tags.
        content_element = soup.find('main') or soup.find('article')
        
        if content_element:
            text = content_element.get_text(separator="\n")
        else:
            # Fallback: If no <main> tag, grab the whole body (messier, but works)
            print("Warning: No <main> tag found. Falling back to <body>.")
            text = soup.body.get_text(separator="\n") if soup.body else ""

        # Collapse whitespace (turn multiple newlines into one)
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        if not clean_text:
            print("Warning: Page content was empty after cleaning.")
            return []

        # Return as a Document
        metadata = {"source": url, "type": "web_page"}
        return [Document(page_content=clean_text, metadata=metadata)]

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Test Block
if __name__ == "__main__":
    # Test on a Wikipedia page (Great for testing because it has clear structure)
    TEST_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    docs = load_web_page(TEST_URL)
    
    if docs:
        print("\n--- SAMPLE WEB CONTENT ---")
        print(f"Source: {docs[0].metadata['source']}")
        print(f"Snippet: {docs[0].page_content[:500]}...") # Print first 500 chars
        print("--------------------------")