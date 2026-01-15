import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import requests
import pdfplumber
from io import BytesIO
from typing import Optional
import time


def download_pdf_tool(pdf_url: str) -> Optional[bytes]:
    """
    Download PDF from URL
    
    Args:
        pdf_url: URL to PDF file
        
    Returns:
        PDF bytes or None
    """
    print(f"📥 Downloading PDF: {pdf_url[:60]}...")
    
    try:
        response = requests.get(pdf_url, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Downloaded {len(response.content)} bytes")
            return response.content
        else:
            print(f"❌ Failed: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None


def extract_text_tool(pdf_bytes: bytes) -> Optional[str]:
    """
    Extract text from PDF bytes
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        Extracted text or None
    """
    print("📄 Extracting text from PDF...")
    
    try:
        pdf_file = BytesIO(pdf_bytes)
        text = ""
        
        with pdfplumber.open(pdf_file) as pdf:
            total_pages = len(pdf.pages)
            print(f"  Pages: {total_pages}")
            
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                
                if i % 5 == 0:
                    print(f"  Processed {i}/{total_pages} pages...")
        
        print(f"✅ Extracted {len(text)} characters")
        return text
        
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return None


def process_pdf_url(pdf_url: str) -> Optional[str]:
    """
    Complete pipeline: download + extract
    
    Args:
        pdf_url: URL to PDF
        
    Returns:
        Extracted text
    """
    pdf_bytes = download_pdf_tool(pdf_url)
    if pdf_bytes:
        return extract_text_tool(pdf_bytes)
    return None


if __name__ == "__main__":
    test_url = "https://arxiv.org/pdf/2301.00001.pdf"
    
    text = process_pdf_url(test_url)
    
    if text:
        print("\n" + "="*60)
        print("EXTRACTED TEXT PREVIEW:")
        print("="*60)
        print(text[:1000])
        print("...")