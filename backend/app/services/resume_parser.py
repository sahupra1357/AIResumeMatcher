import PyPDF2
import pdfplumber
import docx
import io
from typing import Optional


class ResumeParser:
    """Service to extract text from resume files (PDF, DOCX)"""

    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file using pdfplumber for better accuracy"""
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text.strip()
        except Exception as e:
            # Fallback to PyPDF2 if pdfplumber fails
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                return text.strip()
            except Exception as fallback_error:
                raise Exception(f"Failed to parse PDF: {str(e)}, Fallback error: {str(fallback_error)}")

    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")

    @staticmethod
    def parse_resume(file_content: bytes, filename: str) -> str:
        """Parse resume based on file extension"""
        filename_lower = filename.lower()

        if filename_lower.endswith('.pdf'):
            return ResumeParser.extract_text_from_pdf(file_content)
        elif filename_lower.endswith('.docx'):
            return ResumeParser.extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file format. Only PDF and DOCX are supported. Got: {filename}")

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean extracted text by removing extra whitespace"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
