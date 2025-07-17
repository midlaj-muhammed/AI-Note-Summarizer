"""
Utility functions for the AI Notes Summarizer application
"""

import logging
import streamlit as st
from typing import Optional
import re

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def validate_input(text: str, min_length: int = 50) -> bool:
    """
    Validate input text
    
    Args:
        text: Input text to validate
        min_length: Minimum required length
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not text or not text.strip():
        st.error("Please provide some text content")
        return False
    
    if len(text.strip()) < min_length:
        st.error(f"Text is too short. Please provide at least {min_length} characters.")
        return False
    
    return True

def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    
    Args:
        text: Raw text content
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\'\/]', ' ', text)
    
    # Clean up multiple spaces
    text = ' '.join(text.split())
    
    return text.strip()

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def display_summary_stats(original_text: str, summary: str):
    """
    Display statistics about the summarization
    
    Args:
        original_text: Original input text
        summary: Generated summary
    """
    original_words = len(original_text.split())
    summary_words = len(summary.split())
    compression_ratio = (1 - summary_words / original_words) * 100 if original_words > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Original Words", f"{original_words:,}")
    
    with col2:
        st.metric("Summary Words", f"{summary_words:,}")
    
    with col3:
        st.metric("Compression", f"{compression_ratio:.1f}%")

def create_download_link(content: str, filename: str = "summary.txt") -> str:
    """
    Create a download link for the summary
    
    Args:
        content: Content to download
        filename: Name of the file
        
    Returns:
        str: Download link HTML
    """
    import base64
    
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Summary</a>'
    return href
