from duckduckgo_search import DDGS
from playwright.sync_api import sync_playwright
import time

class SearchResultValidator:
    """
    Strict Validator: Rejects anything that smells like spam, foreign SEO farms, or non-content.
    """
    # 1. explicit Blacklist (Known bad actors)
    BLACKLIST_DOMAINS = [
        "baidu.com", "zhidao.baidu.com", "weibo.com", "zhihu.com", # Chinese Social
        "bilibili.com", "csdn.net", "163.com", "sohu.com",
        "youtube.com", "facebook.com", "instagram.com", "tiktok.com", # Social
        "twitter.com", "x.com", "linkedin.com",
        "pinterest.com", "reddit.com", "quora.com",
        "amazon.com", "ebay.com" # Shopping, not news
    ]
    
    BAD_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xml", ".txt"]

    @staticmethod
    def is_valid(url):
        try:
            if not url or not url.startswith("http"): return False
            
            url_lower = url.lower()

            # 1. Check Blacklist
            if any(bad in url_lower for bad in SearchResultValidator.BLACKLIST_DOMAINS):
                return False
            
            # 2. Check File Extensions
            if any(url_lower.endswith(ext) for ext in SearchResultValidator.BAD_EXTENSIONS):
                return False
                
            # 3. (Optional) Force Standard TLDs to avoid weird SEO spam
            # valid_tlds = [".com", ".org", ".net", ".io", ".co", ".us", ".uk", ".gov", ".edu", ".in"]
            # if not any(url_lower.split('/')[2].endswith(tld) for tld in valid_tlds):
            #     return False

            return True
        except:
            return False

def search_web(query, max_results=3):
    print(f"--- Search initiated for: '{query}' ---")
    urls = []

    # --- LAYER 1: DuckDuckGo HTML (Fast) ---
    print("Attempting Layer 1: DuckDuckGo (HTML Backend)...")
    try:
        with DDGS() as ddgs:
            # We use 'text' with region 'us-en'
            results = ddgs.text(query, max_results=10, backend="html", region="us-en")
            for r in results:
                url = r.get('href')
                if SearchResultValidator.is_valid(url):
                    urls.append(url)
            
            if urls:
                print(f"  [+] Layer 1 Success! Found {len(urls)} links.")
                return urls[:max_results]
    except Exception as e:
        print(f"  [!] Layer 1 Failed: {e}")

    # --- LAYER 2: Brave Search (Visual Fallback) ---
    print("Attempting Layer 2: Brave Search (Manual Stealth)...")
    return _search_via_brave_stealth(query, max_results)

def _search_via_brave_stealth(query, max_results):
    urls = []
    try:
        with sync_playwright() as p:
            # 1. Launch Browser
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"] # Standard Stealth Flag
            )
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # 2. MANUAL STEALTH INJECTION (Removes the 'I am a robot' badge)
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # 3. Go to Brave
            page.goto(f"https://search.brave.com/search?q={query}&source=web", timeout=20000)
            
            # 4. Wait & Scrape
            try:
                page.wait_for_selector("#results", timeout=8000)
                links = page.locator("#results a").all()
                
                for link in links:
                    url = link.get_attribute("href")
                    if SearchResultValidator.is_valid(url) and url not in urls:
                        urls.append(url)
                        print(f"  [+] Found: {url}")
                    if len(urls) >= max_results: break
            except:
                print("  [!] Brave timed out (or Captcha).")
                page.screenshot(path="debug_layer2_fail.png")

            browser.close()
            
    except Exception as e:
        print(f"  [!] Layer 2 Failed: {e}")

    return urls

if __name__ == "__main__":
    print(search_web("SpaceX Starship latest news"))