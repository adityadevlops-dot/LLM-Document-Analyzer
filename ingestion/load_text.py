import os
from pypdf import PdfReader
from docx import Document
from io import BytesIO


def load_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def load_docx(file) -> str:
    doc = Document(file)
    return "\n".join(para.text for para in doc.paragraphs).strip()


def load_txt(file) -> str:
    return file.read().decode("utf-8").strip()


def load_text(uploaded_file) -> str:
    extension = os.path.splitext(uploaded_file.name)[1].lower()

    if extension == ".pdf":
        return load_pdf(uploaded_file)
    elif extension == ".docx":
        return load_docx(uploaded_file)
    elif extension == ".txt":
        return load_txt(uploaded_file)
    else:
        raise ValueError("❌ Unsupported file format")
