import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def get_resume_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

def load_single_resume(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    return filename, extract_text_from_pdf(file_path)



# def save_extracted_text(filename, text, output_folder):
#     # Remove the .pdf extension and add .txt
#     txt_filename = os.path.splitext(filename)[0] + '.txt'
    
#     # Create the output folder if it doesn't exist
#     os.makedirs(output_folder, exist_ok=True)
    
#     # Full path for the output file
#     output_path = os.path.join(output_folder, txt_filename)
    
#     # Write the extracted text to the file
#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.write(text)

# # Add this to the existing load_single_resume function
# def load_single_resume(folder_path, filename):
#     file_path = os.path.join(folder_path, filename)
#     text = extract_text_from_pdf(file_path)
    
#     # Save the extracted text
#     output_folder = os.path.join(folder_path, 'extracted_text')
#     save_extracted_text(filename, text, output_folder)
    
#     return filename, text