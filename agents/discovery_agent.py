import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Dict
from tools.search.arxiv_tool import arxiv_search, Paper
from tools.search.google_scholar_tool import google_scholar_search
from tools.search.duckduckgo_tool import duckduckgo_search


class PaperDiscoveryAgent:
    """Agent that discovers research papers from multiple sources"""
    
    def __init__(self):
        self.name = "Paper Discovery Agent"
    
    def discover_papers(self, query: str, max_papers: int = 50) -> Dict[str, List]:
        """
        Discover papers from multiple sources
        
        Args:
            query: Research query
            max_papers: Maximum papers to find
            
        Returns:
            Dictionary with papers from different sources
        """
        print("\n" + "="*60)
        print(f"🔍 {self.name} ACTIVATED")
        print("="*60)
        print(f"Query: {query}")
        print(f"Target: {max_papers} papers\n")
        
        results = {
            'arxiv_papers': [],
            'scholar_papers': [],
            'web_results': []
        }
        
        print("1️⃣ Searching ArXiv...")
        results['arxiv_papers'] = arxiv_search(query, max_results=max_papers)
        
        print("\n2️⃣ Searching Google Scholar...")
        results['scholar_papers'] = google_scholar_search(query, max_results=10)
        
        print("\n3️⃣ Searching DuckDuckGo...")
        results['web_results'] = duckduckgo_search(f"{query} research paper", max_results=10)
        
        total = len(results['arxiv_papers']) + len(results['scholar_papers']) + len(results['web_results'])
        
        print("\n" + "="*60)
        print(f"✅ DISCOVERY COMPLETE: {total} sources found")
        print(f"   ArXiv: {len(results['arxiv_papers'])} papers")
        print(f"   Scholar: {len(results['scholar_papers'])} papers")
        print(f"   Web: {len(results['web_results'])} results")
        print("="*60 + "\n")
        
        return results


if __name__ == "__main__":
    agent = PaperDiscoveryAgent()
    results = agent.discover_papers("deep learning medical imaging", max_papers=10)
    
    print("\n📊 Sample ArXiv Paper:")
    if results['arxiv_papers']:
        paper = results['arxiv_papers'][0]
        print(f"Title: {paper.title}")
        print(f"Authors: {', '.join(paper.authors[:3])}")
        print(f"PDF: {paper.pdf_url}")