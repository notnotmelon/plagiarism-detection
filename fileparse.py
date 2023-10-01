from docx import Document
from PyPDF2 import PdfReader

def get_text(filename):
    try:
        if filename.endswith('.docs') or filename.endswith('.doc') or filename.endswith('.docx'):
            doc = Document(filename)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        elif filename.endswith('.pdf'):
            reader = PdfReader(filename)
            full_text = ''
            for page in reader.pages:
                full_text += page.extract_text() + '\n'
            return full_text
        else:
            with open(filename, 'r') as file:
                return file.read()
    except:
        return None