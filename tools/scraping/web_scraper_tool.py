import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict


def scrape_webpage(url: str) -> Optional[Dict[str, str]]:
    """
    Scrape webpage content
    
    Args:
        url: Webpage URL
        
    Returns:
        Dictionary with title, text, links
    """
    print(f"🌐 Scraping: {url[:60]}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('title')
        title_text = title.get_text() if title else "No title"
        
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        links = [a['href'] for a in soup.find_all('a', href=True)][:20]
        
        result = {
            'title': title_text,
            'text': text[:5000],
            'links': links,
            'url': url
        }
        
        print(f"✅ Scraped {len(text)} characters")
        return result
        
    except Exception as e:
        print(f"❌ Scraping error: {e}")
        return None


if __name__ == "__main__":
    result = scrape_webpage("https://arxiv.org")
    
    if result:
        print(f"\nTitle: {result['title']}")
        print(f"Text preview: {result['text'][:200]}...")
        print(f"Found {len(result['links'])} links")