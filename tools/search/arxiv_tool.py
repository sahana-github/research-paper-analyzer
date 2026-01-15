import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import arxiv
from typing import List
from pydantic import BaseModel, Field


class Paper(BaseModel):
    """Research paper metadata"""
    title: str
    authors: List[str]
    abstract: str
    pdf_url: str
    published: str
    categories: List[str]
    entry_id: str


def arxiv_search(query: str, max_results: int = 50) -> List[Paper]:
    """
    Search ArXiv for research papers
    
    Args:
        query: Search query (e.g., "machine learning healthcare")
        max_results: Maximum number of papers to return
        
    Returns:
        List of Paper objects with metadata
    """
    print(f"🔍 Searching ArXiv for: '{query}'")
    print(f"📊 Max results: {max_results}")
    
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for i, result in enumerate(search.results(), 1):
            paper = Paper(
                title=result.title,
                authors=[str(author) for author in result.authors],
                abstract=result.summary,
                pdf_url=result.pdf_url,
                published=str(result.published.date()),
                categories=result.categories,
                entry_id=result.entry_id
            )
            papers.append(paper)
            
            if i % 10 == 0:
                print(f"  📄 Found {i} papers...")
        
        print(f"✅ Found {len(papers)} papers total")
        return papers
        
    except Exception as e:
        print(f"❌ ArXiv search error: {e}")
        return []


if __name__ == "__main__":
    papers = arxiv_search("deep learning medical imaging", max_results=5)
    
    print("\n" + "="*60)
    print("SAMPLE RESULTS:")
    print("="*60)
    
    for i, paper in enumerate(papers[:3], 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors[:3])}")
        print(f"   Published: {paper.published}")
        print(f"   PDF: {paper.pdf_url}")
        print(f"   Abstract: {paper.abstract[:200]}...")