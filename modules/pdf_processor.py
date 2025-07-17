"""
PDF Processing Module
Handles PDF file upload, text extraction, and preprocessing.
"""

import PyPDF2
import io
import re
from typing import Optional, List
import streamlit as st


class PDFProcessor:
    """Class to handle PDF file processing and text extraction"""

    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit

    def validate_pdf(self, uploaded_file) -> bool:
        """
        Validate uploaded PDF file

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            bool: True if valid, False otherwise
        """
        # Check file size
        if uploaded_file.size > self.max_file_size:
            st.error(
                f"File size ({uploaded_file.size / 1024 / 1024:.1f}MB) exceeds limit (10MB)"
            )
            return False

        # Check file type
        if uploaded_file.type != "application/pdf":
            st.error("Please upload a valid PDF file")
            return False

        return True

    def extract_text_from_pdf(self, uploaded_file) -> Optional[str]:
        """
        Extract text content from uploaded PDF file

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            str: Extracted text content or None if extraction fails
        """
        try:
            # Reset file pointer
            uploaded_file.seek(0)

            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))

            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                st.error(
                    "❌ Cannot process encrypted PDF files. Please upload an unencrypted PDF."
                )
                return None

            # Check number of pages
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                st.error("❌ PDF file appears to be empty or corrupted.")
                return None

            if num_pages > 100:
                st.warning(
                    f"⚠️ Large PDF detected ({num_pages} pages). Processing may take longer."
                )

            # Extract text from all pages
            text_content = ""
            failed_pages = []

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():  # Only add non-empty pages
                        text_content += page_text + "\n"
                except Exception as e:
                    failed_pages.append(page_num + 1)
                    continue

            # Report failed pages
            if failed_pages:
                if len(failed_pages) < 5:
                    st.warning(
                        f"⚠️ Could not extract text from pages: {', '.join(map(str, failed_pages))}"
                    )
                else:
                    st.warning(
                        f"⚠️ Could not extract text from {len(failed_pages)} pages"
                    )

            if not text_content.strip():
                st.error(
                    "❌ No readable text content found in the PDF file. The PDF might contain only images or scanned content."
                )
                return None

            # Check if extracted text is too short
            if len(text_content.strip()) < 100:
                st.warning(
                    "⚠️ Very little text was extracted. The PDF might contain mostly images or have formatting issues."
                )

            return text_content

        except PyPDF2.errors.PdfReadError as e:
            st.error(f"❌ Invalid or corrupted PDF file: {str(e)}")
            return None
        except MemoryError:
            st.error("❌ PDF file is too large to process. Please try a smaller file.")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error processing PDF file: {str(e)}")
            return None

    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess extracted text

        Args:
            text: Raw extracted text

        Returns:
            str: Cleaned and preprocessed text
        """
        if not text:
            return ""

        # Remove excessive whitespace and newlines
        text = re.sub(r"\n+", "\n", text)
        text = re.sub(r"\s+", " ", text)

        # Remove special characters that might interfere with processing
        text = re.sub(r"[^\w\s\.\,\!\?\;\:\-\(\)]", " ", text)

        # Remove extra spaces
        text = " ".join(text.split())

        return text.strip()

    def process_pdf(self, uploaded_file) -> Optional[str]:
        """
        Complete PDF processing pipeline

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            str: Processed text content or None if processing fails
        """
        if not self.validate_pdf(uploaded_file):
            return None

        # Extract text
        raw_text = self.extract_text_from_pdf(uploaded_file)
        if raw_text is None:
            return None

        # Preprocess text
        processed_text = self.preprocess_text(raw_text)

        if len(processed_text) < 50:
            st.warning(
                "The extracted text is very short. Please check if the PDF contains readable text."
            )

        return processed_text
