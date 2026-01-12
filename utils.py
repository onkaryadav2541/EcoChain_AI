from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Reads a PDF file and returns the text content.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {e}")