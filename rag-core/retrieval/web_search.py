from tavily import TavilyClient
import os

# Hardcode key for now (or put in .env if you prefer)
TAVILY_API_KEY = "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" 

def search_web(query):
    """
    Uses Tavily to find AND scrape data in one go.
    """
    print(f"Searching web via Tavily: '{query}'...")
    
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        
        # 'search_depth="advanced"' scrapes the full page content for us!
        response = client.search(
            query=query, 
            search_depth="basic", 
            max_results=3,
            include_answer=True # Tavily even generates a short answer for us
        )
        
        # Tavily returns clean text automatically. No need for BeautifulSoup!
        results = []
        for result in response.get('results', []):
            results.append({
                "url": result['url'],
                "content": result['content']
            })
            print(f"  [+] Found: {result['url']}")
            
        return results

    except Exception as e:
        print(f"Tavily Search failed: {e}")
        return []