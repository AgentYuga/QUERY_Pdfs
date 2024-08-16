import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def load_resumes(folder_path):
    resumes = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        resumes[filename] = extract_text_from_pdf(file_path)
    return resumes