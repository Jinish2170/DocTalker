import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def load_xml_from_url(url, content_tags=["description", "summary", "content"], metadata_tags=["title", "link", "pubDate"]):
    """
    Fetches an XML file from a URL and extracts specific tags.
    Returns a list of LangChain Document objects.
    
    Args:
        url (str): The URL of the XML file (RSS feed, Sitemap, etc.)
        content_tags (list): XML tags that contain the actual text we want to chunk.
        metadata_tags (list): XML tags to keep as extra info (not chunked).
    """
    print(f"Fetching XML from: {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise error if download fails
        
        # Use 'xml' parser specifically
        soup = BeautifulSoup(response.content, "xml")
        
        documents = []
        
        # In most XML feeds (RSS/Atom), items are inside <item> or <entry> tags
        items = soup.find_all(["item", "entry", "url"]) 
        
        print(f"Found {len(items)} items in XML.")

        for item in items:
            # 1. Extract the main content (The "Body")
            # We look for the first tag that matches our list (description, summary, etc.)
            content_text = ""
            for tag in content_tags:
                found_tag = item.find(tag)
                if found_tag and found_tag.text:
                    content_text = found_tag.text.strip()
                    break # Stop once we find content
            
            # If no content found, skip this item
            if not content_text:
                continue

            # 2. Extract Metadata (The "Header")
            metadata = {"source": url, "type": "xml"}
            for tag in metadata_tags:
                found_tag = item.find(tag)
                if found_tag:
                    metadata[tag] = found_tag.text.strip()

            # 3. Create the Standardized Document
            # This is the "Adapter" moment. We make XML look just like a PDF to the system.
            doc = Document(page_content=content_text, metadata=metadata)
            documents.append(doc)

        print(f"Successfully processed {len(documents)} XML documents.")
        return documents

    except Exception as e:
        print(f"Error loading XML: {e}")
        return []

# Test Block
if __name__ == "__main__":
    # Test with a real Tech News RSS Feed (The Verge or similar)
    # This is a safe, public XML URL
    TEST_URL = "http://feeds.bbci.co.uk/news/technology/rss.xml"
    
    docs = load_xml_from_url(TEST_URL)
    
    if docs:
        print("\n--- SAMPLE XML ENTRY ---")
        print(f"Title: {docs[0].metadata.get('title')}")
        print(f"Content: {docs[0].page_content}")
        print("------------------------")