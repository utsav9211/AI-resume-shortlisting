"""
Text extraction utilities for resumes: PDF, DOCX, TXT
"""
from pathlib import Path
from typing import Optional
from io import StringIO
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document


def extract_text_from_pdf(path: str) -> str:
    """Extract text from a PDF file using pdfminer.six"""
    return pdf_extract_text(path)


def extract_text_from_docx(path: str) -> str:
    """Extract text from a DOCX file using python-docx"""
    doc = Document(path)
    texts = [p.text for p in doc.paragraphs]
    return "\n".join(texts)


def extract_text_from_txt(path: str) -> str:
    """Read text from a plain text file"""
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def extract_text(path: str) -> Optional[str]:
    """Main function to extract text given a file path; returns None if unsupported."""
    if not Path(path).exists():
        return None
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    elif suffix in (".docx", ".doc"):
        return extract_text_from_docx(path)
    elif suffix in (".txt",):
        return extract_text_from_txt(path)
    else:
        # unsupported file type
        return None
