import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Dict, Optional
from tools.scraping.pdf_tool import process_pdf_url
from tools.scraping.web_scraper_tool import scrape_webpage
from tools.search.arxiv_tool import Paper
import time


class ScrapingAgent:
    """Agent that scrapes and extracts content from papers"""
    
    def __init__(self):
        self.name = "Scraping Agent"
    
    def scrape_papers(self, papers: List[Paper], max_papers: int = 20) -> List[Dict]:
        """
        Scrape and extract text from papers
        
        Args:
            papers: List of Paper objects
            max_papers: Maximum papers to process
            
        Returns:
            List of dictionaries with paper content
        """
        print("\n" + "="*60)
        print(f"📥 {self.name} ACTIVATED")
        print("="*60)
        print(f"Processing {min(len(papers), max_papers)} papers\n")
        
        processed_papers = []
        
        for i, paper in enumerate(papers[:max_papers], 1):
            print(f"\n[{i}/{min(len(papers), max_papers)}] Processing: {paper.title[:60]}...")
            
            try:
                # Extract PDF text
                text = process_pdf_url(paper.pdf_url)
                
                if text:
                    processed_papers.append({
                        'title': paper.title,
                        'authors': paper.authors,
                        'abstract': paper.abstract,
                        'full_text': text,
                        'pdf_url': paper.pdf_url,
                        'published': paper.published,
                        'categories': paper.categories
                    })
                    print(f"   ✅ Extracted {len(text)} characters")
                else:
                    print(f"   ⚠️ Skipped (extraction failed)")
                
                # Rate limiting
                if i % 5 == 0:
                    print(f"\n   ⏸️ Pausing (rate limit)...\n")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        print("\n" + "="*60)
        print(f"✅ SCRAPING COMPLETE: {len(processed_papers)} papers processed")
        print("="*60 + "\n")
        
        return processed_papers
    
    def scrape_single_paper(self, paper: Paper) -> Optional[Dict]:
        """Scrape a single paper"""
        
        print(f"📄 Scraping: {paper.title[:50]}...")
        
        try:
            text = process_pdf_url(paper.pdf_url)
            
            if text:
                return {
                    'title': paper.title,
                    'authors': paper.authors,
                    'abstract': paper.abstract,
                    'full_text': text,
                    'pdf_url': paper.pdf_url,
                    'published': paper.published
                }
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return None


if __name__ == "__main__":
    from tools.search.arxiv_tool import arxiv_search
    
    # Find papers
    papers = arxiv_search("machine learning", max_results=3)
    
    # Scrape them
    agent = ScrapingAgent()
    processed = agent.scrape_papers(papers, max_papers=2)
    
    print(f"\n📊 Processed {len(processed)} papers")
    if processed:
        print(f"\nSample: {processed[0]['title']}")
        print(f"Text length: {len(processed[0]['full_text'])} chars")