# app/file_utils.py

import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def extract_text(file_path: str) -> str:
    """
    Detect file type by extension and extract text.
    Supports: .pdf, .docx
    """
    path_lower = file_path.lower()

    if path_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    if path_lower.endswith(".docx"):
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported file type. Please upload a PDF or DOCX resume.")
