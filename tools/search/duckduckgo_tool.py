import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import requests
from bs4 import BeautifulSoup
from typing import List
from pydantic import BaseModel


class SearchResult(BaseModel):
    """DuckDuckGo search result"""
    title: str
    url: str
    snippet: str


def duckduckgo_search(query: str, max_results: int = 10) -> List[SearchResult]:
    """
    Search using DuckDuckGo
    
    Args:
        query: Search query
        max_results: Number of results
        
    Returns:
        List of SearchResult objects
    """
    print(f"🦆 Searching DuckDuckGo: '{query}'")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    results = []
    
    try:
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        result_divs = soup.find_all('div', class_='result')[:max_results]
        
        for div in result_divs:
            try:
                title_elem = div.find('a', class_='result__a')
                snippet_elem = div.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        snippet=snippet
                    ))
            except:
                continue
        
        print(f"✅ Found {len(results)} results")
        
    except Exception as e:
        print(f"⚠️ DuckDuckGo error: {e}")
    
    return results


if __name__ == "__main__":
    results = duckduckgo_search("artificial intelligence research", max_results=5)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Snippet: {result.snippet[:100]}...")