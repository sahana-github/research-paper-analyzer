from langchain.tools import tool
from tools.search.arxiv_tool import search_arxiv

@tool
def arxiv_search(query: str):
    """Search arXiv for research papers"""
    return search_arxiv(query, max_results=1)
