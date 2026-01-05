import time
import nest_asyncio
from playwright.sync_api import sync_playwright
from langchain_core.documents import Document

nest_asyncio.apply()

class DynamicWebLoader:
    def __init__(self):
        self.headless = True

    def scrape_url(self, url):
        print(f"Scraping: {url}...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                
                # Stealth
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                try:
                    # 1. Load Page
                    page.goto(url, timeout=20000, wait_until="domcontentloaded")
                    time.sleep(3) # Wait for redirects to settle
                    
                    # 2. Extract Content (Safe Mode)
                    # We use evaluate_handle to be safer against context destruction
                    try:
                        content = page.evaluate("""() => {
                            return document.body.innerText; 
                        }""")
                    except Exception as e:
                        # Fallback: If JS fails (context destroyed), just grab raw HTML text
                        print(f"  [!] JS Evaluation failed, using fallback. Error: {e}")
                        element = page.query_selector("body")
                        content = element.inner_text() if element else ""
                    
                    browser.close()

                    # 3. Clean and Validate
                    clean_text = "\n".join([line.strip() for line in content.splitlines() if line.strip()])
                    
                    if len(clean_text) < 200: # Increased threshold
                        print("  [-] Content too short (Block/Captcha/Nav/Footer only).")
                        return []
                    
                    title = "Web Page" # Simplify title extraction to avoid another crash
                    
                    return [Document(
                        page_content=clean_text,
                        metadata={"source": url, "title": title}
                    )]

                except Exception as e:
                    print(f"  [!] Timeout/Nav Error: {e}")
                    browser.close()
                    return []

        except Exception as e:
            print(f"  [!] Browser Launch Error: {e}")
            return []

        