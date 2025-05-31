import PyPDF2
import re
from io import BytesIO
import requests

def extract_text_from_pdf(file_path):
    """Extract text content from PDF file with optimizations"""
    file = None
    try:
        # Check if it's a URL
        if file_path.startswith(('http://', 'https://')):
            response = requests.get(file_path)
            file = BytesIO(response.content)
        else:
            file = open(file_path, 'rb')
        
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        # Only extract first 5 pages for speed
        num_pages = min(len(reader.pages), 5)
        
        for i in range(num_pages):
            page = reader.pages[i]
            text += page.extract_text() + "\n"
            
        # Clean and compress text
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
        
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    finally:
        if file is not None and not isinstance(file, BytesIO):
            file.close()