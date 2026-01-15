from langchain.tools import tool
from tools.scraping.pdf_extractor import extract_text_from_pdf

@tool
def extract_text_tool(pdf_path: str):
    """Extract text from PDF"""
    return extract_text_from_pdf(pdf_path)
