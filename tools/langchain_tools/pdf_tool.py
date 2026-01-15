from langchain.tools import tool
from tools.scraping.pdf_downloader import download_pdf

@tool
def download_pdf_tool(pdf_url: str):
    """Download research paper PDF"""
    return download_pdf(pdf_url)
