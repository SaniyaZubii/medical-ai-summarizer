import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    text = ""  # Initialized inside the function
    
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        
        if text:
            text = text.encode("ascii", "ignore").decode()
            text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\s+', ' ', text).strip()
            
    except Exception as e:
        print(f"Error reading PDF: {e}")
        
    return text  # <--- Make sure there are 4 spaces before 'return'