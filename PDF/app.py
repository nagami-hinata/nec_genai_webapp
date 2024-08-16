import os
import PyPDF2

# Get the Cotomi API key from the environment variable
cotomi_api_key = os.getenv("COTOMI_API_KEY")
if not cotomi_api_key:
    raise ValueError("COTOMI_API_KEY environment variable is not set.")

def pdf_to_text(pdf_path):
    """
    Convert a PDF file to text and return the text and page information.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        A list of tuples, where each tuple contains the page number and the text content of that page.
    """
    page_content = []
    
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page_num in range(len(pdf_reader.pages)):  #len(pdf_reader.pages
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            page_content.append((page_num + 1, page_text))
    
    return page_content

pdf_path = ""  #URLをここに入れる
page_content = pdf_to_text(pdf_path)

for page_num, text in page_content:
    print(f"Page {page_num}:\n{text}\n")